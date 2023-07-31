# import translators as ts
import os
from googletranslatepy import Translator
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/celes/Documents/AppConfig/studied-source-262518-f247950e815e.json"

translator = Translator()

path = './translate/input/'  # 待读取文件的文件夹绝对地址
files = os.listdir(path)  # 获得文件夹中所有文件的名称列表

# for filename in ["translate/test.ERB"]:
for filename in files:
    if ("Store" in filename):
        continue
    print(filename)
    text = ""
    with open(path+filename, 'r') as f:
        text = f.read()
        f.close()

    lines = text.split("\n")

    def cut(line):
        begin, end = 0, 0
        for i in range(0, len(line)):
            if (line[i] == '「'):
                begin = i
            elif (line[i] == '」'):
                end = i
        for i in range(begin, end):
            if (line[i] == '%'):
                if (close):
                    close = False
                else:
                    close = True
                    begin = i+1
                    break
        if (begin == 0 or end == 0):
            return 0, 0
        return begin, end

    def cut2(line):
        p = "()"
        begin, end = 0, 0
        PTL = ["PRINTFORML ", "RETURN_STR '=  ", "DATAFORM ",
               "PRINTFORMDW ", "PRINTFORMDL ", "PRINTFORMW ", "CALL HTMLPRINTW(@\" ", "PRINTDL ", "PRINTDW ","CALL HTMLPRINTW"]
        PT = ""

        for s in PTL:
            if (s in line):
                PT = s

        if ((PT == "") or (("RETURN_STR '=  ") and (line[begin] in "QWERTYUIOPASDFGHJKLZXCVBNM")) or (line.count('%') >= 6)):
            return 0, 0

        idx = line.find(PT)
        begin = idx+len(PT)
        end = len(line)
        
        if (PT == "CALL HTMLPRINTW"):
            begin += 4

        if (("\\@" in line[begin:end])):
            return 0, 0
        close = True

        for i in range(begin, end):
            if (line[i] == '「' or (line[i] == p[0])):
                begin = i+1
            if (line[i] == '%'):
                if (close):
                    close = False
                else:
                    close = True
                    begin = i+1
                    break

        for i in reversed(range(begin, end)):
            if ((line[i] == '」') or (line[i] == p[1])):
                end = i
            if (line[i] == '%'):
                if (close):
                    close = False
                else:
                    close = True
                    end = i
                    break
        if ((begin >= len(line)) or (end > len(line))):
            return 0, 0
        if (line[begin] == "\""):
            begin = begin+1
        if (line[end-1] == "\""):
            end = end-1
        return begin, end

    document = ""
    to_translate = []
    be = []
    separator = "<b>"

    TEXT = []
    for line in lines:
        begin, end = cut2(line)
        be.append((begin, end))
        text = line[begin:end]
        to_translate.append(text)

    assert (len(to_translate) == len(lines))

    def put_togethoer(list, begin, end):
        out = ""
        for i in range(begin, end):
            if (i > len(list)-1):
                break
            out += list[i]+separator
        return out

    TOGETHOR = [to_translate[i] == '' for i in range(len(to_translate))]
    TEXT = ['' for i in range(len(to_translate))]

    for i in range(len(to_translate)):
        print(i, "/", len(to_translate))
        if (not TOGETHOR[i]):
            TEXT[i] = translator.translate(
                to_translate[i], src='ja', dest='zh')
            if (type(TEXT[i]) != str):
                TEXT[i] = to_translate[i]
            # TEXT[i]=translate_jp_zh(to_translate[i])

    print(len(TEXT), len(lines))
    assert (len(TEXT) == len(lines))

    for i in range(len(be)):
        begin, end = be[i]
        line = lines[i]
        if (not TOGETHOR[i]):
            newline = line[:begin]+TEXT[i]+line[end:]
        else:
            newline = line
        document += newline+"\n"

    name = filename.split('/')[-1]
    with open(name, 'w') as f:
        f.write(document)
        f.close()
