import re
import genanki as gk

pattern = re.compile(r'(^[0-9]+)', re.I)
my_model = gk.Model(
  1607392319,
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])

def preprocessing(text):
    text = text.split('\n')
    dic = dict()
    for line in text:
        if (len(line) <= 6):
            text.remove(line)
    key = ""
    content = ""
    for i in range(len(text)):
        if (re.match(pattern, text[i]) != None):
            if ((key != "") and (content != "")):
                dic[key] = content
            key = text[i]
            content = ""
        else:
            content += text[i]+"\n"
    return dic


def progress_text(pp):
    pp = pp.split('\n')

    for words in pp:
        if (len(words) <= 6):
            pp.remove(words)

    # print(pp)

    dic = {}

    def is_english(c):
        return (ord(c)-ord('a') >= 0 and ord(c)-ord('a') <= 26) or (ord(c)-ord('A') >= 0 and ord(c)-ord('A') <= 26)

    def split_word(text):
        word = ""
        other = ""
        button = False
        for c in text:
            if (is_english(c) and word == ""):
                button = True

            if (button and ((is_english(c)) or (c in " /,.~=;"))):
                word += c
            else:
                button = False
                if (c not in "- ()"):
                    other += c

        return word, other

    for words in pp:
        word, other = split_word(words)
        dic[other] = word

    return dic

def encode_string(mystring):
    mybytes = mystring.encode('utf-8')
    myint = int.from_bytes(mybytes, 'little')
    return myint

def decode_string(myint):
    recoveredbytes = myint.to_bytes((myint.bit_length() + 7) // 8, 'little')
    recoveredstring = recoveredbytes.decode('utf-8')
    return recoveredstring

def dic_to_anki(dic,deckname):
    my_deck = gk.Deck(encode_string(deckname)%(1<<12),deckname)
    for key,value in dic.items():
        my_note = gk.Note(
        model=my_model,
        fields=[key, value])
        my_deck.add_note(my_note)

    gk.Package(my_deck).write_to_file(deckname+'.apkg')    
