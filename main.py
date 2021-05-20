# img_viewer.py

import PySimpleGUI as sg
import os.path
import PIL.Image
import base64
import random
import io


def sortByNum(e):
    return int(e.split(".")[0])


def convert_to_bytes(file_or_byte, resize=None):
    if isinstance(file_or_byte, str):
        img = PIL.Image.open(file_or_byte)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_byte)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_byte)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height / cur_height, new_width / cur_width)
        img = img.resize((int(cur_width * scale), int(cur_height * scale)), PIL.Image.ANTIALIAS)
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()


def getMeaning(fname, filename):
    filename = os.path.join(
        folder, fname
    )
    textFileName = filename.split(".jpg")
    textFileName[0] += ".txt"
    desc = open("Meaning/" + textFileName[0][6:], "r")
    lines = desc.readlines()
    meaning = fname + "\n\nUpright: \n" + lines[0] + "\nReversed: \n" + lines[1]
    if lines[1].endswith("\n"):
        meaning += "\nAdditional meanings: \n" + str(lines[2])
        if lines[2].endswith("\n"):
            meaning += "\nReversed: \n" + str(lines[3])
    return meaning


# First the window layout in 2 columns


file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
    [sg.Text("Resize to"), sg.In(key='-W-', size=(5, 1)), sg.In(key='-H-', size=(5, 1))]
]

# For now will only show the name of the file that was chosen

image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    # [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

image_description_column = [
    [sg.Text("description here")],
    # [sg.Text(size=(20, None), key="-CNAME-")],
    [sg.Text(size=(40, None), key="-TOUT-")],
]

# ----- Full layout -----

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
        sg.VSeperator(),
        sg.Column(image_description_column),
        sg.VSeperator(),
        sg.Button("Draw card", key="-DRAW-")
    ]
]

window = sg.Window("Tarot", layout, finalize=True)

# Get the list of images in the cards folder
folder = "cards"
try:
    file_list = os.listdir(folder)
except:
    file_list = []
fnames = [f
          for f in file_list
          if os.path.isfile(os.path.join(folder, f))
          and f.lower().endswith((".png", ".gif", ".jpg"))
          ]
fnames.sort(key=sortByNum)
window["-FILE LIST-"].update(fnames)

# run the event loop
while True:

    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "-FILE LIST-":  # A file was chosen from the listbox

        fname = values["-FILE LIST-"][0]
        filename = os.path.join(
            folder, fname
        )

        if values['-W-'] and values['-H-']:
            new_size = int(values['-W-']), int(values['-H-'])
        else:
            new_size = None
        if new_size is None:
            new_size = (300, 300)

    elif event == "-DRAW-":
        rand = random.randint(0, 77)
        fname = fnames[rand]
        filename = os.path.join(
            folder, fname
        )

        if values['-W-'] and values['-H-']:
            new_size = int(values['-W-']), int(values['-H-'])
        else:
            new_size = None
        if new_size is None:
            new_size = (300, 300)

        rand = random.randint(0, 1)
        if rand == 0:
            img = PIL.Image.open(filename)
            img = PIL.Image.Image.transpose(img, PIL.Image.FLIP_TOP_BOTTOM)
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            filename = bio.getvalue()

    meaning = getMeaning(fname, filename)
    window["-TOUT-"].update(meaning)

    window["-IMAGE-"].update(data=convert_to_bytes(filename, resize=new_size))

window.close()
# Press the green button in the gutter to run the script.
# if __name__ == '__main__':


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# https://realpython.com/pysimplegui-python/
# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Image_Elem_Image_Viewer_PIL_Based.py
# https://www.tarotcardmeanings.net/tarotcards.htm

# add button to draw card
# add description for each card
# add image rotation for drawn cards
# get tarot images and a working search bar
