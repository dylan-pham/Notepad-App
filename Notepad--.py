from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import drive

class Notepad():
    def __init__(self):
        self.window = Tk()
        self.windowTitle = None
        self.windowIcon = None
        self.menuBar = None
        self.statusBar = None
        self.textBox = None
        self.text = None

        self.filePath = None
        self.fileName = None
        self.fileDialog = None

    def updateVariables(self):
        try:
            self.filePath = self.fileDialog.name
            self.fileName = self.filePath.split('/')[-1]
            self.windowTitle = self.window.windowTitle(self.fileName)
        except AttributeError:
            pass

    def getText(self):
        self.text = self.textBox.get('1.0', END)
        self.saveText()

    def saveText(self):
        self.fileDialog = filedialog.asksaveasfile(mode='w')
        self.updateVariables()
        if self.fileDialog is not None:
            self.fileDialog.write(self.text)
            self.statusBar['text'] = 'Saved!'
            self.changeSBColor()
            self.fileDialog.close()

    def openFile(self):
        self.textBox.delete('1.0', END) # clear textbox before opening new file

        self.fileDialog = filedialog.askopenfile(mode='r')
        self.updateVariables()        
        if self.fileDialog is not None:
            self.textBox.insert(INSERT, self.fileDialog.read())
            self.statusBar['text'] = 'Opened!'
            self.changeSBColor()
            self.fileDialog.close()

    def uploadToDrive(self):
        drive.main()
        drive.upload(self.fileName, self.filePath, 'text/txt')
        self.statusBar['text'] = 'Uploaded!'
        self.changeSBColor()

    def confirmQuit(self):
        answer = messagebox.askyesnocancel("Are you sure you want to quit?", "Continue Editing?")
        if answer == True:
            pass
        else:
            quit()

    def changeSBColor(self):
        self.statusBar.configure(bg='green', fg='white')

    def createWindow(self):
        self.window.geometry('500x500')
        self.windowTitle = self.window.title('Untitled')
        self.windowIcon = self.window.iconbitmap(r'C:\_Code_\Python\Notepad--\pencil.ico')
        self.menuBar = Menu(self.window)
        self.menuBar.add_command(label="Open", command=self.openFile)
        self.menuBar.add_command(label="Save", command=self.getText)
        self.menuBar.add_command(label='Save to Drive', command=self.uploadToDrive)
        self.menuBar.add_command(label="Quit", command=self.confirmQuit)
        self.window.config(menu=self.menuBar)
        self.statusBar = Label(self.window, text='', bd=1, relief=SUNKEN, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)
        self.statusBar.configure(bg='black', fg='white')
        self.textBox = Text(self.window, height=500, width=500)
        self.textBox.configure(bg='black')
        self.textBox.configure(fg='white')
        self.textBox.configure(insertbackground="white")
        self.textBox.pack()
        
def main():
    notepad = Notepad()
    notepad.createWindow()
    notepad.window.mainloop()

main()