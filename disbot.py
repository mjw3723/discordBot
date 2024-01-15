
#Python version 3.8.0
import yt_dlp as youtube_dl
import discord
from discord.ext import commands
import asyncio
import search
import os
import message as m
import time

TOKEN = os.environ.get("DISCORD_TOKEN")
playlist = [] # url list
infolist =[]  # title,name,imgurl list
autolist = [] # auto url list
autoMode = 0  # 0 Off 1 ON
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''
 
 
ytdl_format_options = {
    """
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
    """
    'quiet': False,
    'default_search': 'ytsearch',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'youtube_include_dash_manifest': False,
}
 
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}
 
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
 
        self.data = data
 
        self.title = data.get('title')
        self.url = data.get('url')
 
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
 
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
 
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
    
    
    
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents,help_command = None)

@bot.event
async def on_ready():
    print(f'{bot.user.name} 연결 완료!')
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'안녕하세요. {member.name}, 환영합니다.!'
    )
@bot.command()
async def help(ctx):
    embed = m.em.helpM()
    await ctx.send(embed=embed)
@bot.command(name='입장')
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.connect()
        embed = discord.Embed(title="봇 입장", color=discord.Color.random())
        await ctx.channel.send(embed=embed)
        await help(ctx)
    else:
        await ctx.send("음성 채널에 유저가 존재하지 않습니다. 1명 이상 입장해 주세요.")

@bot.command(name='나가')
async def exit(ctx):
    await bot.voice_clients[0].disconnect()
    embed = discord.Embed(title="봇 퇴장", color=discord.Color.random())
    await ctx.channel.send(embed=embed)
    
    global autoMode
    if(autoMode==1):
        autoMode = 0
    playlist.clear()
    infolist.clear()
    autolist.clear()


@bot.command(name='재생')
async def reserve(ctx, *args):
    voice_channel = ctx.guild.voice_client
    if voice_channel and voice_channel.is_connected():
        """노래를 예약합니다."""
        global playlist
        parameter = ' '.join(args)
        title,name,url,imgurl = search.getUrl(1, parameter)
        playlist.append(url)
        infolist.append([title,name,imgurl])
        if len(playlist)==1:
            if ctx.voice_client.is_playing():
                embed = m.em.reserveM(ctx,title,name,imgurl)
                return await ctx.send(embed=embed)
            else:
                await play_next(ctx)
            
        else:
            embed = m.em.reserveM(ctx,title,name,imgurl) 
            await ctx.send(embed=embed)
    else:        
        await ctx.send("음성 채널에 봇이 존재하지 않습니다. 입장시켜주세요.")

async def play_next(ctx):
    global playlist
    if len(playlist) > 0:
        url = playlist.pop(0)
        title,name,imgurl = infolist.pop(0)
        
        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        
        def after_playing(error):
            if error:
                print(f'Player error: {error}')
            bot.loop.create_task(play_next(ctx))
        
        ctx.voice_client.play(player, after=after_playing)
        embed = m.em.playM(ctx,title,name,imgurl)
        await ctx.send(embed=embed)
        ctx.voice_client.source.volume = 50 / 100

    else:
        if autoMode ==1 :
            title,name,url,imgurl = autolist.pop(0)
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)

            def after_playing(error):
                if error:
                    print(f'Player error: {error}')
                bot.loop.create_task(play_next(ctx))
        
            ctx.voice_client.play(player, after=after_playing)
            embed = m.em.AutoM(title,name,imgurl)
            await ctx.send(embed=embed)
            ctx.voice_client.source.volume = 50 / 100
        else: 
            await bot.voice_clients[0].disconnect()
            await bot.voice_clients[0].cleanup()
            playlist.clear()
            
            search.driver.close()
@bot.command(name='다음')   
async def skip(ctx):
    if len(playlist)>0 or (autoMode == 1 and len(autolist)>0):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        await play_next(ctx)
    else:
        embed = discord.Embed(title="다음 노래가 없습니다.", color=discord.Color.random())
        await ctx.send(embed=embed)
@bot.command(name='예약목록')
async def list(ctx):
    if len(infolist)>0:
        embed = m.em.listM(infolist)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="예약된 노래가 없습니다.", color=discord.Color.random())
        await ctx.send(embed=embed)
@bot.command(name='소리')
async def volume(ctx, volume: int):
    """Changes the player's volume"""

    if ctx.voice_client is None:
        embed = discord.Embed(title=f"재생중이 아닙니다.", color=discord.Color.random())
        return await ctx.send(embed=embed)

    ctx.voice_client.source.volume = volume / 100
    embed = m.em.volumeM(volume)
    await ctx.send(embed=embed)       
@bot.command(name='일시정지')
async def pause(ctx):
    try:
        ctx.voice_client.pause()
        embed = m.em.pauseM()
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="일시정지할 노래가 없습니다.", color=discord.Color.random())
        await ctx.send(embed=embed)
@bot.command(name='다시재생')
async def resume(ctx):
    try:
        ctx.voice_client.resume()
        embed = m.em.resumeM()
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="다시 재생할 노래가 없습니다.", color=discord.Color.random())
        await ctx.send(embed=embed)
@bot.command(name='오토')
async def auto(ctx):
    global autoMode
    global autolist
    if autoMode == 0:
        autolist = search.auto()
        embed = m.em.AutoOnOffM(autoMode)
        autoMode = 1
        await ctx.send(embed=embed)
    else:
        autoMode = 0 
        embed = m.em.AutoOnOffM(autoMode)
        await ctx.send(embed=embed)

                
bot.run(TOKEN)

