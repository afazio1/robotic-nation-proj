import threading

class time :
    def __init__(self) :
        self.elapsed_time = 0
        self.song_length = int()
        self.end_flag = False
    async def set_song_length(self, song_length) :
        self.song_length = song_length
    async def start(self) :
        print(self.elapsed_time)
        timer = threading.Timer(1, self.start)
        self.elapsed_time += 1
        timer.start()

        if self.elapsed_time > self.song_length :
            self.end_flag = True
            timer.cancel()

# mytime = time()
# mytime.set_song_length(3)
# mytime.start()