import json
from emotion import ProcessEmotions

f = open("reddit.json",encoding = 'utf-8')
loaded = json.load(f)
data = loaded["data"]["children"]
text = map(lambda x: x["data"]["title"], data)

res = map(ProcessEmotions, text)
for item in res:
    if item:
        for i in item:
            if i["valid"]:
                print(i["emotion"], i["valid"])
            else:
                print(i["emotion"], i["text"])
    else:
        print("No item")