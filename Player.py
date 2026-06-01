import math, os, time, random, io, pygame
from tkinter import messagebox
from PIL import Image
from mutagen.id3 import ID3
from mutagen.mp3 import MP3

class Player:
    def __init__(self, main, music_folder):
        self.main = main
        self.currentSong = None
        self.currentLength = 0
        self.currentStartTime = 0
        self.currentPauseTime = 0
        self.volume = 0.5
        self.queueType = 1

        self.isPaused = True
        self.isMuted = False

        self.music_folder = music_folder
        self.songs = []
        self.queue = []

    def nextQueueType(self):
        if self.queueType == 3:
            self.queueType = 1
        else :
            self.queueType += 1

    def load_songs(self):
        self.songs.clear()
        files = os.listdir(self.music_folder)

        mp3_files = [
            file for file in files
            if file.lower().endswith(".mp3")
        ]

        for index, song in enumerate(mp3_files):
            self.songs.append(song)

    def check_song_end(self):
        if not pygame.mixer.music.get_busy() and self.isPaused != True and self.currentSong is not None:
            self.moveNextSong()
        else :
            self.main.mainFrame.after(500, self.check_song_end)

    def play_song(self, name):
        index = self.songs.index(name)
        played_song = self.songs[index]
        try:
            print("Próba uruchomienia utworu '"+played_song+"'")

            self.currentSong = self.songs[index]
            full_path = os.path.join(
                self.music_folder,
                played_song
            )

            audio = MP3(full_path)
            self.currentLength = math.floor(audio.info.length)

            print("Długość utworu : ", self.currentSong)

            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play()
            self.currentStartTime = time.time()
            self.isPaused = False
            self.currentSong = played_song
            self.check_song_end()
            if not self.queue :
                self.queue.insert(0, self.currentSong)

            print("Uruchomiono utwór!")
        except Exception as e:
            messagebox.showerror(
                "Błąd 'play_song'",
                f"Nie udało się odtworzyć utworu\n\n{e}"
            )

    def addAndPlay(self, song):
        self.addNext(song)
        self.moveNextSong()

    def clearQueue(self):
        self.stopSong()
        self.queue.clear()

    def playFromPlaylist(self, song, playlist):
        self.clearQueue()
        for _, songName in playlist:
            self.queue.append(songName)
        self.play_song(song)

    def moveNextSong(self):
        index = self.queue.index(self.currentSong)
        if index < len(self.queue):
            match self.queueType:
                case 1:
                    self.play_song(self.queue[index+1])
                case 2:
                    self.play_song(self.queue[random.randint(0, len(self.queue) - 1)])
                case 3:
                    if self.queue.index(self.currentSong) == len(self.queue) - 1:
                        self.play_song(self.queue[0])
                    else :
                        self.play_song(self.queue[index + 1])
                case _:
                    print("Niepoprawny typ kolejki")
        self.main.refreshPlayer()

    def movePreviousSong(self):
        index = self.queue.index(self.currentSong)
        if index > 0:
            self.play_song(self.queue[index-1])
        self.main.refreshPlayer()

    def isInQueue(self,song):
        return song in self.queue

    def deletFromQueue(self,song):
        self.queue.remove(song)

    def deleteIfInQueue(self, song):
        if self.isInQueue(song):
            self.deletFromQueue(song)

    def addNext(self, song):
        addindex = self.queue.index(self.currentSong)
        self.queue.insert(addindex+1, song)

    def addLast(self, song):
        self.queue.append(song)

    def getCurretTime(self):
        if self.isPaused:
            return math.floor(self.currentPauseTime)
        return math.floor(time.time() - self.currentStartTime)

    def getCover(self):
        try:
            full_path = os.path.join(
                self.music_folder,
                self.currentSong
            )
            cover_audio = ID3(full_path)

            apic = cover_audio.getall('APIC')
            if apic:
                img = Image.open(io.BytesIO(apic[0].data))
                return img
        except Exception as e:
            print("Błąd wydobywania okładki : ", e)

        return None

    def getAlbum(self):
        full_path = os.path.join(
            self.music_folder,
            self.currentSong
        )
        audio = ID3(full_path)
        album = audio.get("TALB")
        if album:
            return album.text[0]
        return None

    def getArtist(self):
        full_path = os.path.join(
            self.music_folder,
            self.currentSong
        )
        audio = ID3(full_path)
        artist = audio.get("TPE1")
        if artist:
            return artist.text[0]
        return None

    def pause(self):
        if not self.isPaused:
            pygame.mixer.music.pause()
            self.currentPauseTime = time.time() - self.currentStartTime
            self.isPaused = True
            print("Wstrzymano utwór")
        else :
            print("Utwór jest już zapauzowany")

    def unpause(self):
        if self.isPaused:
            pygame.mixer.music.unpause()
            self.currentStartTime = time.time() - self.currentPauseTime
            self.isPaused = False
            print("Wznowiono utwór")
        else :
            print("Utwór nie jest zapauzowany")

    def stopSong(self):
        pygame.mixer.music.stop()
        self.currentSong = None
        self.isPaused = False
        self.currentSong = 0
        self.currentStartTime = 0

    def changetime(self, newtime):
        pygame.mixer.music.set_pos(newtime)
        self.currentStartTime = time.time() - newtime


    def mute(self):
        self.isMuted = True
        pygame.mixer.music.set_volume(0.0)

    def unmute(self):
        self.isMuted = False
        pygame.mixer.music.set_volume(float(self.volume))

    def changeVolume(self, newvolume):
        if newvolume == 0:
            self.mute()
        else :
            self.isMuted = False
            pygame.mixer.music.set_volume(float(newvolume))
            self.volume = newvolume