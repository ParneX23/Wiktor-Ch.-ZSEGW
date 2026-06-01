import customtkinter as ctk
import pygame, math
from PIL import Image
from Player import Player
from db import DB

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

pygame.mixer.init()

class MusicPlayer(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("MP3 Player")
        self.geometry("500x600")

        self.MUSIC_FOLDER = r"D:\,ZSEL\4TP\Aplikacje Desktopowe\MusicPlayer\example_songs"

        self.currentNavPage = 0

        self.currentPage = 0
        self.TRACK_LIST_LENGTH = 12

        # tutaj główny panel

        self.mainFrame = ctk.CTkFrame(
            self,
            width=650,
            height=500
        )

        self.db = DB()

        self.player = Player(self, self.MUSIC_FOLDER)
        self.player.load_songs()

        #tutaj będzie navbar i jego przyciski


        def settings():
            setpopup = ctk.CTkToplevel(self)
            setpopup.title("Settings")
            setpopup.geometry("300x150")

            music_folder_entry = ctk.CTkEntry(
                setpopup,
                placeholder_text=self.MUSIC_FOLDER,
                width=100,
            )
            music_folder_entry.pack(pady=15)

            def zmien_folder(nowy_folder):
                self.MUSIC_FOLDER = nowy_folder
                self.player.music_folder = nowy_folder
                self.player.load_songs()
                print("Zmieniono folder muzyki na : "+nowy_folder)
                setpopup.destroy()

            change_btn = ctk.CTkButton(
                setpopup,
                text="Zmień",
                command=lambda: zmien_folder(music_folder_entry.get())
            )
            change_btn.pack(pady=15)

        self.navbar = ctk.CTkFrame(
            self,
            width=650
        )
        self.navbar.pack(pady=15)
        self.navbar.grid_columnconfigure(0, pad=10)
        self.navbar.grid_columnconfigure(1, pad=10)
        self.navbar.grid_columnconfigure(2, pad=10)
        self.navbar.grid_columnconfigure(3, pad=10)
        self.navbar.grid_columnconfigure(4, pad=10)

        self.settings = ctk.CTkButton(
            self.navbar,
            text="⚙",
            width=40,
            command=settings,
        )
        self.settings.grid(row=0, column=0)

        self.nowplayed = ctk.CTkButton(
            self.navbar,
            width=50,
            text="Odtwarzacz",
            command=lambda: self.changePanel(0)
        )
        self.nowplayed.grid(row=0, column=1)

        self.queue = ctk.CTkButton(
            self.navbar,
            width=50,
            text="Kolejka",
            command=lambda: self.changePanel(1)
        )
        self.queue.grid(row=0, column=2)

        self.songs = ctk.CTkButton(
            self.navbar,
            width=50,
            text="Utwory",
            command=lambda: self.changePanel(2)
        )
        self.songs.grid(row=0, column=3)

        self.playlists = ctk.CTkButton(
            self.navbar,
            width=50,
            text="Playlisty",
            command=lambda: self.changePanel(3)
        )
        self.playlists.grid(row=0, column=4)

        self.mainFrame.pack()

        self.changePanel(self.currentNavPage)

    def changePanel(self, number):
        for widget in self.mainFrame.winfo_children():
            widget.destroy()
        match number:
            case 0:
                print("Zmiana panelu na odtwarzacz")
                self.currentNavPage = 0

                # informacje

                def truncate_text(text, max_len=40):
                    text = text[:-4]
                    if len(text) > max_len:
                        return text[:max_len - 3] + "..."
                    return text

                self.infoFrame = ctk.CTkFrame(
                    self.mainFrame,
                    width=650,
                    height=300
                )
                self.infoFrame.grid(row=0, column=0)

                image = Image.open("placeholder.png")
                self.cover = ctk.CTkImage(
                    dark_image=image,
                    size=(200, 200)
                )
                self.cover_label = ctk.CTkLabel(
                    self.infoFrame,
                    text="",
                    image=self.cover
                )
                self.cover_label.pack(side="left")

                self.trackName = ctk.CTkLabel(
                    self.infoFrame,
                    text="Nazwa utworu",
                )
                self.trackName.pack(padx=10, pady=30)

                self.albumName = ctk.CTkLabel(
                    self.infoFrame,
                    text="Nazwa albumu",
                )
                self.albumName.pack(padx=10, pady=10)

                self.artistName = ctk.CTkLabel(
                    self.infoFrame,
                    text="Nazwa artysty",
                )
                self.artistName.pack(padx=10, pady=10)

                if self.player.currentSong != None:
                    self.trackName.configure(text=truncate_text(self.player.currentSong))
                    newImage = self.player.getCover()
                    if newImage != None:
                        self.cover.configure(dark_image=newImage)
                        self.cover.image = newImage
                    newAlbumName = self.player.getAlbum()
                    if newAlbumName != None:
                        self.albumName.configure(text=newAlbumName)
                    newArtistName = self.player.getArtist()
                    if newArtistName != None:
                        self.artistName.configure(text=newArtistName)

                # kontrolki

                self.controlsFrame = ctk.CTkFrame(
                    self.mainFrame,
                    width=650,
                    height=200
                )
                self.controlsFrame.grid(row=1, column=0)

                self.queue_type_btn = ctk.CTkButton(
                    self.controlsFrame,
                    text="→",
                    width=50,
                    command=lambda: nextQueueType()
                )
                self.queue_type_btn.grid(row=0, column=0)

                match self.player.queueType:
                    case 1:
                        self.queue_type_btn.configure(
                            text="→"
                        )
                    case 2:
                        self.queue_type_btn.configure(
                            text="⤮"
                        )
                    case 3:
                        self.queue_type_btn.configure(
                            text="↻"
                        )
                    case _:
                        self.queue_type_btn.configure(
                            text="?"
                        )

                def nextQueueType():
                    self.player.nextQueueType()
                    match self.player.queueType:
                        case 1:
                            self.queue_type_btn.configure(
                                text="→"
                            )
                        case 2:
                            self.queue_type_btn.configure(
                                text="⤮"
                            )
                        case 3:
                            self.queue_type_btn.configure(
                                text="↻"
                            )
                        case _:
                            self.queue_type_btn.configure(
                                text="?"
                            )

                def muteUnmute():
                    if self.player.isMuted and self.player.volume != 0.0:
                        self.player.unmute()
                        self.mute_button.configure(text="🔈")
                    else:
                        self.player.mute()
                        self.mute_button.configure(text="🔇")

                self.mute_button = ctk.CTkButton(
                    self.controlsFrame,
                    text="🔈",
                    width=50,
                    command=lambda: muteUnmute()
                )
                self.mute_button.grid(row=0, column=1)

                self.volume_slider = ctk.CTkSlider(
                    self.controlsFrame,
                    from_=0,
                    to=1,
                    command=self.player.changeVolume
                )
                self.volume_slider.grid(row=0, column=2)

                def playerPrevious():
                    self.player.movePreviousSong()
                    self.refreshPlayer()

                self.player_previous_btn = ctk.CTkButton(
                    self.controlsFrame,
                    text="⏮",
                    width=50,
                    command=lambda: playerPrevious()
                )
                self.player_previous_btn.grid(row=0, column=3)

                def playerNext():
                    self.player.moveNextSong()
                    self.refreshPlayer()

                self.player_next_btn = ctk.CTkButton(
                    self.controlsFrame,
                    text="⏭",
                    width=50,
                    command=lambda: playerNext()
                )
                self.player_next_btn.grid(row=0, column=4)

                self.play_button = ctk.CTkButton(
                    self.controlsFrame,
                    text="▶",
                    command=lambda: pauseUnpause(),
                    width=50
                )
                self.play_button.grid(row=1, column=0)

                self.stop_button = ctk.CTkButton(
                    self.controlsFrame,
                    text="⏹",
                    command=lambda: self.player.stopSong(),
                    width=50
                )
                self.stop_button.grid(row=1, column=1)

                def changeTimeBar(newValue):
                    self.player.changetime(newValue)
                    #self.changePanel(0)

                self.timebar = ctk.CTkSlider(self.controlsFrame, from_=0, to=100, command=changeTimeBar)
                self.timebar.grid(row=1, column=2)

                self.playingtime = ctk.CTkEntry(
                    self.controlsFrame,
                    width=60
                )
                self.playingtime.insert(0, "00:00")
                self.playingtime.configure(state="readonly")
                self.playingtime.grid(row=1, column=4)

                self.songtime = ctk.CTkEntry(
                    self.controlsFrame,
                    width=60
                )
                self.songtime.insert(0, "00:00")
                self.songtime.configure(state="readonly")
                self.songtime.grid(row=1, column=5)

                def pauseUnpause():
                    if self.player.isPaused:
                        self.player.unpause()
                        self.play_button.configure(text="⏸︎")
                    else:
                        self.player.pause()
                        self.play_button.configure(text="▶")

                def setPlayingTime(newtime):
                    self.playingtime.configure(state="normal")
                    self.playingtime.delete(0, "end")

                    self.playingtime.insert(0, "" + str(math.floor(newtime / 60)) + ":" + str(newtime % 60))
                    self.playingtime.configure(state="readonly")

                def setSongTime(newtime):
                    self.songtime.configure(state="normal")
                    self.songtime.delete(0, "end")

                    self.songtime.insert(0, "" + str(math.floor(newtime / 60)) + ":" + str(newtime % 60))
                    self.songtime.configure(state="readonly")

                def setTimeBar():
                    self.timebar.configure(to=self.player.currentLength)

                def update_time():
                    if not self.timebar.winfo_exists():
                        return
                    if not self.player.isPaused and pygame.mixer.music.get_busy():
                        self.timebar.set(self.player.getCurretTime())
                        setPlayingTime(self.player.getCurretTime())
                    self.after(500, update_time)

                if self.player.currentSong != None:
                    if not self.player.isPaused:
                        setTimeBar()
                        update_time()
                        self.play_button.configure(text="⏸︎")
                    setPlayingTime(self.player.getCurretTime())
                    setSongTime(self.player.currentLength)
                    self.volume_slider.set(self.player.volume)
                    if self.player.isMuted:
                        self.mute_button.configure(text="🔇")
                    else :
                        self.mute_button.configure(text="🔈")


            case 1:
                print("Zmiana panelu na kolejkę")
                self.currentNavPage = 1
                self.queueFrame = ctk.CTkFrame(
                    self.mainFrame,
                    height=400,
                    width=650,
                )
                self.queueFrame.grid(row=0, column=0)
                self.controlsFrame = ctk.CTkFrame(
                    self.mainFrame,
                    width=650,
                    height=100,
                )
                self.controlsFrame.grid(row=1, column=0)
                self.rows = []
                for i in range(self.TRACK_LIST_LENGTH):
                    row = ctk.CTkFrame(self.queueFrame)
                    row.pack(fill="x", padx=5, pady=5)

                    button = ctk.CTkButton(row, text="", anchor="w")
                    button.pack(side="left", fill="x", expand=True)

                    delete_btn = ctk.CTkButton(row, text="🗑", width=30)
                    delete_btn.pack(side="right")

                    move_down_btn = ctk.CTkButton(row, text="▼", width=30)
                    move_down_btn.pack(side="right")

                    move_up_btn = ctk.CTkButton(row, text="▲", width=30)
                    move_up_btn.pack(side="right")

                    self.rows.append({
                        "frame": row,
                        "song_btn": button,
                        "delete_btn": delete_btn,
                        "move_down_btn": move_down_btn,
                        "move_up_btn": move_up_btn,
                    })
                self.currentQueuePage = 0
                self.queueBtnJumpLeft = ctk.CTkButton(
                    self.controlsFrame,
                    text="⏮",
                    width=50,
                    command=lambda: loadPage(0)
                )
                self.queueBtnJumpLeft.grid(row=0, column=0)
                self.queueBtnGoLeft = ctk.CTkButton(
                    self.controlsFrame,
                    text="◀",
                    width=50,
                    command=lambda: loadPage(self.currentQueuePage - 1)
                )
                self.queueBtnGoLeft.grid(row=0, column=1)
                self.currentQueuePageLabel = ctk.CTkLabel(
                    self.controlsFrame,
                    text=str(self.currentQueuePage),
                    width=50
                )
                self.currentQueuePageLabel.grid(row=0, column=2)
                self.queueBtnGoRight = ctk.CTkButton(
                    self.controlsFrame,
                    text="▶",
                    width=50,
                    command=lambda: loadPage(self.currentQueuePage + 1)
                )
                self.queueBtnGoRight.grid(row=0, column=3)
                def jumpRight():
                    loadPage(math.ceil(len(self.player.queue) / self.TRACK_LIST_LENGTH)-1)
                self.queueBtnJumpRight = ctk.CTkButton(
                    self.controlsFrame,
                    text="⏭",
                    width=50,
                    command=lambda: jumpRight()
                )
                self.queueBtnJumpRight.grid(row=0, column=4)
                def delete_song(song):
                    movequeueindex = self.player.queue.index(song)
                    if song is not self.player.currentSong:
                        del self.player.queue[movequeueindex]
                        loadPage(self.currentQueuePage)
                    else :
                        if movequeueindex != 0:
                            self.player.moveNextSong()
                            del self.player.queue[movequeueindex]
                            loadPage(self.currentQueuePage)
                        else :
                            self.player.stopSong()
                            loadPage(self.currentQueuePage)

                def moveup(song):
                    movequeueindex = self.player.queue.index(song)
                    if movequeueindex > 0:
                        self.player.queue[movequeueindex], self.player.queue[movequeueindex - 1] = self.player.queue[movequeueindex - 1], self.player.queue[movequeueindex]
                        loadPage(self.currentQueuePage)

                def movedown(song):
                    movequeueindex = self.player.queue.index(song)
                    if movequeueindex < len(self.player.queue) - 1:
                        self.player.queue[movequeueindex], self.player.queue[movequeueindex + 1] = self.player.queue[movequeueindex + 1], self.player.queue[movequeueindex]
                        loadPage(self.currentQueuePage)

                def loadPage(page):
                    if page >= 0 and page <= (math.ceil(len(self.player.queue) / self.TRACK_LIST_LENGTH)-1):
                        print("Zmiana strony kolejki na "+str(page))
                        self.currentQueuePage = page
                        self.currentQueuePageLabel.configure(text=str(self.currentQueuePage))

                    start = self.currentQueuePage * self.TRACK_LIST_LENGTH
                    for i, row in enumerate(self.rows):
                        song_index = start + i

                        def truncate_text(text, max_len=40):
                            if len(text) > max_len:
                                return text[:max_len - 3] + "..."
                            return text

                        if song_index < len(self.player.queue):
                            song = self.player.queue[song_index]

                            row["song_btn"].configure(
                                text=truncate_text(song),
                                command=lambda s=song: self.player.play_song(s),
                                fg_color="#9F9FDF"
                            )

                            if song == self.player.currentSong:
                                row["song_btn"].configure(
                                    text=truncate_text(song),
                                    command=lambda s=song: self.player.play_song(s),
                                    fg_color="#9A4FDB",
                                )

                            row["delete_btn"].configure(
                                command=lambda s=song: delete_song(s)
                            )

                            row["move_down_btn"].configure(
                                command=lambda s=song: movedown(s)
                            )

                            row["move_up_btn"].configure(
                                command=lambda s=song: moveup(s)
                            )
                        else :
                            row["song_btn"].configure(
                                text=" ",
                                fg_color="#9F9FDF"
                            )

                if self.player.currentSong is None:
                    loadPage(self.currentQueuePage)
                else :
                    queueindex = self.player.queue.index(self.player.currentSong)
                    loadPage(math.floor(queueindex/self.TRACK_LIST_LENGTH))

            #
            #   Panel Utwory
            #

            case 2:
                print("Zmiana panelu na utwory")
                self.currentNavPage = 2
                self.songsFrame = ctk.CTkFrame(
                    self.mainFrame,
                    height=400,
                    width=650,
                )
                self.songsFrame.grid(row=0, column=0)
                self.controlsFrame = ctk.CTkFrame(
                    self.mainFrame,
                    width=650,
                    height=100,
                )
                self.controlsFrame.grid(row=1, column=0)
                self.rows = []
                for i in range(self.TRACK_LIST_LENGTH):
                    row = ctk.CTkFrame(self.songsFrame)
                    row.pack(fill="x", padx=5, pady=5)

                    button = ctk.CTkButton(row, text="", anchor="w")
                    button.pack(side="left", fill="x", expand=True)

                    add_last_btn = ctk.CTkButton(row, text="⏭+", width=30)
                    add_last_btn.pack(side="right")

                    add_next_btn = ctk.CTkButton(row, text="⏮+", width=30)
                    add_next_btn.pack(side="right")


                    add_playlist_btn = ctk.CTkButton(row, text="📋+", width=30)
                    add_playlist_btn.pack(side="right")

                    self.rows.append({
                        "frame": row,
                        "song_btn": button,
                        "add_playlist_btn": add_playlist_btn,
                        "add_last_btn": add_last_btn,
                        "add_next_btn": add_next_btn,
                    })

                self.btnJumpLeft = ctk.CTkButton(
                    self.controlsFrame,
                    text="⏮",
                    width=50,
                    command=lambda: loadPage(0)
                )
                self.btnJumpLeft.grid(row=0, column=0)
                self.btnGoLeft = ctk.CTkButton(
                    self.controlsFrame,
                    text="◀",
                    width=50,
                    command=lambda: loadPage(self.currentPage-1)
                )
                self.btnGoLeft.grid(row=0, column=1)
                self.currentPageLabel = ctk.CTkLabel(
                    self.controlsFrame,
                    text=str(self.currentPage),
                    width=50
                )
                self.currentPageLabel.grid(row=0, column=2)
                self.btnGoRight = ctk.CTkButton(
                    self.controlsFrame,
                    text="▶",
                    width=50,
                    command=lambda: loadPage(self.currentPage + 1)
                )
                self.btnGoRight.grid(row=0, column=3)

                def play_song(song):
                    if self.player.currentSong is not None:
                        self.player.addAndPlay(song)
                    else :
                        self.player.play_song(song)

                def add_next(song):
                    self.player.deleteIfInQueue(song)
                    self.player.addNext(song)

                def add_last(song):
                    self.player.deleteIfInQueue(song)
                    self.player.addLast(song)

                def add_to_playlist(song):
                    popup = ctk.CTkToplevel(self)
                    popup.title("Dodaj '"+song+"' do playlisty")
                    popup.geometry("300x150")

                    rows = self.db.getPlaylists()

                    playlists2 = []

                    for row in rows:
                        if row[0] not in ('SONGS', 'sqlite_sequence'):
                           playlists2.append(row[0])

                    playlistsList = ctk.CTkOptionMenu(
                        popup,
                        values=playlists2
                    )
                    playlistsList.grid(row=0, column=1)

                    def addSongToPlaylist(playlist_name, thesong):
                        print("Próbujemy dodać "+thesong+" do playlisty "+playlist_name)
                        self.db.addToPlaylist(playlist_name, thesong)
                        popup.destroy()

                    add_to_playlist_box_btn = ctk.CTkButton(
                        popup,
                        text="+",
                        command=lambda: addSongToPlaylist(playlistsList.get(), song)
                    )
                    add_to_playlist_box_btn.grid(row=0, column=2)

                def loadPage(page):
                    if page >= 0 and page <= (math.ceil(len(self.player.songs) / self.TRACK_LIST_LENGTH)-1):
                        print("Zmiana strony na "+str(page))
                        self.currentPage = page
                        self.currentPageLabel.configure(text=str(self.currentPage))

                    start = self.currentPage * self.TRACK_LIST_LENGTH
                    for i, row in enumerate(self.rows):
                        song_index = start + i

                        def truncate_text(text, max_len=40):
                            if len(text) > max_len:
                                return text[:max_len - 3] + "..."
                            return text

                        if song_index < len(self.player.songs):
                            song = self.player.songs[song_index]

                            row["song_btn"].configure(
                                text=truncate_text(song),
                                command=lambda s=song: play_song(s)
                            )

                            row["add_playlist_btn"].configure(
                                command=lambda s=song: add_to_playlist(s)
                            )

                            row["add_next_btn"].configure(
                                command=lambda s=song: add_next(s)
                            )

                            row["add_last_btn"].configure(
                                command=lambda s=song: add_last(s)
                            )
                        else :
                            row["song_btn"].configure(
                                text=" "
                            )

                loadPage(self.currentPage)

                def jumpRight():
                    if len(self.player.songs) % self.TRACK_LIST_LENGTH == 0:
                        loadPage(math.floor(len(self.player.songs) / self.TRACK_LIST_LENGTH))
                    else:
                        loadPage(math.floor(len(self.player.songs) / self.TRACK_LIST_LENGTH))

                self.btnJumpRight = ctk.CTkButton(
                    self.controlsFrame,
                    text="⏭",
                    width=50,
                    command=lambda: jumpRight()
                )
                self.btnJumpRight.grid(row=0, column=4)

            #
            #   Panel Playlisty
            #

            case 3:
                print("Zmiana panelu na playlisty")
                self.currentNavPage = 3

                #   Kontrolki

                self.playlists = []

                rows = self.db.getPlaylists()

                for row in rows:
                    if row[0] not in ('SONGS','sqlite_sequence'):
                        self.playlists.append(row[0])

                print(self.playlists)

                self.mainControlsFrame = ctk.CTkFrame(
                    self.mainFrame,
                    width=650,
                    height=100,
                )
                self.mainControlsFrame.grid(row=0, column=0)

                self.playlistsList = ctk.CTkOptionMenu(
                    self.mainControlsFrame,
                    values=self.playlists,
                )
                self.playlistsList.grid(row=0, column=1)

                def createNewPlaylist():
                    popup = ctk.CTkToplevel(self)
                    popup.title("Nowa playlista")
                    popup.geometry("300x150")

                    name_entry = ctk.CTkEntry(
                        popup,
                        placeholder_text="Nazwa playlisty"
                    )
                    name_entry.pack(pady=20)

                    def createNew():
                        self.db.createPlaylist(name_entry.get())
                        popup.destroy()

                    create_btn = ctk.CTkButton(
                        popup,
                        text="Utwórz",
                        command=createNew
                    )
                    create_btn.pack(pady=10)

                self.create_new_btn = ctk.CTkButton(
                    self.mainControlsFrame,
                    text="+",
                    width=50,
                    command=lambda: createNewPlaylist()
                )
                self.create_new_btn.grid(row=0, column=2)

                def deletePlaylist(name):
                    popup = ctk.CTkToplevel(self)
                    popup.title("Usuń playlistę")
                    popup.geometry("300x150")

                    info_label = ctk.CTkLabel(
                        popup,
                        text = "Na pewno chcesz usunąć playlistę '"+name+"'?",
                    )
                    info_label.pack(pady=20)

                    def delete():
                        self.db.deletePlaylist(name)
                        popup.destroy()

                    delete_btn = ctk.CTkButton(
                        popup,
                        text="Tak",
                        command=delete()
                    )
                    delete_btn.pack(pady=10)

                self.delete_playlist_btn = ctk.CTkButton(
                    self.mainControlsFrame,
                    text="🗑",
                    width=50,
                    command=lambda: deletePlaylist(self.playlistsList.get())
                )
                self.delete_playlist_btn.grid(row=0, column=3)

                self.songsFrame = ctk.CTkFrame(
                    self.mainFrame,
                    width=650,
                    height=400,
                )
                self.songsFrame.grid(row=1, column=0)

                self.songsControlsFrame = ctk.CTkFrame(
                    self.mainFrame,
                    width=650,
                    height=100,
                )
                self.songsControlsFrame.grid(row=2, column=0)

                self.rows = []
                for i in range(self.TRACK_LIST_LENGTH):
                    row = ctk.CTkFrame(self.songsFrame)
                    row.pack(fill="x", padx=5, pady=5)

                    button = ctk.CTkButton(row, text="", anchor="w")
                    button.pack(side="left", fill="x", expand=True)

                    delete_btn = ctk.CTkButton(row, text="🗑", width=30)
                    delete_btn.pack(side="right")

                    move_down_btn = ctk.CTkButton(row, text="▼", width=30)
                    move_down_btn.pack(side="right")

                    move_up_btn = ctk.CTkButton(row, text="▲", width=30)
                    move_up_btn.pack(side="right")

                    self.rows.append({
                        "frame": row,
                        "song_btn": button,
                        "delete_btn": delete_btn,
                        "move_down_btn": move_down_btn,
                        "move_up_btn": move_up_btn,
                    })
                self.currentPlaylistsPage = 0
                self.playlistsBtnJumpLeft = ctk.CTkButton(
                    self.songsControlsFrame,
                    text="⏮",
                    width=50,
                    command=lambda: loadPlaylistPage(0)
                )
                self.playlistsBtnJumpLeft.grid(row=0, column=0)
                self.playlistsBtnGoLeft = ctk.CTkButton(
                    self.songsControlsFrame,
                    text="◀",
                    width=50,
                    command=lambda: loadPlaylistPage(self.currentPlaylistsPage - 1)
                )
                self.playlistsBtnGoLeft.grid(row=0, column=1)
                self.currentPlaylistsPageLabel = ctk.CTkLabel(
                    self.songsControlsFrame,
                    text=str(self.currentPlaylistsPage),
                    width=50
                )
                self.currentPlaylistsPageLabel.grid(row=0, column=2)
                self.playlistsBtnGoRight = ctk.CTkButton(
                    self.songsControlsFrame,
                    text="▶",
                    width=50,
                    command=lambda: loadPlaylistPage(self.currentPlaylistsPage + 1)
                )
                self.playlistsBtnGoRight.grid(row=0, column=3)

                def jumpRight():
                    loadPlaylistPage(math.ceil(self.db.getPlaylistLenght(self.playlistsList.get()) / self.TRACK_LIST_LENGTH)-1)

                self.playlistsBtnJumpRight = ctk.CTkButton(
                    self.songsControlsFrame,
                    text="⏭",
                    width=50,
                    command=lambda: jumpRight()
                )
                self.playlistsBtnJumpRight.grid(row=0, column=4)

                def playlist_delete_song(song):
                    self.db.deleteFromPlaylist(self.playlistsList.get(), song)
                    loadPlaylistPage(self.currentPlaylistsPage)

                def moveup(song):
                    self.db.moveUpInPlaylist(self.playlistsList.get(), song)
                    loadPlaylistPage(self.currentPlaylistsPage)

                def movedown(song):
                    self.db.moveDownInPlaylist(self.playlistsList.get(), song)
                    loadPlaylistPage(self.currentPlaylistsPage)

                def loadPlaylistPage(page):
                    thisPlaylistName = self.playlistsList.get()
                    thisPlaylistLength = self.db.getPlaylistLenght(thisPlaylistName)
                    self.thisPlaylistSongs = self.db.getPlalist(thisPlaylistName)

                    if page >= 0 and page <= (math.ceil(thisPlaylistLength / self.TRACK_LIST_LENGTH))-1:
                        print("Zmiana strony playlisty na " + str(page))
                        self.currentPlaylistsPage = page
                        self.currentPlaylistsPageLabel.configure(text=str(self.currentPlaylistsPage))

                    start = self.currentPlaylistsPage * self.TRACK_LIST_LENGTH
                    for i, row in enumerate(self.rows):
                        song_index = start + i

                        def truncate_text(text, max_len=40):
                            if len(text) > max_len:
                                return text[:max_len - 3] + "..."
                            return text

                        if song_index < thisPlaylistLength:
                            song = self.thisPlaylistSongs[song_index][1]

                            row["song_btn"].configure(
                                text=truncate_text(song),
                                command=lambda s=song: self.player.playFromPlaylist(s, self.thisPlaylistSongs),
                                text_color="black",
                                fg_color="#B1DEDA"
                            )

                            row["delete_btn"].configure(
                                command=lambda s=song: playlist_delete_song(s)
                            )

                            row["move_down_btn"].configure(
                                command=lambda s=song: movedown(s)
                            )

                            row["move_up_btn"].configure(
                                command=lambda s=song: moveup(s)
                            )
                        else:
                            row["song_btn"].configure(
                                text=" ",
                                fg_color="#B1DEDA"
                            )

                self.playlistsList.configure(
                    command=lambda value: loadPlaylistPage(0)
                )

                loadPlaylistPage(0)

            case _:
                print("Niepoprawny panel")

    def refreshPlayer(self):
        def truncate_text(text, max_len=40):
            text = text[:-4]
            if len(text) > max_len:
                return text[:max_len - 3] + "..."
            return text
        print(self.currentNavPage)
        if self.currentNavPage == 0:
            if self.player.currentSong != None:
                self.trackName.configure(text=truncate_text(self.player.currentSong))
                newImage = self.player.getCover()
                if newImage != None:
                    self.cover.configure(dark_image=newImage)
                    self.cover.image = newImage
                newAlbumName = self.player.getAlbum()
                if newAlbumName != None:
                    self.albumName.configure(text=newAlbumName)
                newArtistName = self.player.getArtist()
                if newArtistName != None:
                    self.artistName.configure(text=newArtistName)

        match self.player.queueType:
            case 1:
                self.queue_type_btn.configure(
                    text="→"
                )
            case 2:
                self.queue_type_btn.configure(
                    text="⤮"
                )
            case 3:
                self.queue_type_btn.configure(
                    text="↻"
                )
            case _:
                self.queue_type_btn.configure(
                    text="?"
                )


app = MusicPlayer()
app.mainloop()