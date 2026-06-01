import sqlite3 as sql

class DB:
    def __init__(self):
        self.con = sql.connect("database.db")
        self.cur = self.con.cursor()

    def createPlaylist(self, playlist_name):
        self.cur.execute("CREATE TABLE IF NOT EXISTS "+playlist_name+" (id INTEGER PRIMARY KEY AUTOINCREMENT, song TEXT)")
        return 1

    def deletePlaylist(self, playlist_name):
        self.cur.execute("DROP TABLE "+playlist_name)
        return 1

    def addToPlaylist(self, playlist_name, song):
        try:
            query = f"INSERT INTO {playlist_name} VALUES (NULL, ?)"
            self.cur.execute(query, (song,))
            self.con.commit()
        except Exception as e:
            print("ERROR:", e)

    def moveUpInPlaylist(self, playlist_name, song_name):
        self.cur.execute(f"SELECT id, song FROM {playlist_name}")
        playlist_order = self.cur.fetchall()

        prev_song_id = None
        prev_song_name = None
        song_id = None

        for row in playlist_order:
            if row[1] == song_name:
                song_id = row[0]
                break
            else :
                prev_song_id = row[0]
                prev_song_name = row[1]

        if song_id is None or song_id == 0:
            return 1
        else :
            self.cur.execute(f"UPDATE {playlist_name} SET song = ? WHERE id = ?", (song_name, prev_song_id))
            self.con.commit()
            self.cur.execute(f"UPDATE {playlist_name} SET song = ? WHERE id = ?", (prev_song_name, song_id))
            self.con.commit()
            return 0

    def moveDownInPlaylist(self, playlist_name, song_name):
        self.cur.execute(f"SELECT id, song FROM {playlist_name}")
        playlist_order = self.cur.fetchall()

        prev_song_id = None
        prev_song_name = None
        song_id = None

        for row in reversed(playlist_order):
            if row[1] == song_name:
                song_id = row[0]
                break
            else :
                prev_song_id = row[0]
                prev_song_name = row[1]

        if song_id is None or prev_song_id is None:
            return 1
        else:
            self.cur.execute(f"UPDATE {playlist_name} SET song = ? WHERE id = ?", (song_name, prev_song_id))
            self.con.commit()
            self.cur.execute(f"UPDATE {playlist_name} SET song = ? WHERE id = ?", (prev_song_name, song_id))
            self.con.commit()
            return 0

    def deleteFromPlaylist(self, playlist_name, song_name):
        self.cur.execute(f"DELETE FROM {playlist_name} WHERE song=?", (song_name,))
        print(f"DELETE FROM {playlist_name} WHERE song={song_name}")

    def getPlaylists(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return self.cur.fetchall()

    def getPlaylistLenght(self, playlist_name):
        self.cur.execute("SELECT COUNT(*) FROM "+playlist_name)
        return self.cur.fetchone()[0]

    def getPlalist(self, playlist_name):
        self.cur.execute("SELECT * FROM "+playlist_name)
        return self.cur.fetchall()