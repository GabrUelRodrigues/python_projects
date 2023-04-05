import textwrap
import base64
import os
import json
from io import BytesIO
from PIL import Image
import PySimpleGUI as sg
from player import Player

BG_COLOR = "#01014c"
DEFAULT_COVER = os.path.realpath("./images/cover.png")
PREVIOUS_BUTTON = os.path.realpath("./images/previous.png")
PLAY_BUTTON = os.path.realpath("./images/play.png")
PAUSE_BUTTON = os.path.realpath("./images/pause.png")
NEXT_BUTTON = os.path.realpath("./images/next.png")

# region Import images as Base64


def load_image(path, size=()):
    _buffer = BytesIO()
    with Image.open(path) as img:
        img = img.resize(size)
        img.save(_buffer, format="PNG")

        return base64.b64encode(_buffer.getvalue())

# endregion

# region Save and Load settings


def load_settings():
    try:
        with open("./settings.json", "r") as file:
            return json.load(file)

    except (FileNotFoundError):
        return {"musics": "", "covers": ""}


def save_settings(settings):
    with open("./settings.json", "w") as file:
        json.dump(settings, file)

# endregion


# region Setup
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
                [sg.Image(source=load_image(DEFAULT_COVER,
                                            (200, 200)), key="-SONG_COVER-")]
            ], size=(210, 210), title="", border_width=0, background_color="white"),
            sg.Canvas(size=(10, 210), background_color=BG_COLOR)
        ],

        [sg.Text("Song Title...", background_color=BG_COLOR,
                 font="UbuntuCondensed 12 italic bold", key="-SONG_TITLE-")],
        [sg.Canvas(size=(250, 2), background_color="white")],

        [
            sg.Canvas(size=(25, 64), background_color=BG_COLOR),
            sg.Button(key="-PREV-", image_data=load_image(PREVIOUS_BUTTON, (40, 40)),
                      button_color=("", BG_COLOR), mouseover_colors=("", "grey"), border_width=0),
            sg.Button(key="-PLAY_PAUSE-", image_data=load_image(PLAY_BUTTON, (72, 72)),
                      button_color=("", BG_COLOR), mouseover_colors=("", "grey"), border_width=0),
            sg.Button(key="-NEXT-", image_data=load_image(NEXT_BUTTON, (40, 40)),
                      button_color=("", BG_COLOR), mouseover_colors=("", "grey"), border_width=0),
            sg.Canvas(size=(25, 64), background_color=BG_COLOR)
        ]
    ]

    return sg.Window("Player", background_color=BG_COLOR, layout=layout, finalize=True)
# endregion


# region Event loop
window1, window2 = settings_window(), player_window()
window2.hide()
player = Player()

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
            window2.un_hide()
            player.play()

        except (FileNotFoundError):
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

    # Next song
    elif event == "-NEXT-":
        player.next()

    # Show song title
    _song_title = textwrap.fill(
        player.get_current_music(), width=30, max_lines=1, placeholder="...")
    window2["-SONG_TITLE-"].update(_song_title)

    # Show album cover
    try:
        window2["-SONG_COVER-"].update(source=load_image(
            player.get_cover(default=DEFAULT_COVER), (200, 200)))

    except (FileNotFoundError):
        window2["-SONG_COVER-"].update(
            source=load_image(DEFAULT_COVER, (200, 200)))

    # Change play button icon
    if player.is_paused():
        window2["-PLAY_PAUSE-"].update(
            image_data=load_image(PLAY_BUTTON, (72, 72)))

    else:
        window2["-PLAY_PAUSE-"].update(
            image_data=load_image(PAUSE_BUTTON, (72, 72)))

window1.close()
window2.close()
# endregion
