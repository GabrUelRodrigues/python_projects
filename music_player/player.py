import os
from mutagen.mp3 import MP3
from pygame import mixer, error


class Player():
    def __init__(self):
        mixer.init()
        self.__musics_path = ""
        self.__covers_path = ""
        self.__musics = []
        self.__covers = []
        self.__index = 0
        self.__playing = False
        self.__paused = False

    def load_musics(self, path=""):
        self.__musics_path = path
        self.__musics = list(
            filter(lambda file: ".mp3" in file, os.listdir(self.__musics_path)))

        self.__musics.sort()

    def load_covers(self, path=""):
        self.__covers_path = path
        self.__covers = list(
            map(lambda song: song.replace(".mp3", ".png"), self.__musics))

        self.__covers.sort()

    def get_song_title(self):
        return self.__musics[self.__index]

    def get_song_length(self):
        return int(MP3(self.get_music()).info.length)

    def get_playtime(self):
        return int(mixer.music.get_pos() / 1000)

    def get_music(self):
        return os.path.join(self.__musics_path, self.__musics[self.__index])

    def get_cover(self):
        return os.path.join(self.__covers_path, self.__covers[self.__index])

    def is_paused(self):
        return self.__paused

    def play(self):
        self.__paused = False

        if not self.__playing:
            self.__playing = True
            mixer.music.load(self.get_music())
            mixer.music.play()

        else:
            mixer.music.unpause()

    def pause(self):
        self.__paused = True
        mixer.music.pause()

    def reset(self):
        self.__playing = False
        self.__index = 0

        try:
            self.play()

        except error:
            self.next()

    def warp_around(self):
        self.__playing = False
        self.__index = len(self.__musics) - 1

        try:
            self.play()

        except error:
            self.previous()

    def previous(self):
        self.__playing = False

        if self.__index > 0:
            self.__index -= 1

            try:
                self.play()

            except error:
                if self.__index == 0:
                    self.warp_around()

                else:
                    self.previous()

        else:
            self.warp_around()

    def next(self):
        self.__playing = False

        if self.__index < len(self.__musics) - 1:
            self.__index += 1

            try:
                self.play()

            except error:
                if self.__index >= len(self.__musics) - 1:
                    self.reset()

                else:
                    self.next()

        else:
            self.reset()
