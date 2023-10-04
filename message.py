import discord

class em:
    def helpM():
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
        return embed
    
    def reserveM(ctx,title,name,imgurl):
        embed = discord.Embed(title="노래 예약", color=discord.Color.random())
        embed.set_thumbnail(url=imgurl)
        embed.add_field(name=title, value=name, inline=False)
        embed.set_footer(text=f'신청자 : {ctx.author.display_name}님')
        return embed
    
    def playM(ctx,title,name,imgurl):
        embed = discord.Embed(title="노래 시작", color=discord.Color.random())
        embed.set_thumbnail(url=imgurl)
        embed.add_field(name=title, value=name, inline=False) #player.title 사용가능
        embed.set_footer(text=f'신청자 : {ctx.author.display_name}님')
        return embed
    
    def AutoM(title,name,imgurl):
        embed = discord.Embed(title="노래 시작", color=discord.Color.random())
        embed.set_thumbnail(url=imgurl)
        embed.add_field(name=title, value=name, inline=False) #player.title 사용가능
        embed.set_footer(text=f'Auto모드 재생중')
        return embed
    
    def AutoOnOffM(autoMode):
        if autoMode == 0:
            embed = discord.Embed(title="Auto모드 ON", color=discord.Color.random())
            return embed
        else: 
            embed = discord.Embed(title="Auto모드 OFF", color=discord.Color.random())
            return embed
        
    def resumeM():
        embed = discord.Embed(title="음악을 다시 시작 합니다.", color=discord.Color.random())
        return embed
    
    def pauseM():
        embed = discord.Embed(title="음악을 일시정지 합니다.", color=discord.Color.random())
        return embed
    
    def volumeM(volume):
        embed = discord.Embed(title=f"소리 : {volume}%", color=discord.Color.random())
        return embed
    
    def listM(infolist):
        i= 1;
        embed = discord.Embed(title='예약목록', color=discord.Color.random())
        for [title,name,imgurl] in infolist:
            embed.add_field(name=f'{i}:{title}', value=name, inline=False)
            embed.set_thumbnail(url=imgurl)
            i=i+1
        return embed