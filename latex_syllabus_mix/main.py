import pyperclip

LLL = ["LU3IN030", "LU2IN024", "LU2IN005", "LU3IN034", "LU2MA120", "LU2IN009", "LU2IN015",
       "LU2IN023", "LU2IN014", "LU3IN003", "LU2IN003", "LU2IN002", "LU2MA241", "LU1MA001",
       "LU2MA221", "LU2MA123", "LU2MA216", "LU2MA260", "LU2IN006", "LU2IN013", "LU2IN019",
       "LU2IN018", "LU2PY532", "LU1IN002", "LU1IN001", "LU3MA232", "LU3IN024"]

text = """\section{LU1IN001}\n\label{LU1IN001}\n\subsection{translation}\n\includegraphics[scale=0.7]{en/LU1IN001_en.pdf}\n\n\n"""

ppp = text.replace("LU1IN001", "LU1IN002")

# print(text)

out=""
for course in LLL:
    out+=text.replace("LU1IN001", course)

# pyperclip.copy(out)
with open("test.txt","w") as f:
    f.write(out)
