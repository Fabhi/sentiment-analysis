import spacy
import json

def parse2(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    noun_adj_pairs = []
    for i,token in enumerate(doc):
        if token.pos_ not in ('NOUN','PROPN'):
            continue
        for j in range(i+1,len(doc)):
            if doc[j].pos_ == 'ADJ':
                noun_adj_pairs.append((token,doc[j]))
                break
    return noun_adj_pairs

def parse(text):
    query = "I feel"
    start = text.find(query)+len(query)
    end = text.find(' ', start+1)
    if(end>=len(text)):
        return None
    # print(start, end)
    adj = text[start+1:end+1]
    return adj

if __name__ == "__main__":
    f = open("json.json",encoding = 'utf-8')
    data = json.load(f,)
    for data in data["data"]:
        a = parse(data["text"])
        if a:
            print(data["text"])
            print(a)
        print()