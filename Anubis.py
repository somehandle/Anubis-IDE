#############      author => Anubis Graduation Team        ############
#############      this project is part of my graduation project and it intends to make a fully functioned IDE from scratch    ########

import sys
import glob

import Python_Coloring
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pathlib import Path

# Display to use for the window
# Only relevent on multi-screen setups
display_monitor = 0

class Signal(QObject):
    # initializing a Signal which will take (string) as an input
    reading = pyqtSignal(str)
    def __init__(self):
        QObject.__init__(self)

App = 0
class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        global App 
        App = self
        App.setDarkTheme()
        win = Window()
        sys.exit(self.exec_())

    def setDarkTheme(self):
        style = "./editor/colorscheme/dark.qss"

        file = QFile(style)
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.setStyleSheet(stream.readAll())

    def setLightTheme(self):
        style = "./editor/colorscheme/light.qss"

        file = QFile(style)
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.setStyleSheet(stream.readAll())


# Making text editor as A global variable (to solve the issue of being local to (self) in widget class)
text2 = QTextEdit

# this class is made to connect the QTab with the necessary layouts
class TextBuffer(QWidget):
    def __init__(self, path):
        super().__init__()

        # Layout
        hbox = QHBoxLayout()
        self.setLayout(hbox)

        # Contents
        self.data = QTextEdit()
        hbox.addWidget(self.data)

        # Open file
        f = open(path, 'r')
        self.setText(f.read())

        # Extra operations (Syntax Highlighting)
        Python_Coloring.PythonHighlighter(self.data)

    def setText(self, newText):
        self.data.setText(newText)

class Editor(QWidget):
    def __init__(self):
        super().__init__()
        self.tabsList = QTabWidget()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tabsList)
        self.setLayout(self.layout)
        self.buffers = {}

    def openBuffer(self, name, path):
        self.buffers[name] = TextBuffer(path)
        self.tabsList.addTab(self.buffers[name], name)
        self.activeBuffer = self.buffers[name]

    def getActiveBuffer(self):
        return self.activeBuffer


class Layout(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # This widget is responsible of making Tab in IDE which makes the Text editor looks nice
        self.editor = Editor()

        # second editor in which the error messeges and succeeded connections will be shown
        global text2
        text2 = QTextEdit()
        text2.setReadOnly(True)
        # defining a Treeview variable to use it in showing the directory included files
        self.treeview = QTreeView()

        # making a variable (path) and setting it to the root path (surely I can set it to whatever the root I want, not the default)
        #path = QDir.rootPath()

        path = QDir.currentPath()

        # making a Filesystem variable, setting its root path and applying somefilters (which I need) on it
        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(QDir.rootPath())

        # NoDotAndDotDot => Do not list the special entries "." and "..".
        # AllDirs =>List all directories; i.e. don't apply the filters to directory names.
        # Files => List files.
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        self.treeview.setModel(self.dirModel)
        self.treeview.setRootIndex(self.dirModel.index(path))
        self.treeview.clicked.connect(self.on_clicked)

        vbox = QVBoxLayout()
        Left_hbox = QHBoxLayout()
        # Right_hbox = QHBoxLayout()

        # after defining variables of type QVBox and QHBox
        # I will Assign treevies variable to the left one and the first text editor in which the code will be written to the right one
        Left_hbox.addWidget(self.treeview)
        # Right_hbox.addWidget(tabs_list)

        # defining another variable of type Qwidget to set its layout as an QHBoxLayout
        # I will do the same with the right one
        Left_hbox_Layout = QWidget()
        Left_hbox_Layout.setLayout(Left_hbox)

        # Right_hbox_Layout = QWidget()
        # Right_hbox_Layout.setLayout(Right_hbox)

        # I defined a splitter to seperate the two variables (left, right) and make it more easily to change the space between them
        H_splitter = QSplitter(Qt.Horizontal)
        H_splitter.addWidget(Left_hbox_Layout)
        # H_splitter.addWidget(Right_hbox_Layout)
        H_splitter.addWidget(self.editor)

        H_splitter.setStretchFactor(1, 1)

        # I defined a new splitter to seperate between the upper and lower sides of the window
        V_splitter = QSplitter(Qt.Vertical)
        V_splitter.addWidget(H_splitter)
        V_splitter.addWidget(text2)

        Final_Layout = QHBoxLayout(self)
        Final_Layout.addWidget(V_splitter)

        self.setLayout(Final_Layout)

    # defining a new Slot (takes string) to save the text inside the first text editor
    @pyqtSlot(str)
    def Saving(self, s):
        with open('main.py', 'w') as f:
            TEXT = self.editor.getActiveBuffer().toPlainText()
            f.write(TEXT)

    # defining a new Slot (takes string) to set the string to the text editor
    @pyqtSlot(str)
    def Open(self, s):
        self.editor.getActiveBuffer().setText(s)

    def on_clicked(self, index):

        nn = self.sender().model().filePath(index)
        nn = tuple([nn])

        if nn[0]:
            name = nn[0]
            path = nn[0]
            self.editor.openBuffer(name, path)
            # f = open(nn[0],'r')
            # with f:
            #     data = f.read()
            #     self.editor.getActiveBuffer().setText(data)

# defining a new Slot (takes string)
# Actually I could connect the (mainwindow) class directly to the (widget class) but I've made this function in between for futuer use
# All what it do is to take the (input string) and establish a connection with the widget class, send the string to it
@pyqtSlot(str)
def reading(s):
    b = Signal()
    b.reading.connect(Layout.Saving)
    b.reading.emit(s)

# same as reading Function
@pyqtSlot(str)
def Openning(s):
    b = Signal()
    b.reading.connect(Layout.Open)
    b.reading.emit(s)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def switch_theme(self, dark):
        if(dark) :
            App.setDarkTheme()
        else :
            App.setLightTheme()

    def initUI(self):
        self.b = Signal()

        self.Open_Signal = Signal()

        # connecting (self.Open_Signal) with Openning function
        self.Open_Signal.reading.connect(Openning)

        # connecting (self.b) with reading function
        self.b.reading.connect(reading)

        # creating menu items
        menubar = self.menuBar()

        # I have three menu items
        filemenu = menubar.addMenu('File')
        view     = menubar.addMenu('View')
        Run      = menubar.addMenu('Run')

        # Making and adding Run Actions
        RunAction = QAction("Run", self)
        RunAction.triggered.connect(self.Run)
        Run.addAction(RunAction)

        # Making and adding File Features
        Save_Action = QAction("Save", self)
        Save_Action.triggered.connect(self.save)
        Save_Action.setShortcut("Ctrl+S")
        Close_Action = QAction("Close", self)
        Close_Action.setShortcut("Alt+c")
        Close_Action.triggered.connect(self.close)
        Open_Action = QAction("Open", self)
        Open_Action.setShortcut("Ctrl+O")
        Open_Action.triggered.connect(self.open)

        filemenu.addAction(Save_Action)
        filemenu.addAction(Close_Action)
        filemenu.addAction(Open_Action)

        dark_theme_checkbox = QAction("Dark Theme", self, checkable=True, checked=True)
        dark_theme_checkbox.triggered.connect(self.switch_theme)
        view.addAction(dark_theme_checkbox)

        # Seting the window Geometry
        monitor = QDesktopWidget().screenGeometry(display_monitor)
        self.move(monitor.left(), monitor.top())
        self.resize(800, 600)
        self.setWindowTitle('Anubis IDE')
        self.setWindowIcon(QtGui.QIcon('Anubis.png'))

        main_layout = Layout()

        self.setCentralWidget(main_layout)
        self.show()

    ###########################        Start OF the Functions          ##################
    def Run(self):
        pass

    # I made this function to save the code into a file
    def save(self):
        self.b.reading.emit("name")

    # I made this function to open a file and exhibits it to the user in a text editor
    def open(self):
        file_name = QFileDialog.getOpenFileName(self,'Open File','/home')

        if file_name[0]:
            f = open(file_name[0],'r')
            with f:
                data = f.read()
            self.Open_Signal.reading.emit(data)

if __name__ == '__main__':
    Application(sys.argv)
