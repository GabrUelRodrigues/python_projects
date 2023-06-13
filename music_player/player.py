import os
from mutagen.mp3 import MP3
from pygame import mixer, error


class Player():
    def __init__(self) -> None:
        mixer.init()
        self.__musics_path: str = ""
        self.__covers_path: str = ""
        self.__musics: list[str] = []
        self.__covers: list[str] = []
        self.__index: int = 0
        self.__playing: bool = False
        self.__paused: bool = False

    def load_musics(self, path="") -> None:
        self.__musics_path = path
        self.__musics = [file for file in os.listdir(self.__musics_path) if file.endswith((".mp3", ".ogg", ".wav"))]

        self.__musics.sort()

    def load_covers(self, path="") -> None:
        self.__covers_path = path
        self.__covers = list(map(lambda song: song[:-4] + ".png", self.__musics))

        self.__covers.sort()

    def get_song_title(self) -> str:
        return self.__musics[self.__index]

    def get_song_length(self) -> int:
        return int(MP3(self.get_music()).info.length)

    def get_playtime(self) -> int:
        return int(mixer.music.get_pos() / 1000)

    def get_music(self) -> str:
        return os.path.join(self.__musics_path, self.__musics[self.__index])

    def get_cover(self) -> str:
        return os.path.join(self.__covers_path, self.__covers[self.__index])

    def is_paused(self) -> bool:
        return self.__paused

    def play(self) -> None:
        self.__paused = False

        if not self.__playing:
            self.__playing = True
            mixer.music.load(self.get_music())
            mixer.music.play()

        else:
            mixer.music.unpause()

    def pause(self) -> None:
        self.__paused = True
        mixer.music.pause()

    def reset(self) -> None:
        self.__playing = False
        self.__index = 0

        try:
            self.play()

        except error:
            self.next()

    def warp_around(self) -> None:
        self.__playing = False
        self.__index = len(self.__musics) - 1

        try:
            self.play()

        except error:
            self.previous()

    def previous(self) -> None:
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

    def next(self) -> None:
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
