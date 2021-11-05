from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, Tk, Button, Label, messagebox
import cv2
import numpy as np
import math

# create GUI
StegGB = Tk()
# GUI background color
StegGB.configure(background='#ADD8E6')
# GUI title
StegGB.title("StegGB")
# GUI size
StegGB.geometry('600x600')
# GUI cannot resize
StegGB.resizable(width=False, height=False)

# disable the cross button
def disable_xbtn():
   pass


StegGB.protocol("WM_DELETE_WINDOW", disable_xbtn)

# display image size on GUI
image_size = 400, 400

# function to load the image when using the choose image button
def loadImg():
    global img_base

    # load the image using the path
    load_image = Image.open(path_image)

    # set the image into the GUI using the thumbnail function from tkinter
    load_image.thumbnail(image_size, Image.ANTIALIAS)
    # load the image as a numpy array for efficient computation and change the type to unsigned integer
    np_load_image = np.asarray(load_image)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    render = ImageTk.PhotoImage(np_load_image)
    img_base = Label(StegGB, image=render, anchor=CENTER)
    img_base.image = render
    img_base.place(x=90, y=90)


def chooseFile():

    global path_image

    # use the tkinter filedialog library to obtain the image of the path
    path_image = filedialog.askopenfilename(title='Choose a file',
                                            filetypes=[('PNG files', '.png'), ('JPG files', '.jpg'),
                                                       ('BMP files', '*.bmp')])  # filter types of files
    # load image
    loadImg()

# function to display error message
def errorMsg():
    # display error message when no image is selected
    error = messagebox.showerror("No image selected", "Please choose an image before encoding/decoding!")

# function to encode message in popup
def encodeImg():
    global enterFilename, encodeTxt, popUp

    try:
        # If user click encode button before uploading image, show error message
       loadImg()

    except NameError:
        errorMsg()

    else:
        # c# create a pop up window to show encode message
        popUp = Toplevel(StegGB)
        popUp.geometry("400x400")
        popUp.title("Encode")
        popUp.resizable(width=False, height=False)

        labelEncode = Label(popUp, text="Enter message to encode:")
        labelEncode.place(x=75, y=30)
        # create a text box for users to input message to encode
        encodeTxt = Text(popUp, wrap=WORD, width=25, font=("Helvetica", 15))
        encodeTxt.place(x=75, y=55, height=165)

        labelFilename = Label(popUp, text="Enter filename with extension(e.g .jpg/.png/.bmp):")
        labelFilename.place(x=60, y=250)
        enterFilename = Entry(popUp, width=25, font=("Helvetica", 15))
        enterFilename.pack()
        enterFilename.place(x=60, y=275)

        # save file button will go to confirmMsg function
        saveFile_button = Button(popUp, text="Save File", bg='white', fg='black', command=confirmMsg)
        saveFile_button.place(x=140, y=320, width=110, height=40)

# function to encode image
def encodeAlg():

    global path_image, img_base

    # store the secret message into 'secretMsg'
    secretMsg = encodeTxt.get(1.0, "end-1c")
    # load the image
    img = cv2.imread(path_image)
    # convert message into array of ASCII
    secretMsg = [format(ord(i), '08b') for i in secretMsg]
    _, widImg, _ = img.shape

    # encode image
    # Calculate number of pixels = length of the array of ASCII from secretMsg * 3
    noPix = len(secretMsg) * 3

    noRow = noPix / widImg
    noRow = math.ceil(noRow)

    count = 0
    charCount = 0
    # passing through the image in row-wise
    for i in range(noRow + 1):

        while count < widImg and charCount < len(secretMsg):
            char = secretMsg[charCount]
            charCount += 1

            for index_k, k in enumerate(char):
                # if the bit is 1 and pixel is even number, minus 1
                if ((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (
                        k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                    img[i][count][index_k % 3] -= 1
                # count the number of letters
                if index_k % 3 == 2:
                    count += 1
                # if the index equals 7, check is there any character
                if index_k == 7:
                    # if there is character, make the end of file bit to 0
                    if charCount * 3 < noPix and img[i][count][2] % 2 == 1:
                        img[i][count][2] -= 1
                    if charCount * 3 >= noPix and img[i][count][2] % 2 == 0:
                        img[i][count][2] -= 1
                    # if there is no character, make it as 1
                    count += 1
        count = 0

        # Write the encoded image into a new file - get filename input from users
        cv2.imwrite(enterFilename.get(), img)




def confirmMsg():
    # validate message and filename inputs
    if not encodeTxt.get(1.0, "end-1c"):
        error = messagebox.showerror("No input", "Please input your message before saving the file!")
    elif not enterFilename.get():
        error = messagebox.showerror("No input", "Please input your file name before saving the file!")
        encodeTxt.focus_set()
    else:
        # when input both message and filename, will ask to confirm message
        Confirm = messagebox.askyesno("Confirmation", "Confirm encode text and save file name?")
        if Confirm == 1:
            # call the encodeImage() function
            encodeAlg()
            messagebox.showinfo("Successful", "Encoded Successfully")
            # to close the 2nd window
            popUp.destroy()

        else:
            messagebox.showinfo("Failed", "Failed to Encode, please try again")


def decodeImage():

    global img_base

    try:
        # If user click decode button before uploading image, show error message
        loadImg()

    except NameError:
        errorMsg()

    else:

        # decrypt secretMsg from the image
        img = cv2.imread(path_image)

        # convert image into numpy array
        secretMsg = []
        stop = False

        for index_i, i in enumerate(img):
            i.tolist()
            # check whether reach the end of file character
            for index_j, j in enumerate(i):
                if index_j % 3 == 2:
                    # r pixel
                    secretMsg.append(bin(j[0])[-1])
                    # g pixel
                    secretMsg.append(bin(j[1])[-1])
                    # b pixel
                    if bin(j[2])[-1] == '1':
                        stop = True
                        break
                else:
                    # r pixel
                    secretMsg.append(bin(j[0])[-1])
                    # g pixel
                    secretMsg.append(bin(j[1])[-1])
                    # b pixel
                    secretMsg.append(bin(j[2])[-1])
            if stop:
                break
        decodeMsg = []
        # combine all the ASCII bits to form letters
        for i in range(int((len(secretMsg) + 1) / 8)):
            decodeMsg.append(secretMsg[i * 8:(i * 8 + 8)])
        # join all the letters to form the message
        decodeMsg = [chr(int(''.join(i), 2)) for i in decodeMsg]
        decodeMsg = ''.join(decodeMsg)
        # message_label = Label(StegGB, text=decodeMsg, bg='lavender', font=("Times New Roman", 10))
        # message_label.place(x=30, y=400)
        # create a pop up window to show decoded message
        popUp = Toplevel(StegGB)
        popUp.geometry("300x300")
        popUp.title("Decode")
        popUp.resizable(width=False, height=False)
        # a textbox to display decoded message - disabled textbox
        labelDecode = Label(popUp, text="The decoded message is:")
        labelDecode.place(x=30, y=30)
        decodedtext = Text(popUp, state='disabled', width=30, height=10)
        decodedtext.place(x=30, y=60)
        decodedtext.configure(state='normal')
        decodedtext.insert('end', decodeMsg)
        decodedtext.configure(state='disabled')

        img_base.config(image='')  # clear image


def ExitApp():
    ExitBox = messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application', icon='warning')
    if ExitBox == 'yes':
        StegGB.destroy()
    else:
        messagebox.showinfo('Return', 'You will now return to the application screen')


exitbutton = Button(StegGB, text='Exit', command=ExitApp, bg='red', fg = 'black')
exitbutton.place(x=500, y=20, width=60, height=40)

# button to choose image file
chooseImage = Button(StegGB, text="Choose Image", bg='white', fg='black', command=chooseFile)
chooseImage.place(x=250, y=20, width=110, height=40)

# button to encode message and save file name
encode_button = Button(StegGB, text="Encode", bg='white', fg='black', command=encodeImg)
encode_button.place(x=160, y=530, width=110, height=40)

# button to decode image
decode_button = Button(StegGB, text="Decode", bg='white', fg='black', command=decodeImage)
decode_button.place(x=340, y=530, width=110, height=40)

StegGB.mainloop()
