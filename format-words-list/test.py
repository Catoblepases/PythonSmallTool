import re
import enchant
import os


def delete_extension(name):
    end = len(name)
    for i in range(len(name)):
        if name[i] == '.':
            end = i
    return name[:end]

output_dir = r'output'
file_dir = r"to-do"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
files = os.listdir(file_dir)
print(files)

dic_list=[enchant.Dict("en_US"),enchant.Dict("fr")]
def check(word):
    for d in dic_list:
        if d.check(word):
            return True
    return False


for file in files:
    with open(file_dir+'/'+file) as f:
        with open(output_dir+"/"+delete_extension(file)+".txt", mode="w+") as nf:
            str = f.readline()
            while (str):
                str = re.sub(u"([^\u0041-\u005a\u0061-\u007a\u0020\u3000\u002d])", "", str)
                l = str.split(' ')
                s = ""
                for i in range(len(l)):
                    if (l[i] == ''):
                        continue
                    if (l[i][0] == '('):
                        l[i] = l[i][1:-1]
                    if (len(l[i]) <= 1):
                        continue
                    if (check(l[i])):
                        s += l[i]+" "
                if len(s) == 0:
                    str = f.readline()
                    continue
                if s[-1] == ' ':
                    s = s[:-1]
                nf.write(s+'\n')
                str = f.readline()
            nf.close()
        f.close()
