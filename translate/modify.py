FILE=[""]
prefix="./translate/input/"

def put_togethoer(list):
    out=""
    for i in range(len(list)):
        out+=list[i]+'\n'
    return out

for filename in FILE:
    with open(filename, "r") as fw:
        with open(prefix+filename, "r") as fr:
            test_r=fr.read()
            test_w=fw.read()
            TEXT_r=test_r.split('\n')
            TEXT_w=test_w.split('\n')
            for i in range(min(len(TEXT_r),len(TEXT_w))):
                if(('\\@' in TEXT_w[i])):
                    print(TEXT_w[i])
                    TEXT_w[i]=TEXT_r[i]
                    print(i)
            for i in range(len(TEXT_w)):
                print(TEXT_w[i])
            with open("./.output/"+filename,'w') as f:
                f.write(put_togethoer(TEXT_w)) 