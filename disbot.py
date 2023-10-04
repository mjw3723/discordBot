
import yt_dlp as youtube_dl
import discord
from discord.ext import commands
import search
import os
TOKEN = os.environ.get("DISCORD_TOKEN")
playlist = []
infolist =[]
autolist = []
autoMode = 0
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''
 
 
ytdl_format_options = {
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
    print(f'{bot.user.name} has connected to Discord!')
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="봇 명령어", color=discord.Color.random())
    embed.add_field(name='!입장\t봇 보이스채널 초대',value="", inline=False)
    embed.add_field(name='!나가\t봇 보이스채널 퇴장',value="",  inline=False)
    embed.add_field(name='!재생\t유튜브 노래 재생',value="",  inline=False)
    embed.add_field(name='!다음\t다음 노래 재생',value="",  inline=False)
    embed.add_field(name='!예약목록\t예약된 노래목록',value="",  inline=False)
    embed.add_field(name='!소리\t 봇 소리 설정(0~100)',value="",  inline=False)
    embed.add_field(name='!일시정지\t노래 일시정지',value="",  inline=False)
    embed.add_field(name='!다시재생\t노래 다시재생',value="",  inline=False)
    embed.add_field(name='!오토\t재생할 노래 없으면 봇이 자동으로 재생',value="",  inline=False)
    await ctx.send(embed=embed)
@bot.command(name='입장')
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.connect()
        embed = discord.Embed(title="봇 입장", color=discord.Color.random())
        await ctx.channel.send(embed=embed)
        await help(ctx)
        search.driver
    else:
    	await ctx.sendctx.send("음성 채널에 유저가 존재하지 않습니다. 1명 이상 입장해 주세요.")

@bot.command(name='나가')
async def exit(ctx):
    await bot.voice_clients[0].disconnect()
    embed = discord.Embed(title="봇 입장", color=discord.Color.random())
    await ctx.channel.send(embed=embed)
    search.driver.close()


@bot.command(name='재생')
async def reserve(ctx, *args):
    """노래를 예약합니다."""
    global playlist
    parameter = ' '.join(args)
    title,name,url,imgurl = search.getUrl(1, parameter)
    playlist.append(url)
    infolist.append([title,name,imgurl])
    if len(playlist)==1:
        if ctx.voice_client.is_playing():
            embed = discord.Embed(title="노래 예약", color=discord.Color.random())
            embed.set_thumbnail(url=imgurl)
            embed.add_field(name=title, value=name, inline=False)
            embed.set_footer(text=f'신청자 : {ctx.author.display_name}님')
            return await ctx.send(embed=embed)
        else:
            await play_next(ctx)
        
    else:
        embed = discord.Embed(title="노래 예약", color=discord.Color.random())
        embed.add_field(name=title, value=name, inline=False)
        embed.set_footer(text=f'신청자 : {ctx.author.display_name}님')   
        await ctx.send(embed=embed)


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
        embed = discord.Embed(title="노래 시작", color=discord.Color.random())
        embed.set_thumbnail(url=imgurl)
        embed.add_field(name=title, value=name, inline=False) #player.title 사용가능
        embed.set_footer(text=f'신청자 : {ctx.author.display_name}님')
        await ctx.send(embed=embed)
    else:
        if autoMode ==1 :
            title,name,url,imgurl = autolist.pop(0)
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)

            def after_playing(error):
                if error:
                    print(f'Player error: {error}')
                bot.loop.create_task(play_next(ctx))
        
            ctx.voice_client.play(player, after=after_playing)
            embed = discord.Embed(title="노래 시작", color=discord.Color.random())
            embed.set_thumbnail(url=imgurl)
            embed.add_field(name=title, value=name, inline=False) #player.title 사용가능
            embed.set_footer(text=f'Auto모드 재생중')
            await ctx.send(embed=embed)
        else: 
            await bot.voice_clients[0].disconnect()
            search.driver.close()
@bot.command(name='다음')   
async def skip(ctx):
    if len(playlist)>0:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        await play_next(ctx)
    else:await ctx.send("다음 노래가 없습니다.")
@bot.command(name='예약목록')
async def list(ctx):
    i= 1;
    embed = discord.Embed(title='예약목록', color=discord.Color.random())
    for [title,name,imgurl] in infolist:
        embed.add_field(name=f'{i}:{title}', value=name, inline=False)
        i=i+1
    await ctx.send(embed=embed)
@bot.command(name='소리')
async def volume(ctx, volume: int):
    """Changes the player's volume"""
 
    if ctx.voice_client is None:
        return await ctx.send("Not connected to a voice channel.")
 
    ctx.voice_client.source.volume = volume / 100
    embed = discord.Embed(title=f"소리 : {volume}%", color=discord.Color.random())
    await ctx.send(embed=embed)       
@bot.command(name='일시정지')
async def pause(ctx):
    try:
        ctx.voice_client.pause()
        await ctx.send("음악을 일시정지 합니다.")
    except:
        await ctx.send("일시정지 에러")
@bot.command(name='다시재생')
async def resume(ctx):
    try:
        ctx.voice_client.resume()
        await ctx.send("음악을 다시 시작 합니다.")
    except:
        await ctx.send("다시재생 에러")
@bot.command(name='오토')
async def auto(ctx):
    global autoMode
    global autolist
    if autoMode == 0:
        embed = discord.Embed(title="Auto모드 ON", color=discord.Color.random())
        await ctx.send(embed=embed)
        autoMode = 1
        autolist = search.auto() 
    else: 
        autoMode = 0
        embed = discord.Embed(title="Auto모드 OFF", color=discord.Color.random())
        await ctx.send(embed=embed)

                
bot.run(TOKEN)