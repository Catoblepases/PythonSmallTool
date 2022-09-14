import json

output = ""
with open("outbox.json", "r") as f:
    dict = json.loads(f.read())
    content = dict["orderedItems"]
    for item in content:
        output += item["object"]["content"][3:-4]+"\n\n"
    f.close()

with open("output.txt", "w") as f:
    f.write(output)
    f.close()
