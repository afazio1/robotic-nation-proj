# OSS Discord Music bot

음악을 실행시켜주는 음악봇 입니다. 
실행시키기 전 voice.py에 있는 client.run('your_token')의 your_token을 자신의 봇의 token으로 바꿔주세요



# Requirement

crawling에서 쓰이는 라이브러리
- 자신에게 맞는 chromedriver.exe
- selenium library
- Beautifulsoup4 library
- lxml library

play기능에 쓰이는 라이브러리
- ffmpeg library
- mutagen library
- Spotipy library
- ffprobe library



# How to set up and use ffmpeg

1. Download ffmpeg. gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z
2. Unzip the file, and copy the whole folder to C:\Users\Username\Documents (Destination directory isn’t very important here. Paste where you want, but remember where you pasted.)
3. Press Windows button and search Environment Variables.
4. Below “User variables for [Username]” Scroll down a little, you’ll see “Path”.
5. Click “Path”, hit “Edit” then hit “New”. 
6. Add two directories where you unzipped and pasted before. C:\Users\Username\Documents\ffmpeg, C:\Users\ Username \Documents\ffmpeg\bin
7. Go to C:\Users\Username\Documents\ffmpeg\bin then execute 3 exe files. [ffmpeg, ffplay, ffprobe]
8. Copy 3 exe files [ffmpeg, ffplay, ffprobe] then paste them into C:\Users\Username\AppData\Roaming\Python\Python38\Scripts (Your Python version may be different)
9. Eexecute 3 exe files again.



# How to set up Selenium

1. Check your Chrome version.
2. Visit the [site](https://sites.google.com/a/chromium.org/chromedriver/) and download ChromeDriver.exe for your Chrome version.
3. Unzip the file
4. Please replace the absolute path in crawling_YT.py with the absolute path to the downloaded file. (driver = webdriver.Chrome('Your absolute path of Chromedriver.exe'))



# Command

prefix는 !이며 모든 명령어 앞에는 !를 붙여야합니다.



**음악재생과 관련된 명령어**

- !play [words]       :  words에 대한 유튜브 상위 검색 결과 5개의 제목을 채팅창에 전송합니다. 봇이 반환하는 메시지를 보고 사용자가 !play [숫자(1~5)]를 입력하면 봇이 해당 음악을 재생합니다.
- !q                  :  Queue에 어떤 음악이 들어있는지 알려주는 기능입니다.
- !artist             :  DB에 있는 artist정보를 가져와서 보여주는 기능입니다.
- !auto [artist]      :  Spotify의 API를 이용해 Artist의 Top3 음악을 큐에 저장 및 재생하는 기능입니다.
- !leave              :  음성채널에 있는 봇을 연결끊기 합니다.
- !pause              :  현재 재생하고 있는 음악을 잠시 멈춥니다.
- !resume             :  !pause로 멈춘 음악을 다시 재생시킵니다.
- !stop               :  현재 재생하고 있는 음악을 멈추고 Queue를 비웁니다.
- !is_connected       :  현재 봇이 음성채널에 있는지 확인합니다.



**그 외의 명령어**

monitoring message(passive)  -  항상 돌아가는 기능으로 금지어로 지정한 단어들을 감시하는 기능입니다. 

- !clear [count]      :  채팅채널의 메시지를 삭제하는 기능입니다.
- !banlist            :  금지어로 지정한 단어들을 출력해주는 기능입니다.
- !addban [word]      :  word를 금지어로 지정하는 기능입니다.
- !delban [word]      :  word에 해당하는 금지어를
- !unmute [user]      :  금지어를 5번 이상 입력해 mute가 된 user를 풀어주는 기능입니다.
- !banuserlist        :  금지어를 입력했던 사람들의 목록과 금지어를 몇 번 입력했는지 보여주는 기능입니다.
- !delbanuser [user]  :  user의 금지어 카운트를 0으로 리셋해주는 기능입니다.
- !comment [msg]      :  msg에 단어를 입력하면 단어에 대한 유튜브 상위 검색 결과 5개의 제목을 채팅창에 전송합니다. 
                         봇이 반환하는 메시지를 보고 원하는 제목의 번호에 대한 아이콘을 클릭하면 봇이 해당하는 댓글, 좋아요 갯수, 작성자 닉네임을 가져옵니다.
                         msg에 url주소가 들어간다면 유튜브url에 대한 댓글, 좋아요 갯수, 작성자 닉네임을 가져옵니다.