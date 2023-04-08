import textwrap
import base64
import os
import json
from io import BytesIO
from PIL import Image
import PySimpleGUI as sg
from player import Player

# region Import images


def load_image(path, size):
    _buffer = BytesIO()
    with Image.open(path) as img:
        img = img.resize(size)
        img.save(_buffer, format="PNG")

        return base64.b64encode(_buffer.getvalue())


def update_song_cover(path):
    try:
        return load_image(path, (200, 200))

    except FileNotFoundError:
        return DEFAULT_COVER

# endregion

# region Save and Load settings


def load_settings():
    try:
        with open("./settings.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return {"musics": "", "covers": ""}


def save_settings(settings):
    with open("./settings.json", "w") as file:
        json.dump(settings, file)

# endregion


# region Setup
BG_COLOR = "#01014c"
DEFAULT_COVER = load_image(os.path.realpath("./images/cover.png"), (200, 200))
PREVIOUS_BUTTON = load_image(
    os.path.realpath("./images/previous.png"), (40, 40))
PLAY_BUTTON = load_image(os.path.realpath("./images/play.png"), (72, 72))
PAUSE_BUTTON = load_image(os.path.realpath("./images/pause.png"), (72, 72))
NEXT_BUTTON = load_image(os.path.realpath("./images/next.png"), (40, 40))

sg.theme("DarkGrey14")
settings = load_settings()
# endregion

# region Settings window


def settings_window():
    layout = [
        [sg.Text("Musics:"), sg.Input(key="-MUSICS-", size=(25, 1),
                                      default_text=settings["musics"]), sg.FolderBrowse(initial_folder="./")],
        [sg.Text("Covers:"), sg.Input(key="-COVERS-", size=(25, 1),
                                      default_text=settings["covers"]), sg.FolderBrowse(initial_folder="./")],
        [sg.Button("Exit"), sg.Button("Accept")]
    ]

    return sg.Window("Settings", layout=layout, finalize=True)
# endregion

# region Player window


def player_window():
    layout = [
        [sg.Canvas(size=(250, 20), background_color=BG_COLOR)],

        [
            sg.Canvas(size=(10, 210), background_color=BG_COLOR),
            sg.Frame(layout=[
                [sg.Image(source=DEFAULT_COVER, key="-SONG_COVER-")]
            ], size=(210, 210), title="", border_width=0, background_color="white"),
            sg.Canvas(size=(10, 210), background_color=BG_COLOR)
        ],

        [sg.Text("Song Title...", background_color=BG_COLOR,
                 font="UbuntuCondensed 12 italic bold", key="-SONG_TITLE-")],
        [sg.Canvas(size=(250, 2), background_color="white")],

        [
            sg.Canvas(size=(25, 64), background_color=BG_COLOR),
            sg.Button(key="-PREV-", image_data=PREVIOUS_BUTTON,
                      button_color=("", BG_COLOR), mouseover_colors=("", "grey"), border_width=0),
            sg.Button(key="-PLAY_PAUSE-", image_data=PLAY_BUTTON,
                      button_color=("", BG_COLOR), mouseover_colors=("", "grey"), border_width=0),
            sg.Button(key="-NEXT-", image_data=NEXT_BUTTON,
                      button_color=("", BG_COLOR), mouseover_colors=("", "grey"), border_width=0),
            sg.Canvas(size=(25, 64), background_color=BG_COLOR)
        ]
    ]

    return sg.Window("Player", background_color=BG_COLOR, layout=layout, finalize=True)
# endregion


# region Event loop
window1, window2 = settings_window(), None
# window2.hide()
player = Player()
song_cover = DEFAULT_COVER

while True:
    window, event, values = sg.read_all_windows()

    # Exit program
    if event == sg.WIN_CLOSED or event == "Exit":
        break

    # Save settings
    elif event == "Accept":
        try:
            player.load_musics(values["-MUSICS-"])
            player.load_covers(values["-COVERS-"])
            window1.close()
            window2 = player_window()
            player.play()
            song_cover = update_song_cover(player.get_cover())

        except FileNotFoundError:
            sg.popup("No musics found!", keep_on_top=True)

        settings["musics"] = values["-MUSICS-"]
        settings["covers"] = values["-COVERS-"]

        save_settings(settings)

    # Play/Pause
    elif event == "-PLAY_PAUSE-":
        if player.is_paused():
            player.play()

        else:
            player.pause()

    # Previous song
    elif event == "-PREV-":
        player.previous()
        song_cover = update_song_cover(player.get_cover())

    # Next song
    elif event == "-NEXT-":
        player.next()
        song_cover = update_song_cover(player.get_cover())

    # Show song title
    _song_title = textwrap.fill(
        player.get_song_title(), width=30, max_lines=1, placeholder="...")
    window2["-SONG_TITLE-"].update(_song_title)

    # Show album cover
    window2["-SONG_COVER-"].update(source=song_cover)

    # Change play button icon
    if player.is_paused():
        window2["-PLAY_PAUSE-"].update(image_data=PLAY_BUTTON)

    else:
        window2["-PLAY_PAUSE-"].update(image_data=PAUSE_BUTTON)

window1.close()
window2.close()
# endregion
