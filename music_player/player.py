from pygame import mixer
import os

class Player():
    def __init__(self):
        mixer.init()
        self.__musics_path = ""
        self.__musics = []
        self.__covers = {}
        self.__index = 0
        self.__playing = False
        self.__paused = False

    def load_musics(self, path=""):
        self.__musics_path = path
        self.__musics = list(
            filter(lambda file: ".mp3" in file, os.listdir(self.__musics_path)))
        self.__musics.sort()

    def load_covers(self, path=""):
        try:
            _covers = list(
                filter(lambda file: ".png" in file, os.listdir(path)))

            for _cover in _covers:
                self.__covers[_cover.replace(
                    ".png", ".mp3")] = os.path.join(path, _cover)

        except (FileNotFoundError):
            pass

    def get_current_music(self):
        try:
            return self.__musics[self.__index]

        except (IndexError):
            return "Song Title"

    def get_cover(self, default):
        try:
            return self.__covers[self.get_current_music()]

        except (KeyError):
            return default

    def is_paused(self):
        return self.__paused

    def play(self):
        self.__paused = False

        if not self.__playing:
            self.__playing = True
            mixer.music.load(os.path.join(
                self.__musics_path, self.__musics[self.__index]))
            mixer.music.play(loops=-1)

        else:
            mixer.music.unpause()

    def pause(self):
        self.__paused = True
        mixer.music.pause()

    def previous(self):
        if self.__index > 0:
            self.__index -= 1

        self.__playing = False
        self.play()

    def next(self):
        if self.__index < len(self.__musics) - 1:
            self.__index += 1

        self.__playing = False
        self.play()
