# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog
from tkinter import messagebox

# import swapper functions
from app import ass_swap_text as st

# import sys exit
from sys import exit


# variables
inputFile = ''
translateFile = ''
outputFile = ''


# select input file
def browseInputFile():
    global inputFile
    inputFile = filedialog.askopenfilename(
                                           title="Select a File",
                                           filetypes=[("ASS file", "*.ass")])

    # Change label contents
    label_input_file_select.configure(text="File Opened: "+inputFile)
    text_output_file.insert('end', inputFile[:-4]+'_modified.ass')


# select translate file
def browseTlFile():
    global translateFile
    translateFile = filedialog.askopenfilename(
                                               title="Select a File",
                                               filetypes=[("TXT or SRT file", "*.txt *srt")])

    # Change label contents
    label_tl_file_select.configure(text="File Opened: "+translateFile)


# validating inputs
def validateInputs():
    return st.verify_file_type(inputFile, ".ass") and \
        st.verify_file_type(translateFile, (".srt", ".txt")) and \
        st.verify_file_type(outputFile, ".ass")


# translate selected files
def translate():
    global outputFile
    outputFile = text_output_file.get()
    if (validateInputs()):
        st.translate_files(inputFile, translateFile, outputFile)
        messagebox.showinfo("Success!", "Translate completed!")
    else:
        messagebox.showinfo("Warning", "Please check all inputs are filled in")


# Create the root window
window = Tk()

# Set window title
window.title('ASS Translator')

# labels
label_input_file_select = Label(window,
                                width=100,
                                text="Input File (.ass)",
                                fg="black")

label_tl_file_select = Label(window,
                             width=100,
                             text="Translate File (.txt|.srt)",
                             fg="black")

label_output_file_name = Label(window,
                               text="Output Filename",
                               fg="black")

# buttons
button_input_file = Button(window,
                           text="Select Input File",
                           command=browseInputFile)

button_tl_file = Button(window,
                        text="Select Output File",
                        command=browseTlFile)

button_translate = Button(window,
                          text="Translate",
                          command=translate)

button_exit = Button(window,
                     text="Exit",
                     command=exit)

# text entry
text_output_file = Entry(
    window,
)

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_input_file_select.grid(column=1, row=1, sticky='nesw',
                             padx=10, pady=10, ipadx=5, ipady=5)
label_tl_file_select.grid(column=1, row=2, sticky='nesw',
                          padx=10, pady=10, ipadx=5, ipady=5)

button_input_file.grid(column=0, row=1, sticky='nesw',
                       padx=10, pady=10, ipadx=5, ipady=5)
button_tl_file.grid(column=0, row=2, sticky='nesw',
                    padx=10, pady=10, ipadx=5, ipady=5)

label_output_file_name.grid(column=0, row=3, sticky='nesw', pady=10)
text_output_file.grid(column=1, row=3, sticky='nesw', pady=10, padx=10)

button_translate.grid(column=1, row=4, sticky='nesw',
                      padx=10, pady=10, ipadx=5, ipady=5)
button_exit.grid(column=0, row=4, sticky='nesw',
                 padx=10, pady=10, ipadx=5, ipady=5)

# Let the window wait for any events
window.mainloop()
