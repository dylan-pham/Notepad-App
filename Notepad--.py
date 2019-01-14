from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import drive

class Notepad():
    def __init__(self):
        self.window = Tk()
        self.window_title = None
        self.winodw_icon = None
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
            self.window_title = self.window.window_title(self.file_name)
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
            self.change_status_bar_color()
            self.file_dialog.close()

    def open_file(self):
        self.text_box.delete('1.0', END) # clear textbox before opening new file

        self.file_dialog = filedialog.askopenfile(mode='r')
        self.update_variables()        
        if self.file_dialog is not None:
            self.text_box.insert(INSERT, self.file_dialog.read())
            self.status_bar['text'] = 'Opened!'
            self.change_status_bar_color()
            self.file_dialog.close()

    def upload_to_drive(self):
        drive.main()
        drive.upload(self.file_name, self.file_path, 'text/txt')
        self.status_bar['text'] = 'Uploaded!'
        self.change_status_bar_color()

    def confirm_quit(self):
        answer = messagebox.askyesnocancel("Are you sure you want to quit?", "Continue Editing?")
        if answer == True:
            pass
        else:
            quit()

    def change_status_bar_color(self):
        self.status_bar.configure(bg='green', fg='white')

    def create_window(self):
        self.window.geometry('500x500')
        self.window_title = self.window.title('Untitled')
        self.winodw_icon = self.window.iconbitmap(r'C:\_Code_\Python\Notepad--\pencil.ico')
        self.menu_bar = Menu(self.window)
        self.menu_bar.add_command(label="Open", command=self.open_file)
        self.menu_bar.add_command(label="Save", command=self.get_text)
        self.menu_bar.add_command(label='Save to Drive', command=self.upload_to_drive)
        self.menu_bar.add_command(label="Quit", command=self.confirm_quit)
        self.window.config(menu=self.menu_bar)
        self.status_bar = Label(self.window, text='', bd=1, relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)
        self.status_bar.configure(bg='black', fg='white')
        self.text_box = Text(self.window, height=500, width=500)
        self.text_box.configure(bg='black')
        self.text_box.configure(fg='white')
        self.text_box.configure(insertbackground="white")
        self.text_box.pack()
        
def main():
    notepad = Notepad()
    notepad.create_window()
    notepad.window.mainloop()

main()