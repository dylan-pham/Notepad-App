from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from subprocess import run
import drive

class Notepad():
    def __init__(self):
        self.window = Tk()
        self.window_title = None
        self.window_icon = None
        self.menu_bar = None
        self.status_bar = None
        self.text_box = None
        self.text = None

        self.file_path = None
        self.file_name = None
        self.file_dialog = None

    def update_variables(self):
        try:
            self.file_path = self.file_dialog.name
            self.file_name = self.file_path.split('/')[-1]
            self.window_title = self.window.title(self.file_name)
        except AttributeError:
            pass

    def get_text(self):
        self.text = self.text_box.get('1.0', END)
        self.save_text()

    def save_text(self):
        self.file_dialog = filedialog.asksaveasfile(mode='w')
        self.update_variables()
        if self.file_dialog is not None:
            self.file_dialog.write(self.text)
            self.status_bar['text'] = 'Saved!'
            self.set_status_bar_color('green', 'white')
            self.file_dialog.close()

    def open_file(self):
        self.text_box.delete('1.0', END) # clear textbox before opening new file

        self.file_dialog = filedialog.askopenfile(mode='r')
        self.update_variables()        
        if self.file_dialog is not None:
            self.text_box.insert(INSERT, self.file_dialog.read())
            self.status_bar['text'] = 'Opened!'
            self.set_status_bar_color(bg='green', fg='white')
            self.file_dialog.close()

    def upload_to_drive(self):
        drive.main()
        drive.upload(self.file_name, self.file_path, 'text/txt')
        self.status_bar['text'] = 'Uploaded!'
        self.set_status_bar_color(bg='green', fg='white')

    def confirm_quit(self):
        answer = messagebox.askyesnocancel("Quit?", "Are you sure you want to quit?")
        if answer == True:
            quit()

    def set_status_bar_color(self, bg='black', fg='white'):
        self.status_bar.configure(bg=bg, fg=fg)

    def key(self, event):
        key_pressed = event.char
        if key_pressed == '(':
            self.text_box.insert(INSERT, ')')
        if key_pressed == '[':
            self.text_box.insert(INSERT, ']')
        if key_pressed == '{':
            self.text_box.insert(INSERT, '}')
        if key_pressed == '\"':
            self.text_box.insert(INSERT, '\"')
        if key_pressed == '\'':
            self.text_box.insert(INSERT, '\'')

    def run(self):
        if ".py" in self.file_path:
            command = r"python " + self.file_path
            output = run(command)
        elif ".java" in self.file_path:
            compiler = r"javac " + self.file_path
            run(compiler)
            command = r"java" + self.file_path
            output = run(command)
        else:
            self.status_bar['text'] = 'Unrunnable file'
            self.set_status_bar_color(bg='red', fg='black')

    def create_window(self):
        self.window.geometry('500x500')
        self.window.geometry("+700+250")
        self.window.protocol("WM_DELETE_WINDOW", self.confirm_quit)
        self.window_title = self.window.title('Untitled')
        self.window_icon = self.window.iconbitmap(r'C:\_Code_\Python\Notepad--\pencil.ico')
        self.menu_bar = Menu(self.window)
        self.menu_bar.add_command(label="Open", command=self.open_file)
        self.menu_bar.add_command(label="Save", command=self.get_text)
        self.menu_bar.add_command(label='Save to Drive', command=self.upload_to_drive)
        self.menu_bar.add_command(label='Run', command=self.run)
        self.menu_bar.add_command(label="Quit", command=self.confirm_quit)
        self.window.config(menu=self.menu_bar)
        self.status_bar = Label(self.window, text='', bd=1, relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)
        self.set_status_bar_color()
        self.text_box = Text(self.window, height=500, width=500, tabs=("2c"))
        self.text_box.configure(bg='black')
        self.text_box.configure(fg='white')
        self.text_box.configure(insertbackground="white")
        self.text_box.pack()
        
def main():
    notepad = Notepad()
    notepad.create_window()
    notepad.window.bind("<Key>", notepad.key)
    notepad.window.mainloop()

main()