import json
import os
import sys


class WordsReview:
    def __init__(self, filename="dic/test.txt", mode="regular", save=True, listenMode=False):
        self.alphabet = {}
        self.filename = filename
        self.output_dir = "output/"
        self.mode = mode
        self.saveFile = save
        self.listenMode = listenMode
        with open(path, 'r') as f:
            while True:
                line = f.readline()
                if line == '':
                    break
                if line == '\n' or line == ' \n':
                    continue
                self.add_to_alphabet(line[:-1], 0)
            f.close()

    def delete_extension(name):
        end = len(name)
        for i in range(len(name)):
            if name[i] == '.':
                end = i
        return name[:end]

    def add_to_alphabet(self, word, level):
        if (word[-1] == '\n' or word[-1] == ' '):
            word = word[:-1]
        self.alphabet[word] = level

    def deal_with_typing(self, input):
        if input == '.' or input == ':wq' or input == 'quit':
            sys.exit("end")
        if input == '':
            return False
        return True

    def save(self):
        filename = WordsReview.delete_extension(
            os.path.basename(self.filename))
        # self.save_as_json(self.output_dir+filename+".json")
        self.save_as_txt(filename)

    def save_as_json(self, output):
        file = {'content': self.alphabet}
        with open(output, 'w') as nf:
            nf.write(json.dumps(file))
            nf.close()

    def save_as_txt(self, filename):
        with open(self.output_dir+filename+"-all"+".txt", 'w') as nf:
            for key, val in self.alphabet.items():
                if val != 0:
                    nf.write(str(key)+"\n")
            nf.close()
        if (mode != 'simple'):
            with open(self.output_dir+filename+"-only-listen"+".txt", 'w') as nf:
                for key, val in self.alphabet.items():
                    if val == 2:
                        nf.write(str(key)+"\n")
                nf.close()

    def main(self):
        simpleMode = self.mode == 'simple'
        alphabet = self.alphabet.copy()
        for line, _ in alphabet.items():
            # add to dictionary with difficulty level
            while True:
                level = self.alphabet[line]
                os.system("clear")
                os.system("say "+line)
                if (self.deal_with_typing(input("mark or not: \n"))):
                    self.alphabet[line] += 1
                    if (not simpleMode):
                        print(line+'\n')
                        self.alphabet[line] += 1 if self.deal_with_typing(
                            input("mark or not: \n")) else 0
                os.system("trans en:zh "+"\""+line+"\"")
                self.alphabet[line] += 1 if self.deal_with_typing(
                    input("mark or not: \n")) else 0
                if not self.listenMode or level == self.alphabet[line]:
                    break
        if self.saveFile:
            self.save()


if __name__ == "__main__":
    print(sys.argv)
    mode = "regular"
    save = True
    listenMode = False
    if (len(sys.argv) <= 1):
        path = "dic/test.txt"
    else:
        path = sys.argv[1]
    if ('-s' in sys.argv):
        mode = 'simple'
    if '--save=false' in sys.argv or '-ns' in sys.argv:
        save = False
    if '-l' in sys.argv:
        listenMode = True

    object = WordsReview(path, mode, save, listenMode)
    object.main()
