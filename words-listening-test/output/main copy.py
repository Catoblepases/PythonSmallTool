import json
import os
from platform import system
import sys


class WordsReview:
    def __init__(self, filename="dic/test.txt", mode="regular"):
        self.alphabet = {}
        self.filename = filename
        self.mode = mode

    def find_name(name):
        begin = 0
        for i in range(len(name)):
            if name[i] == '\\' or name[i] == '/':
                begin = i+1
        return name[begin:]

    def delete_extension(name):
        end = len(name)
        for i in range(len(name)):
            if name[i] == '.':
                end = i
        return name[:end]

    def add_to_alphabet(self, word, level):
        if(word[-1] == '\n' or word[-1] == ' '):
            word = word[:-1]
        self.alphabet[word] = level

    def deal_with_typing(self, input):
        if input == '.' or input == ':wq' or input == 'quit':
            sys.exit("end")
        if input == '':
            return False
        return True

    def save(self):
        file = {'content': self.alphabet}
        dir = "output/"
        filename = WordsReview.delete_extension(
            WordsReview.find_name(self.filename))
        with open(dir+filename+".json", 'w') as nf:
            nf.write(json.dumps(file))
            nf.close()
        with open(dir+filename+"-a"+".txt", 'w') as nf:
            for key, val in self.alphabet.items():
                nf.write(str(key)+"\n")
            nf.close()

    def main(self):
        simpleMode = self.mode == 'simple'
        with open(path, 'r') as f:
            while True:
                line = f.readline()
                if line == '':
                    break
                if line == '\n' or line == ' \n':
                    continue
                os.system("clear")
                os.system("say "+line)
                # add to dictionary with difficulty level
                level = 1  # 2 read-and-listen-not-understand 1 only-listen-not-understand
                if(self.deal_with_typing(input("mark or not: \n"))):
                    if(not simpleMode):
                        print(line+'\n')
                        level += 1 if self.deal_with_typing(input("mark or not: \n")) else 0
                    self.add_to_alphabet(line, level)
                os.system("trans en:zh "+"\""+line+"\"")
                if input("mark or not: \n") != '':
                    self.add_to_alphabet(line, 1)
            self.save()
            f.close()

print(sys.argv)
mode = "regular"
if (len(sys.argv) <= 1):
    path = "dic/test.txt"
else:
    path = sys.argv[1]
if (len(sys.argv) == 3 and sys.argv[2] == '-s'):
    mode = 'simple'

object = WordsReview(path, mode)
object.main()
