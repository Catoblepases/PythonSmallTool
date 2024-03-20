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

for word in alphabet:
    os.system("trans en:zh "+"\""+word+"\"")
    for i in range(repeatTime):
        os.system("say "+"\""+word+"\"")
    os.system("clear")
