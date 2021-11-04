from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, Tk, Button, Label, messagebox
import cv2
import numpy as np
import math


StegGB = Tk()
StegGB.configure(background='lavender')
StegGB.title("StegGB")
StegGB.geometry('600x600')

global path_image

image_display_size = 400, 400


def errorMsg():
    # display error message
    error = messagebox.showerror("No image selected", "Please choose an image before encoding/decoding!")


def encodeimage():
    
    global path_image, img_base
    data = txt.get(1.0, "end-1c")
    # load the image
    img = cv2.imread(path_image)

    # break the image into its character level. Represent the characters in ASCII.
    data = [format(ord(i), '08b') for i in data]
    _, width, _ = img.shape
    # encode the image
    PixReq = len(data) * 3

    RowReq = PixReq / width
    RowReq = math.ceil(RowReq)

    count = 0
    charCount = 0
    
    for i in range(RowReq + 1):
       
        while (count < width and charCount < len(data)):
            char = data[charCount]
            charCount += 1
            
            for index_k, k in enumerate(char):
                if ((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (
                        k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                    img[i][count][index_k % 3] -= 1
                if (index_k % 3 == 2):
                    count += 1
                if (index_k == 7):
                    if (charCount * 3 < PixReq and img[i][count][2] % 2 == 1):
                        img[i][count][2] -= 1
                    if (charCount * 3 >= PixReq and img[i][count][2] % 2 == 0):
                        img[i][count][2] -= 1
                    count += 1
        count = 0

    
    # Write the encrypted image into a new file
    cv2.imwrite(enterFilename.get(), img)


def saveFilename():
    global enterFilename, txt, popUp

    try:
       loadImg()

    except(NameError):
        errorMsg()

    else:
        # create a popup window
        popUp = Toplevel(StegGB)
        popUp.geometry("400x400")


        labelEncode = Label(popUp, text="Enter message to encode:")
        labelEncode.place(x=75, y=30)
        # add a text box using tkinter's Text function and place it at (340,55). The text box is of height 165pixels.
        txt = Text(popUp, wrap=WORD, width=30)
        txt.place(x=75, y=55, height=165)

        labelFilename = Label(popUp, text="Enter filename with extension(e.g .jpg/.png/.bmp):")
        labelFilename.place(x=60, y=250)
        enterFilename = Entry(popUp, width=25)
        enterFilename.pack()
        enterFilename.place(x=115, y=275)

        saveFile_button = Button(popUp, text="Save File", bg='white', fg='black', command=confirmMsg)
        saveFile_button.place(x=140, y=320, width=110, height=40)


# def check_empty():
#     if txt.get(1.0, "end-1c"):
#         pass  # your function where you want to jump
#     else:
#         error = messagebox.showerror("No input", "Please input your message before saving the file!")
#         txt.focus_set()
def confirmMsg():
    #validate inputs
    if not txt.get(1.0, "end-1c"):
        error = messagebox.showerror("No input", "Please input your message before saving the file!")
    elif not enterFilename.get():
        error = messagebox.showerror("No input", "Please input your file name before saving the file!")
        txt.focus_set()
    else:
        Confirm = messagebox.askyesno("Confirmation", "Confirm encode text?")
        if Confirm == 1:
            # call the encodeimage() function
            encodeimage()
            messagebox.showinfo("Successful", "Encoded Successfully")
            # to close the 2nd window
            popUp.destroy()

        else:
            messagebox.showinfo("Failed", "Failed to Encode, please try again")


def decodeimage():

    global img_base
    try:
        loadImg()

    except(NameError):
        errorMsg()

    else:

        # decrypt the data from the image
        img = cv2.imread(path_image)
        data = []
        stop = False
        for index_i, i in enumerate(img):
            i.tolist()
            for index_j, j in enumerate(i):
                if (index_j) % 3 == 2:
                    # r
                    data.append(bin(j[0])[-1])
                    # g
                    data.append(bin(j[1])[-1])
                    # b
                    if bin(j[2])[-1] == '1':
                        stop = True
                        break
                else:
                    # r
                    data.append(bin(j[0])[-1])
                    # g
                    data.append(bin(j[1])[-1])
                    # b
                    data.append(bin(j[2])[-1])
            if stop:
                break
        msg = []
        # join all the bits to form letters (ASCII Representation)
        for i in range(int((len(data) + 1) / 8)):
            msg.append(data[i * 8:(i * 8 + 8)])
        # join all the letters to form the message.
        msg = [chr(int(''.join(i), 2)) for i in msg]
        msg = ''.join(msg)

        popUp = Toplevel(StegGB)
        popUp.geometry("300x300")
        labelDecode = Label(popUp, text="The decoded message is:")
        labelDecode.place(x=30, y=30)
        decodedtext = Text(popUp, state='disabled', width=30, height=10)
        decodedtext.place(x=30, y=60)
        decodedtext.configure(state='normal')
        decodedtext.insert('end', msg)
        decodedtext.configure(state='disabled')

        img_base.config(image='')  # clear image

def loadImg():
    global img_base
    # load the image using the path
    load_image = Image.open(path_image)
    # set the image into the GUI using the thumbnail function from tkinter
    load_image.thumbnail(image_display_size, Image.ANTIALIAS)
    # load the image as a numpy array for efficient computation and change the type to unsigned integer
    np_load_image = np.asarray(load_image)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    render = ImageTk.PhotoImage(np_load_image)
    img_base = Label(StegGB, image=render)
    img_base.image = render
    img_base.place(x=90, y=90)

def chooseFile():
    global path_image
    # use the tkinter filedialog library to open the file using a dialog box.
    # obtain the image of the path
    path_image = filedialog.askopenfilename(title='Choose a file',
                                            filetypes=[('PNG files', '.png'), ('JPG files', '.jpg'),
                                                       ('BMP files', '*.bmp')])  # filter types of files
    #load image
    loadImg()

# create a button for calling the function on_click
on_click_button = Button(StegGB, text="Choose Image", bg='white', fg='black', command=chooseFile)
on_click_button.place(x=250, y=20, width=110, height=40)

encode_button = Button(StegGB, text="Encode", bg='white', fg='black', command=saveFilename)
encode_button.place(x=160, y=530, width=110, height=40)
decode_button = Button(StegGB, text="Decode", bg='white', fg='black', command=decodeimage)
decode_button.place(x=340, y=530, width=110, height=40)

StegGB.mainloop()
