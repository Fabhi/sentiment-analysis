import json
from emotion import ProcessEmotions


f = open("twitter.json",encoding = 'utf-8')
loaded = json.load(f)
data = loaded["data"]
text = map(lambda x: x["text"], data)

res = map(ProcessEmotions, text)
for item in res:
    if item:
        for i in item:
            if i["valid"]:
                print(i["emotion"], i["valid"])
           




# Note for Sanchit, ignore the emotions where all values in degreeTuples are 0