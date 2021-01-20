import discord
from discord.ext import commands
import youtube_dl
import os
from dbQuery import BAN as ban

intent = discord.Intents.default()
intent.typing = False
intent.presences = False
intent.members = True
client = commands.Bot(command_prefix="#", intent = intent)
queue = list()

class Song :
    def __init__(self) :
        ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
        }
        self.ydl_opts = ydl_opts
    def download_song(self, url) :
        song_there = os.path.isfile("song.mp3")
        try :
            if song_there :
                os.remove("song.mp3")
        except PermissionError:
            return

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
    def get_title(self, url) :
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
        return video_title


@client.command()
async def auto(ctx) :
    import fetch_playlist as fetcher
    for var in fetcher.fetch() :
        queue.append(var)
    buf = 'Added song list'
    i = 1
    for var in queue :
        buf = buf + '[' + str(i) + ']' + ' ' + var + '\n'
        i += 1
    await ctx.send(buf)

@client.command()
async def is_connected(ctx) :
    if client.voice_clients :
        await ctx.send("State : connected")
    else :
        await ctx.send("State : not connected")

@client.command()
async def newplay(ctx, url : str):
    voiceChannel = ctx.author.voice.channel
    
    connection_state = False
    # if client.voice_clients :
    #     connection_state = True
    
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    if connection_state is True and not voice.is_playing() :    #기존 파일 삭제, 다운로드, 재생, nowplaying()
        song_manager = Song()
        song_manager.download_song(url)
        video_title = song_manager.get_title(url)
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        queue.append(video_title)
        await ctx.send("Now playing : {}" .format(str(queue[0]))) 
    elif connection_state is True and voice.is_playing() :
        song_manager = Song()
        new_song_title = song_manager.get_title(url)
        queue.append(new_song_title)
        await ctx.send("Now playing : {}" .format(str(queue[0])))
        await ctx.send("Added new song : {}" .format(new_song_title))
    elif connection_state is False :                            #음성채널 연결, 다운로드, 재생
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        song_manager = Song()
        song_manager.download_song(url)
        video_title = song_manager.get_title(url)
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        queue.append(video_title)
        await ctx.send("Now playing : {}" .format(str(queue[0])))
    

@client.command()
async def nowplaying(ctx) :
    if queue :
        await ctx.send("Now playing : {}" .format(str(queue[0])))
    else :
        await ctx.send("Queue is empty")

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    # voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    voiceChannel = ctx.author.voice.channel
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        queue.append(video_title)
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    nowplaying(ctx)


@client.command()
async def leave(ctx):
    # voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    # if voice.is_connected():
    #     await voice.disconnect()
    # else:
    #     await ctx.send("The bot is not connected to a voice channel.")

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if client.voice_clients :
        await voice.disconnect()
    else :
        await ctx.send("The bot is not connected to a voice channel.")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command() #채팅채널 메세지 삭제 커맨드
async def clear(ctx, amount):
    await ctx.channel.purge(limit=int(amount)+1)#삭제 커맨트 인자 수 만큼 삭제+삭제커맨드메세지 포함 하여 삭제(+1)

@client.command()
async def banlist(ctx):#금지어 목록 출력 커맨드
    banlist = ban.BANREAD() #dbQuery.py의 BAN클래스 에 정의된 BANREAD() 호출 BAN 테이블에 저장된 금지어 목록리턴
    if banlist != []: #데이터베이스의 금지어 목록이 비어있는지 확인
        await ctx.send(banlist)#지정된 금지어 리스트 출력
    else:
        await ctx.send("banlist's empty")

@client.command()
async def addban(ctx, msg): #금지어목록 추가
    banlist = ban.BANREAD() #데이터베이스의 금지어 목록을 가져옴
    if msg in banlist:      #추가하려는 금지어가 데이터베이스의 금지어 목록에 있는지 확인
        await ctx.send("이미 목록에 있습니다.")
    else:
        ban.BANINSERT(msg)  #금지어 추가를위해 BANINSERT()호출 인자로 금지어 msg 전달
        await ctx.send(ban.BANREAD()) #추가 후 금지어 목록 호출

@client.command()
async def delban(ctx, msg): #금지어목록 삭제
    banlist = ban.BANREAD()
    if msg in banlist:  #삭제할 금지어가 데이터베이스에 있는지 확인
        ban.BANDELETE(msg)  #BANDELETE() 호출하여 금지어 삭제
        await ctx.send(msg+"삭제")
        await ctx.send(ban.BANREAD())   #삭제 후 금지어 목록 호출
    else:
        await ctx.send("목록에 없습니다.")

@client.command()
async def unmute(ctx, name):
    user = await ctx.guild.fetch_member(int(name[3:21]))
    await ctx.channel.set_permissions(user,overwrite=None)
    await ctx.send(str(user)+" unmute!")

@client.command()
async def banuserlist(ctx):
    banuser, banusercount = ban.BANUSERREAD()
    print('tasd')
    for i in range(len(banuser)):
        print(banuser[i],banusercount[i])
        await ctx.send(banuser[i]+" "+str(banusercount[i]))

@client.event
async def on_message(ctx):
    banlist = ban.BANREAD()
    user = ctx.author

    if ctx.author != ctx.guild.owner:
        if any([word in ctx.content for word in banlist]):#금지어 삭제 기능
            if ctx.author == client.user:   #금지어 목록 출력을 위해 봇이 쓰는 금지어는 pass
                pass
            elif ctx.content.startswith(client.command_prefix+"delban"):#메세지 시작이 !delban명령어일 경우
                await client.process_commands(ctx) #명령어 실행
            else:   #봇 이외에 금지어를 사용하면 메세지를 삭제하고 경고문 출력
                banuser, banusercount = ban.BANUSERREAD()
                userstr = str(user)
                print(userstr)
                print(banusercount)
                print(type(banusercount))
                if userstr in banuser:
                    print('실행')
                    ban.BANUSERUPDATE(userstr,banusercount[banuser.index(userstr)])
                    await ctx.channel.send(userstr+" ban count = "+str((banusercount[banuser.index(userstr)]+1)))

                    if banusercount[banuser.index(userstr)]+1 > 4:
                        await ctx.channel.set_permissions(user,send_messages=False)
                        ban.BANUSERDELETE(userstr)
                        await ctx.channel.send(userstr+"MUTE!")
                else:
                    ban.BANUSERINSERT(userstr, int(1))
                    await ctx.channel.send(userstr+" ban count = "+ '1')

                await ctx.delete()
                await ctx.channel.send("That Word Is Not Allowed To Be Used! Continued Use Of Mentioned Word Would Lead To Punishment!")
        else:
            await client.process_commands(ctx)
    else:
        await client.process_commands(ctx)

client.run('YOUR_TOKEN')