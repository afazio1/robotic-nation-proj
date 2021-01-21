import discord
from discord.ext import commands
import youtube_dl
import os
from dbQuery import BAN as ban
import asyncio
from crawling_YT import Crawling_YT_Title, Crawling_YT_Comment
from mutagen.mp3 import MP3

intent = discord.Intents.default()
intent.typing = False
intent.presences = False
intent.members = True

client = commands.Bot(command_prefix="!", intent = intent)
queue = list()           #현재 큐안의 제목 
url_queue = list()       #현재 큐안의 url
searched_title = list()  #검색 리스트 5개
searched_url = list()    #검색 리스트 5개


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
            print("PermissionError occurd while deletion")
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
    def do_both(self, url) :
        self.download_song(url)
        return self.get_title(url)


@client.command(
    # ADDS THIS VALUE TO THE $HELP PING MESSAGE.
	help="!help q",
	# ADDS THIS VALUE TO THE $HELP MESSAGE.
	brief="!help "
)
async def q(ctx) :
    buf = str()
    i = 1
    if queue :
        for var in queue :
            buf = buf + '[' + str(i) + ']' + ' ' + var + '\n'
            i += 1
        await ctx.send("Queue list\n{}" .format(buf))
    else :
        await ctx.send("Queue is empty")



@client.command()
async def artist(ctx) :
    import dbQuery
    buf = 'List of artists in DB\n'
    buf += dbQuery.READ()
    await ctx.send(buf)


@client.command()
async def auto(ctx, name : str = '') :
    if name == '' :
        await ctx.send("Enter Artist name. To see list of artists, enter !artist")
        return
    import fetch_playlist as fetcher
    for var in fetcher.fetch() :
        queue.append(var)
    buf = 'Added song list\n'
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

def youtube_search(ctx, title) :
    global searched_title
    global searched_url
    i = 1
    buf = 'Search Results\n'
    searched_title.clear()
    searched_url.clear()
    searched_title, searched_url = Crawling_YT_Title(title)
    for var in searched_title :
        buf = buf + '[' + str(i) + ']' + ' ' + var + '\n'
        i += 1
    return buf


@client.command()
async def play(ctx, input : str = '') :
    # global queue                                #queue변수를 local메소드에서 사용하기 위함
    voiceChannel = ctx.author.voice.channel     #메시지 작성자(유저)의 음성채널
    input_is_valid_num = False
    connection_state = False                    #connection_state : 봇이 음성채널에 연결되어있는지 확인하기 위한 변수
    if input == '':
        await ctx.send("RETURN")
        return
    if client.voice_clients :                   #봇이 음성채널에 있으면 connection_state를 True로 변경
        connection_state = True

    def after_song(err):
        if len(queue) > 0:
            next_song = url_queue.pop(0)
            queue.pop(0)
            song_manager = Song()
            _video_title = song_manager.do_both(next_song)
            voice.play(discord.FFmpegPCMAudio("song.mp3"), after=after_song)
        else:
            url_queue.pop(0)
            queue.pop(0)
            return

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    try :
        converted_input = int(input)
        if type(converted_input) is not int :
            raise ValueError
        elif converted_input >= 1 and converted_input <= 5 :
            input_is_valid_num = True
    except ValueError :
        pass
    
            
    if connection_state is True and not voice.is_playing() and not queue :    #봇이 음성채널에 연결됨 && 음악 재생중이 아님 && 큐가 비어있음 -> 음성채널에 연결, 다운로드, 재생, 재생중인 곡 타이틀 알려줌
        if input_is_valid_num is False :                                        #사용자의 메시지가 1부터 5의 값이 아닌 경우, 즉 제목을 입력한 경우 -> input값을 title인자로 넘겨 유튜브 검색 상위 5개 검색결과 가져옴
            youtube_search(ctx, input)
        else :                                                                  #사용자의 메시지가 1부터 5의 값인 경우 -> class Song(기존 파일 삭제, 번호에 맞는 음악 다운로드), connect, method play(재생), nowplaying()
            song_manager = Song()
            video_title = song_manager.do_both(searched_url[converted_input-1])
            queue.clear()
            queue.append(video_title)

            voice.play(discord.FFmpegPCMAudio("song.mp3"), after=after_song)
            await ctx.send("Now playing : {}" .format(str(queue[0])))

    elif connection_state is True and not voice.is_playing() and queue :        #봇이 음성채널에 연결됨 && 음악 재생중이 아님 && 큐가 비어있지 않음 -> queue에서 가져옴, 다운로드, 재생, 재생중인 곡 타이틀 알려줌
        if input_is_valid_num is False :                                        #사용자의 메시지가 1부터 5의 값이 아닌 경우, 즉 제목을 입력한 경우 -> input값을 title인자로 넘겨 유튜브 검색 상위 5개 검색결과 가져옴
            buf = youtube_search(ctx, input)                                    #queue의 첫 번째 원소를 Youtube에 검색해 상위 5개의 결과를 메시지로 리턴함
            await ctx.send(buf)
        else :                                                                  #사용자의 메시지가 1부터 5의 값인 경우 -> class Song(기존 파일 삭제, 번호에 맞는 음악 다운로드), method play(재생), nowplaying()
            song_manager = Song()
            video_title = song_manager.do_both(searched_url[converted_input-1])
            video_url = searched_url[int(input)-1]
            queue.append(video_title)
            url_queue.append(video_url)

            if not queue :  #queue is empty
                await ctx.send("Queue is empty")

    elif connection_state is False :
        queue.clear()
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if input_is_valid_num is False :                                        #사용자의 메시지가 1부터 5의 값이 아닌 경우, 즉 제목을 입력한 경우 -> input값을 title인자로 넘겨 유튜브 검색 상위 5개 검색결과 가져옴
            buf = youtube_search(ctx, input)
            await ctx.send(buf)
        else :                                                                  #사용자의 메시지가 1부터 5의 값인 경우 -> class Song(기존 파일 삭제, 번호에 맞는 음악 다운로드), connect, method play(재생), nowplaying()
            song_manager = Song()
            video_title = song_manager.do_both(searched_url[converted_input-1])
            queue.clear()
            queue.append(video_title)
            
            song_manager = Song()
            video_title = song_manager.do_both(searched_url[converted_input-1])
            queue.clear()
            queue.append(video_title)

            voice.play(discord.FFmpegPCMAudio("song.mp3"), after=after_song)
            await ctx.send("Now playing : {}" .format(str(queue[0])))

    elif voice.is_playing():
        if input_is_valid_num is False :                                        #사용자의 메시지가 1부터 5의 값이 아닌 경우, 즉 제목을 입력한 경우 -> input값을 title인자로 넘겨 유튜브 검색 상위 5개 검색결과 가져옴
            buf = youtube_search(ctx, input)
            await ctx.send(buf)
        else :                                                                  #사용자의 메시지가 1부터 5의 값인 경우 -> class Song(기존 파일 삭제, 번호에 맞는 음악 다운로드), method play(재생), nowplaying()
            song_manager = Song()
            video_url = searched_url[int(input)-1]
            video_title = song_manager.do_both(video_url)
            url_queue.append(video_url)
            queue.append(video_title)


@client.command()
async def nowplaying(ctx) :
    if queue :
        await ctx.send("Now playing : {}" .format(str(queue[0])))
    else :
        await ctx.send("Queue is empty")


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if client.voice_clients :
        await voice.disconnect()
        os.remove("song.mp3")
    else :
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    try:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
    except Exception:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    try:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
    except Exception:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    try:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        queue.clear()
        url_queue.clear()
        voice.stop()
    except Exception:
        await ctx.send("The bot is not connected.")

@client.command(
    help="!clear # 으로 사용, #=삭제할 메세지 숫자(default=20)",
    brief="채팅채널 메세지(채팅)를 삭제해주는 명령어"
) #채팅채널 메세지 삭제 커맨드
async def clear(ctx, amount=20): #삭제할 메세지 수를 입력하지 않으면 20개 삭제
    await ctx.channel.purge(limit=int(amount)+1)#삭제 커맨트 인자 수 만큼 삭제+삭제커맨드메세지 포함 하여 삭제(+1)

@client.command(
    help="!banlist 로 사용",
    brief="금지어 목록을 출력해주는 명령어"
)
async def banlist(ctx):#금지어 목록 출력 커맨드
    banlist = ban.BANREAD() #dbQuery.py의 BAN클래스 에 정의된 BANREAD() 호출 BAN 테이블에 저장된 금지어 목록리턴
    if banlist != []: #데이터베이스의 금지어 목록이 비어있는지 확인
        await ctx.send(banlist)#지정된 금지어 리스트 출력
    else:
        await ctx.send("금지어 목록이 비어있습니다.")

@client.command(
    help="!addban # 으로 사용, #=금지어",
    brief="입력값을 금지어 목록에 추가해주는 명령어"
)
async def addban(ctx, msg=''): #금지어목록 추가
    if msg:
        banlist = ban.BANREAD() #데이터베이스의 금지어 목록을 가져옴
        if msg in banlist:      #추가하려는 금지어가 데이터베이스의 금지어 목록에 있는지 확인
            await ctx.send("금지할 단어가 이미 목록에 있습니다.")
        else:
            ban.BANINSERT(msg)  #금지어 추가를위해 BANINSERT()호출 인자로 금지어 msg 전달
            await ctx.send(ban.BANREAD()) #추가 후 금지어 목록 호출
    else:
        await ctx.send("추가할 금지어를 입력하세요!")

@client.command(
    help="!delban # 으로 사용 #=금지어",
    brief="입력값을 금지어 목록에서 삭제해주는 명령어"
)
async def delban(ctx, msg=''): #금지어목록 삭제
    if msg:
        banlist = ban.BANREAD()
        if msg in banlist:  #삭제할 금지어가 데이터베이스에 있는지 확인
            ban.BANDELETE(msg)  #BANDELETE() 호출하여 금지어 삭제
            await ctx.send(msg+"삭제")
            await ctx.send(ban.BANREAD())   #삭제 후 금지어 목록 호출
        else:
            await ctx.send("삭제할 단어가 목록에 없습니다.")
    else:
        await ctx.send("삭제할 금지어를 입력하세요!")

@client.command(
    help="!unmute @# 으로 사용 @#=멤버 멘션",
    brief="채팅차단을 풀어주는 명령어"
)
async def unmute(ctx, name=''):#채팅밴 언뮤트 명령어
    if name:
        user = await ctx.guild.fetch_member(int(name[3:21])) #입력한 멘션아이디에서 멤버 아이디만 슬라이싱
        await ctx.channel.set_permissions(user,overwrite=None) #슬라이싱한 멤버아이디로 언뮤트
        await ctx.send(str(user)+" 채팅차단 해제!")
    else:
        await ctx.send("채팅차단 해제할 멤버 멘션을 입력하세요")

@client.command(
    help="#!banuserlist 로 사용",
    brief="채팅차단 카운트와 멤버를 출력해주는 명령어"
)
async def banuserlist(ctx): #채팅벤 데이터베이스 출력 명령어
    banuser, banusercount = ban.BANUSERREAD()   #데이터베이스 읽어오기
    if banuser:
        for i in range(len(banuser)):       #가져온 데이터베이스 만큼 반복
            await ctx.send(banuser[i]+"\tban count = "+str(banusercount[i])) #유저 밴카운트 출력
    else:
        await ctx.send("밴유저 목록이 비어있습니다.")

@client.command(
    help="!delbanuser # 으로 사용 @#=밴카운트를 초기화할 멤버 맨션",
    brief="누적된 밴카운트를 초기화해주는 명령어"
) 
async def delbanuser(ctx, name=''):    #밴카운트 초기화 명령어(db에서 삭제)
    if name:
        user = await ctx.guild.fetch_member(int(name[3:21]))
        ban.BANUSERDELETE(str(user))
        await ctx.send(str(user)+" 밴 카운트 초기화")
    else:
        await ctx.send("밴 카운트를 초기화할 멤버 멘션을 입력하세요!")

@client.event
async def on_message(ctx):
    banlist = ban.BANREAD()
    user = ctx.author

    if any([word in ctx.content for word in banlist]):#금지어 삭제 기능
        if ctx.author == client.user:   #금지어 목록 출력을 위해 봇이 쓰는 금지어는 pass
            pass
        elif ctx.content.startswith(client.command_prefix+"delban") or ctx.content.startswith(client.command_prefix+"addban"):#메세지 시작이 !delban명령어일 경우
            await client.process_commands(ctx) #명령어 실행
        else:   #봇 이외에 금지어를 사용하면 메세지를 삭제하고 경고문 출력
            banuser, banusercount = ban.BANUSERREAD()   #채팅밴 데이터베이스 읽어오기
            userstr = str(user) #멤버형 변수는 사용하기 까다롭기때문에 문자열로 변환
            if userstr in banuser:  #금지어를 사용한멤버가 데이터베이스에 있다면(2번이상 사용자)
                ban.BANUSERUPDATE(userstr,banusercount[banuser.index(userstr)])#업데이트 명령어
                await ctx.channel.send(userstr+"\tban count = "+str((banusercount[banuser.index(userstr)]+1)))

                if banusercount[banuser.index(userstr)]+1 > 4: #밴카운트가 5번 이상
                    await ctx.channel.set_permissions(user,send_messages=False) #채팅금지(MUTE)
                    ban.BANUSERDELETE(userstr)  #채팅금지 후 데이터베이스에서 삭제
                    await ctx.channel.send(userstr+"MUTE!")
            else:
                ban.BANUSERINSERT(userstr, int(1)) #금지어 사용이 처음인경우 데이터베이스 삽입
                await ctx.channel.send(userstr+"\tban count = "+ '1')

            await ctx.delete()
            await ctx.channel.send("금지어를 사용하였습니다. 금지어를 계속 사용하면 차단될 수 있습니다.")
    else:
        await client.process_commands(ctx)

@client.command()
async def comment(ctx, url:str):
    #입력한 str이 url일 경우
    if url.find("youtube.com/watch") > -1:
        yt_id, yt_comment, yt_like = Crawling_YT_Comment(url)
        if len(yt_id)>10:
            yt_id, yt_comment, yt_like = yt_id[:10], yt_comment[:10], yt_like[:10]
        emb = discord.Embed(title="TOP 10 Comments",description="This is comment about {}".format(url),color=discord.Color.blue())
        emb.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        for i in range(len(yt_id)):
            emb.add_field(name="{} (🧡{})".format(yt_id[i], yt_like[i]), value="{}".format(yt_comment[i]),inline=False)
        if len(yt_id)==0:
            emb.add_field(name="Error or No comment", value="Please check the url")
        await ctx.send(embed=emb)

    #입력한 str이 검색어일 경우
    else:
        reaction_list = ['\U00000031\U0000FE0F\U000020E3','\U00000032\U0000FE0F\U000020E3','\U00000033\U0000FE0F\U000020E3','\U00000034\U0000FE0F\U000020E3','\U00000035\U0000FE0F\U000020E3']
        def chk_user(reaction, us):
            return us == ctx.author and reaction.message.id == re_msg.id
        
        titles, hrefs = Crawling_YT_Title(url)
        emb1 = discord.Embed(title="Select the title", description = "Select the number", color=discord.Color.dark_blue())
        for i in range(len(titles)):
            emb1.add_field(name="{}번".format(i+1), value="{}".format(titles[i]), inline=False)

        #반응을 누르기위해 기본반응 추가
        re_msg = await ctx.send(embed=emb1)
        for i in reaction_list:
            await re_msg.add_reaction(i)

        emb2 = discord.Embed(title="Youtube", description="" ,color=discord.Color.dark_blue())
        try:
            reaction, _r_user = await client.wait_for('reaction_add', timeout=5.0, check = chk_user)
        except asyncio.TimeoutError:
            emb2.add_field(name="Time out", value="처음부터 다시 입력해주세요")
            await ctx.send(embed=emb2)
            return
        else:
            num = 0
            if str(reaction) == reaction_list[0]:
                num = 0
            elif str(reaction) == reaction_list[1]:
                num = 1
            elif str(reaction) == reaction_list[2]:
                num = 2
            elif str(reaction) == reaction_list[3]:
                num = 3
            elif str(reaction) == reaction_list[4]:
                num = 4

            yt_id, yt_comment, yt_like = Crawling_YT_Comment(hrefs[num])
            if len(yt_id)>10:
                yt_id, yt_comment, yt_like = yt_id[:10], yt_comment[:10], yt_like[:10]
            emb2 = discord.Embed(title="TOP 10 Comments",description="This is comment about {}".format(url),color=discord.Color.blue())
            emb2.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            for i in range(len(yt_id)):
                emb2.add_field(name="{} (🧡{})".format(yt_id[i], yt_like[i]), value="{}".format(yt_comment[i]),inline=False)
            if len(yt_id)==0:
                emb2.add_field(name="Error or No comment", value="Please check the url")
            await ctx.send(embed=emb2)
            return

client.run('Nzk4NDY3MjA3NDc0NTc3NDA5.X_1ciQ.e7W1Up_RRPkXwL1E7UlDedbvp88')