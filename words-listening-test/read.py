import os
import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QListWidget, QPushButton, QHBoxLayout, QWidget, QToolBar

filename = "meteorology-a.txt"
repeatTime = 2
alphabet = []

print(sys.argv)
if (len(sys.argv) >= 2):
    filename = sys.argv[1]
if (len(sys.argv) >= 3):
    repeatTime = int(int(sys.argv[2]))

with open(filename, 'r') as f:
    while True:
        line = f.readline()
        level = 1  # 2 read-and-listen-not-understand 1 only-listen-not-understand
        if line == '':
            break
        if line == '\n' or line == ' \n':
            continue
        alphabet.append(line[:-1])
    f.close()

random.shuffle(alphabet)


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        self.index = 0

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        # self.addToolBar(toolbar)

        button_action = QAction("latter", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.start)
        button_action.setCheckable(True)
        button_action.setShortcut(QKeySequence("Enter"))
        toolbar.addAction(button_action)

        layout = QHBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(toolbar)
        self.setLayout(layout)

    def start(self):
        window.insert(alphabet[self.index]+"\n")
        os.system("trans en:zh "+"\""+alphabet[self.index]+"\"")
        os.system("say "+"\""+alphabet[self.index]+"\"")
        os.system("clear")
        self.index += 1

    def index_changed(self, i):  # Not an index, i is a QListItem
        print(i.text())

    def insert(self, item):
        self.text.insertPlainText(item)

    def text_changed(self, s):  # s is a str
        print(s)


app = QApplication(["testapp"])
window = MainWindow()
window.show()
sys.exit(app.exec())
