# Copyright ©️ 2023 Sanila Ranatunga. All Rights Reserved

import base64
import os.path
import datetime
import pyperclip
import webbrowser
import tkinter.font
from tkinter import *
from tkinter import filedialog, messagebox, colorchooser, scrolledtext
from tkinter.ttk import Combobox


def date_time():
    a = datetime.datetime.now()
    textArea.insert(END, a.strftime("%H:%M %m/%d/%Y"))


def save_as(event=None):
    global file_save
    file_save = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=(
                                                 ("Text documents (*.txt)", ".txt"),
                                                 ("All files", "*.*")
                                             ))
    if file_save is None:
        return
    fileText = str(textArea.get(1.0, END))
    with open(file_save, "w") as file:
        file.write(fileText)


def save(event=None):
    try:
        with open(file_save, "w", encoding="utf-8") as file:
            file.write(textArea.get(1.0, END))
    except NameError:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(
            ("Text documents", ".txt"),
            ("All Files", "*.*")
        ))
        if not file_path:
            return


def on_close():
    text = textArea.get("1.0", END)
    try:
        with open(file_save, "r") as file:
            if text != file.read():
                print("Not equal")
                result = messagebox.askyesnocancel("Notepad", "Do you want to save changes to the file?")
                if result:
                    save()
                elif result is None:
                    return
                elif result is False:
                    window.destroy()
            else:
                window.destroy()
    except NameError:
        if len(text) == 1:
            window.destroy()
        else:
            result = messagebox.askyesnocancel("Notepad", "Do you want to save changes to the file?")
            if result:
                save()
            elif result is None:
                return
            elif result is False:
                window.destroy()
    except FileNotFoundError:
        window.destroy()


def open_(event=None):
    global opened_filepath
    if len(textArea.get(1.0, END)) > 1:
        question = messagebox.askyesno(message="Do you want to save this file before opening?")
        if question:
            save()
        elif not question:
            try:
                opened_filepath = filedialog.askopenfilename(defaultextension=".txt",
                                                             filetypes=(
                                                                 ("Text documents (*.txt)", ".txt"),
                                                                 ("All Files", "*.*")
                                                             ))
                opened_file = open(opened_filepath, encoding="utf-8")
                textArea.delete(1.0, END)
                textArea.insert(0.0, opened_file.read())
                window.title("Notepad ●" + os.path.basename(opened_filepath))
            except UnicodeError:
                with open(opened_filepath, "rb") as binary_file:
                    textArea.insert(0.0, base64.b64encode(binary_file).decode(opened_file.encoding))
                messagebox.showinfo(title="Unsupported file", message="Unsupported file, unable to open",
                                    icon="warning")
            except FileNotFoundError as e:
                pass
    else:
        try:
            opened_filepath = filedialog.askopenfilename(defaultextension=".txt",
                                                         filetypes=(
                                                             ("Text documents (*.txt)", ".txt"),
                                                             ("All Files", "*.*")
                                                         ))
            opened_file = open(opened_filepath, encoding="utf-8")
            textArea.insert(0.0, opened_file.read())
            window.title("Notepad ●" + os.path.basename(opened_filepath))
            row, col = textArea.index(INSERT).split(".")
            status_label.config(text=f"Line {row}, Column {col}     {opened_file.encoding.capitalize()}")
        except FileNotFoundError:
            pass
        except UnicodeError:
            with open(opened_filepath, "rb") as binary_file:
                textArea.insert(0.0, base64.b64encode(binary_file).decode(opened_file.encoding))
            messagebox.showinfo(title="Unable to open", message=f"Unsupported file type!")


def copy_text(event=None):
    try:
        first_selected_index = textArea.index("sel.first")
        last_selected_index = textArea.index("sel.last")
        text_need_copy = textArea.get(first_selected_index, last_selected_index)
        pyperclip.copy(text_need_copy)
    except TclError:
        pass


def undo(event=None):
    try:
        textArea.edit_undo()
    except TclError:
        pass


def redo(event=None):
    try:
        textArea.edit_redo()
    except TclError:
        pass


def paste_text():
    textArea.insert(1.0, textArea.clipboard_get)


def cut_text(event=None):
    text_copy = textArea.get(1.0, END)
    pyperclip.copy(text_copy)
    textArea.delete(1.0, END)


def select_all(event):
    textArea.tag_add(SEL, 1.0, END)
    return "break"


def select_all_c():
    textArea.tag_add(SEL, 1.0, END)
    return "break"


def github_button():
    url = "https://github.com/sanila2007/tkinter-notepad"
    webbrowser.open(url=url)


def issue_button():
    url = "https://github.com/sanila2007/tkinter-notepad/issues/new"
    webbrowser.open(url=url)


## Notepad about window --
def about_notepad():
    about_window = Toplevel()
    about_window.title("About Notepad")
    about_window.geometry("440x400")
    about_window.resizable(False, False)
    about_window.attributes("-toolwindow", True)
    about_window.attributes("-topmost", True)

    about_window.resized_photo = PhotoImage(file="images/resized_logo.png")
    about_window.issue_photo = PhotoImage(file="images/problem-report.png")
    about_window.source_code_image = PhotoImage(file="images/programming-code-signs.png")
    Label(about_window, image=about_window.resized_photo, justify="center", text=" Notepad Application", compound=LEFT,
          font=(None, 12)).pack(anchor=NW, padx=10, pady=5)
    notepad_text = scrolledtext.ScrolledText(about_window, wrap=WORD,
                                             width=49,
                                             height=12, padx=5, pady=25)
    notepad_text.pack()
    notepad_text.insert(INSERT, "Application Information----------------\n\n"
                                "Version:        0.2.0\n"
                                "License:        GNU General Public License v3.0\n"
                                "Developer:      Sanila Ranatunga\n\n\n"
                                "© 2023 Sanila Ranatunga. \nAll rights reserved.")
    notepad_text.configure(state="disabled")

    Button(about_window, text=" Source Code",image=about_window.source_code_image, compound=LEFT, command=github_button, font=(None, 10)).pack(pady=10)
    Button(about_window, text=" Report an issue", font=(None, 10), image=about_window.issue_photo, compound=LEFT, command=issue_button).pack()


## Window
window = Tk()
FONT_SIZE = 15
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("1200x650")
window.title("Notepad")

icon = PhotoImage(file="images/notepad_icon.png")
window.iconphoto(True, icon)

scrollbar = Scrollbar(window, width=20)
scrollbar.pack(side=RIGHT, fill=Y)

current_font = 'Consolas'
current_font_size = 15


## Font style and font size combo box ------------------------------
def font_style(event):
    global current_font
    try:
        current_font = selected_combo_font.get()
        textArea.config(font=(current_font, current_font_size))
    except NameError:
        pass


def font_size(event):
    global current_font_size
    try:
        current_font_size = int(selected_combo_font_size.get())
        textArea.config(font=(current_font, current_font_size))
    except NameError:
        pass


font_list = [
    "Arial",
    "Calibri",
    "Cambria",
    "Century Gothic",
    "Comic Sans MS",
    "Consolas",
    "Courier New",
    "Franklin Gothic Medium",
    "Garamond",
    "Georgia",
    "Impact",
    "Lucida Sans Unicode",
    "Palatino Linotype",
    "Segoe Print",
    "Segoe Script",
    "Segoe UI",
    "Symbol",
    "Tahoma",
    "Times New Roman",
    "Trebuchet MS",
    "Verdana",
    "Webdings",
    "Wingdings",
    "Yu Gothic",
    "Noto Sans",
    "Open Sans",
    "Roboto",
    "Lato",
    "Source Sans Pro",
    "Montserrat",
    "Roboto Slab",
    "Playfair Display",
    "Oswald",
    "Raleway",
    "Merriweather",
    "PT Serif",
    "Libre Baskerville",
    "Ubuntu",
    "Fira Sans",
    "Poppins",
    "Muli",
    "Montserrat Alternates",
    "Quicksand",
    "Cabin",
    "Alegreya",
    "Exo 2",
    "Nunito",
    "Work Sans",
    "Bebas Neue"
]

## Combo box - Font style
selected_combo_font = StringVar()
fontComboBox = Combobox(window,
                        values=[
                            "Arial",
                            "Calibri",
                            "Cambria",
                            "Century Gothic",
                            "Comic Sans MS",
                            "Consolas",
                            "Courier New",
                            "Franklin Gothic Medium",
                            "Garamond",
                            "Georgia",
                            "Impact",
                            "Lucida Sans Unicode",
                            "Palatino Linotype",
                            "Segoe Print",
                            "Segoe Script",
                            "Segoe UI",
                            "Symbol",
                            "Tahoma",
                            "Times New Roman",
                            "Trebuchet MS",
                            "Verdana",
                            "Webdings",
                            "Wingdings",
                            "Yu Gothic",
                            "Noto Sans",
                            "Open Sans",
                            "Roboto",
                            "Lato",
                            "Source Sans Pro",
                            "Montserrat",
                            "Roboto Slab",
                            "Playfair Display",
                            "Oswald",
                            "Raleway",
                            "Merriweather",
                            "PT Serif",
                            "Libre Baskerville",
                            "Ubuntu",
                            "Fira Sans",
                            "Poppins",
                            "Muli",
                            "Montserrat Alternates",
                            "Quicksand",
                            "Cabin",
                            "Alegreya",
                            "Exo 2",
                            "Nunito",
                            "Work Sans",
                            "Bebas Neue"
                        ],
                        textvariable=selected_combo_font, height=20, width=25)
fontComboBox.pack(anchor=NW, side=TOP, padx=5, pady=5)
fontComboBox.current(5)


def typed_font_in_combo_box(event):
    current_font = fontComboBox.get()
    textArea.config(font=(current_font, current_font_size))


fontComboBox.bind("<Return>", typed_font_in_combo_box)

## Combo box- Font size
selected_combo_font_size = StringVar()
fontSizeCb = Combobox(window,
                      values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
                      textvariable=selected_combo_font_size, height=22, width=25)
fontSizeCb.current(16)
fontSizeCb.pack(anchor=NW, padx=5, pady=5)
fontComboBox.bind('<<ComboboxSelected>>', font_style)
fontSizeCb.bind('<<ComboboxSelected>>', font_size)


def typed_font_size(event):
    current_font_size = fontSizeCb.get()
    if int(current_font_size) > 100 or int(current_font_size) == 0 or int(current_font_size) is None:
        pass
    else:
        textArea.config(font=(current_font, current_font_size))


fontSizeCb.bind("<Key>", typed_font_size)


## ----------------------------------


## Make text bold
def bold(event=None):
    font_text = tkinter.font.Font(font=textArea["font"])
    if font_text.actual()["weight"] == "normal":
        textArea.configure(font=(current_font, current_font_size, "bold"))
    elif font_text.actual()["weight"] == "bold":
        textArea.configure(font=(current_font, current_font_size))


## Make text italic
def italic(event=None):
    font_text = tkinter.font.Font(font=textArea["font"])
    if font_text.actual(["slant"] == "roman"):
        textArea.config(font=(current_font, current_font_size, "italic"))
    elif font_text.actual()["slant"] == "italic":
        textArea.config(font=(current_font, current_font_size, "normal"))


## Underline text
def underline(event=None):
    font_text = tkinter.font.Font(font=textArea["font"])
    if font_text.actual()["underline"] == 0:
        textArea.config(font=(current_font, current_font_size, "underline"))
    elif font_text.actual()["underline"] == 1:
        textArea.config(font=(current_font, current_font_size, "normal"))


## Change the colour of the texts
def font_colour():
    colour = colorchooser.askcolor()
    colourHex = colour[1]
    textArea.config(fg=colourHex)
    if colour is None:
        return


def leftAlign():
    text = textArea.get(1.0, END)
    textArea.tag_config("left", justify="left")
    textArea.delete(1.0, END)
    textArea.insert(INSERT, text, "left")


def rightAlign():
    text = textArea.get(1.0, END)
    textArea.tag_config("right", justify="right")
    textArea.delete(1.0, END)
    textArea.insert(INSERT, text, "right")


def centerAlign():
    text = textArea.get(1.0, END)
    textArea.tag_config("center", justify="center")
    textArea.delete(1.0, END)
    textArea.insert(INSERT, text, "center")


# Find & Replace window
def find_win():
    global find_query, replace_query, replace_button
    find_window = Toplevel()
    find_window.geometry("400x100")
    find_window.title("Find & Replace")
    find_window.resizable(False, False)
    find_window.attributes("-topmost", True)
    find_window.attributes("-toolwindow", True)

    find_window.search_image = PhotoImage(file="images/search.png")
    Label(find_window, text="Find").grid(row=1, column=1, padx=5, pady=5)
    find_query = Entry(find_window)
    find_query.grid(row=1, column=2, padx=5)
    Button(find_window, image=find_window.search_image, activebackground="light gray", command=find).grid(row=1,
                                                                                                          column=3)

    Label(find_window, text="Replace").grid(row=2, column=1, padx=5, pady=5)
    replace_query = Entry(find_window)
    replace_query.grid(row=2, column=2, padx=5)
    replace_button = Button(find_window, text="Replace", activebackground="light gray", command=replace, state=DISABLED)
    replace_button.grid(row=2, column=3)

    Label(find_window, text="Close the window to get the results*", wraplength=400, font=(None, 10)).grid(row=3,
                                                                                                          column=2)


def find():
    textArea.tag_remove("find", 1.0, END)
    word = find_query.get()
    textArea.tag_remove('match', '1.0', END)
    matches = 0
    if word:
        start_pos = '1.0'
        while True:
            start_pos = textArea.search(word, start_pos, stopindex=END)
            if (not start_pos):
                break
            end_pos = f'{start_pos}+{len(word)}c'
            textArea.tag_add("find", start_pos, end_pos)
            matches += 1
            start_pos = end_pos
            textArea.tag_config("find", foreground="red")
            replace_button.configure(state=ACTIVE)
    else:
        messagebox.showinfo(message="Nothing found on your query " + word)


def replace():
    replace_word = replace_query.get()
    find_word = find_query.get()
    text = textArea.get(1.0, END)
    new_text = text.replace(find_word, replace_word)
    textArea.delete(1.0, END)
    textArea.insert(1.0, new_text)


## Satus bar ---------------------------------------
def update_status(event):
    row, col = textArea.index(INSERT).split(".")
    status_label.config(text="Line {}, Column {}".format(row, col))


status_label = Label(window, text="Line 1, Column 1", justify="left", font=(None, 12), width=width, height=2,
                     background="#1E1E1E", foreground="#e0e0e0")
status_label.pack(side=BOTTOM)


## Status bar end -----------------------------------


## Theme function (Dark mode & light mode)
def theme():
    if lightmode.get() is not False:
        ## -- Text are --
        textArea.config(bg="#474747", font=("Consolas", 20), fg="#D3D3D3", insertbackground="#D3D3D3")
        window.config(bg="#212121")
        ## --Menu bar --
        editMenu.config(bg="#2C2C2C", fg="#F5F5F5", activeforeground="#F5F5F5", activebackground="#0078D7")
        fileMenu.config(bg="#2C2C2C", fg="#F5F5F5", activeforeground="#F5F5F5", activebackground="#0078D7")
        viewMenu.config(bg="#2C2C2C", fg="#F5F5F5", foreground="#F5F5F5", activeforeground="#F5F5F5",
                        activebackground="#0078D7")
        paragraphMenu.config(bg="#2C2C2C", fg="#F5F5F5", foreground="#F5F5F5", activeforeground="#F5F5F5",
                             activebackground="#0078D7")
        helpMenu.config(bg="#2C2C2C", fg="#F5F5F5", foreground="#F5F5F5", activeforeground="#F5F5F5",
                        activebackground="#0078D7")
    elif lightmode.get() is False:
        textArea.config(bg="#F5F5F5", font=("Consolas", 20), insertbackground="black", fg="black")
        editMenu.config(bg="#F0F0F0", fg="black", activebackground="#0078D7")
        fileMenu.config(bg="#F0F0F0", fg="black", activebackground="#0078D7")
        viewMenu.config(bg="#F0F0F0", fg="black", activebackground="#0078D7")
        paragraphMenu.config(bg="#F0F0F0", fg="black", activebackground="#0078D7")
        helpMenu.config(bg="#F0F0F0", fg="black", activebackground="#0078D7")
        window.config(bg="#F0F0F0")


# ---------------- MENU BAR -----------------------

## menu bar
menubar = Menu(window)
window.config(menu=menubar)

## File menu ----------------------
fileMenu = Menu(menubar, tearoff=0, font=(None, "15"), relief=SOLID)
menubar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Open", accelerator="Ctrl+O", command=open_)
fileMenu.add_command(label="Save", accelerator="Ctrl+S", command=save)
fileMenu.add_command(label="Save as", accelerator="Ctrl+Shift+S", command=save_as)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=on_close)

## Edit menu -----------------------
editMenu = Menu(menubar, tearoff=0, font=(None, "15"), relief=SOLID)
menubar.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Cut", command=cut_text, accelerator="Ctrl+X", state=DISABLED)
editMenu.add_command(label="Copy", command=copy_text, accelerator="Ctrl+C", state=DISABLED)
editMenu.add_command(label="Paste", command=paste_text, accelerator="Ctrl+V")
editMenu.add_command(label="Undo", command=undo)
editMenu.add_command(label="Redo", command=redo)
editMenu.add_command(label="Select all", command=select_all_c, accelerator="Ctrl+A")
editMenu.add_separator()
editMenu.add_command(label="Bold", command=bold, accelerator="Ctrl+B")
editMenu.add_command(label="Italic", command=italic, accelerator="Ctrl+I")
editMenu.add_command(label="Underline", command=underline, accelerator="Ctrl+U")
editMenu.add_separator()
editMenu.add_command(label="Find & Replace", command=find_win)
editMenu.add_separator()
editMenu.add_command(label="Date/Time", command=date_time)
editMenu.add_separator()
editMenu.add_command(label="Font colour", command=font_colour)

## Paragraph menu ------------------------
paragraphMenu = Menu(menubar, tearoff=0, font=(None, "15"), relief=SOLID)
menubar.add_cascade(label="Paragraph", menu=paragraphMenu)
paragraphMenu.add_command(label="Left Align", command=leftAlign)
paragraphMenu.add_command(label="Right Align", command=rightAlign)
paragraphMenu.add_command(label="Center", command=centerAlign)

## View menu ------------------------------
lightmode = BooleanVar()
viewMenu = Menu(menubar, tearoff=0, font=(None, "15"), relief=SOLID)
menubar.add_cascade(label="View", menu=viewMenu)
viewMenu.add_checkbutton(label="Dark mode", onvalue=1, offvalue=0, variable=lightmode, command=theme)

## Help menu ---------------------------
helpMenu = Menu(menubar, tearoff=0, font=(None, "15"), relief=SOLID)
menubar.add_cascade(label="Help", menu=helpMenu)
helpMenu.add_command(label="About Notepad", command=about_notepad)

## Text Area-----------------------
textArea = Text(window, font=("Consolas", 20), width=width, height=height, pady=15, padx=15,
                yscrollcommand=scrollbar.set, wrap=WORD, undo=True)
textArea.pack()
scrollbar.config(command=textArea.yview)

## Short cut keys -------------
textArea.bind("<KeyRelease>", update_status)
textArea.bind("<Button-1>", update_status)
textArea.bind("<Control-a>", select_all)
textArea.bind("<Control-c>", copy_text)
window.bind("<Control-s>", save)
textArea.bind("<Control-x>", cut_text)
window.bind("<Control-o>", open_)
window.bind("<Control-Shift-s>", save_as)
textArea.bind("<Control-z>", undo)
textArea.bind("<Control-b>", bold)
textArea.bind("<Control-i>", italic)
textArea.bind("<Control-u>", underline)


def update_command_states(event=None):
    if textArea.tag_ranges("sel"):
        editMenu.entryconfig("Copy", state="normal")
        editMenu.entryconfig("Cut", state="normal")
    else:
        editMenu.entryconfig("Copy", state="disabled")
        editMenu.entryconfig("Cut", state="disabled")


textArea.bind("<KeyRelease>", update_command_states)
textArea.bind("<ButtonRelease>", update_command_states)

window.protocol("WM_DELETE_WINDOW", on_close)

window.mainloop()
