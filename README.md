# OSS Discord Music bot

음악을 실행시켜주는 음악봇 입니다. 

Requirement

crawling에서 쓰이는 라이브러리
- 자신에게 맞는 chromedriver.exe
- selenium library
- Beautifulsoup4 library
- lxml library

play기능에 쓰이는 라이브러리
- ffmpeg library
- mutagen library
- Spotify library
- ffprobe library


Command

prefix는 !이며 모든 명령어 앞에는 !를 붙여야합니다.

---음악재생과 관련된 명령어---

!play [words]       :  words에 대한 유튜브 상위 검색 결과 5개의 제목을 채팅창에 전송합니다. 봇이 반환하는 메시지를 보고 사용자가 !play [숫자(1~5)]를 입력하면 봇이 해당 음악을 재생합니다.
!q                  :  Queue에 어떤 음악이 들어있는지 알려주는 기능입니다.
!artist             :  DB에 있는 artist정보를 가져와서 보여주는 기능입니다.
!auto [artist]      :  a
!nowplaying         :
!leave              :
!pause              :
!resume             :
!stop               :
!clear              :
!is_connected       :


---그 외의 명령어---

!banlist            :
!addban             :
!delban             :
!unmute             :
!banuserlist        :
!delbanuser         :

!comment            :