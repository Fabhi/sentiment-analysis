import json
from emotion import ProcessEmotions
import pyodbc


server = "server-itt.database.windows.net"
database = "dwdm"
username = "wefeelfineadmin"
password = "wefeelfine@123"
connectionString = f"""DRIVER={{SQL Server}};
                      SERVER={server};
                      DATABASE={database};
                      UID={username};
                      PWD={password};"""

cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()

def readReddit() :
    f = open("reddit.json",encoding = 'utf-8')
    loaded = json.load(f)
    data = loaded["data"]["children"]
    text = map(lambda x: x["data"]["title"], data)
    return text

def readTwitter():
    f = open("twitter.json",encoding = 'utf-8')
    loaded = json.load(f)
    data = loaded["data"]
    text = map(lambda x: x["text"], data)
    return text

def getEmotions(text, source):
    for item in text:
        results = ProcessEmotions(item)
        if not results : continue
        for result in results:
            print("Original Text :", result["text"])
            print("Emotion :", result["emotion"])
            print("Start Index: ", result["start"])
            print("Final Index", result["end"])
            print("Degree_index", result["degree_tuple"])
            print("Validity", result["validity"])
            print()
            if result["validity"]:
                insertToDB(result["text"], result["emotion"], result["start"], result["end"], result["degree_tuple"], source)

def insertToDB(text, emotion, start, end, degrees, source):
    sql = """
        INSERT INTO UTTERANCE
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(sql, (text, emotion, start, end, 
    bool(degrees["Positive"]), 
    bool(degrees["Negative"]), 
    bool(degrees["Anger"]), 
    bool(degrees["Anticipation"]), 
    bool(degrees["Disgust"]),
    bool(degrees["Fear"]), 
    bool(degrees["Joy"]), 
    bool(degrees["Sadness"]), 
    bool(degrees["Surprise"]), 
    bool(degrees["Trust"]), 
    source))
    # rows = cursor.fetchAll()
    # for row in rows:
    #     print(row)
    cursor.commit()

def main():
    # reddit = readReddit()
    # getEmotions(reddit, "reddit")


    twitter = readTwitter()
    getEmotions(twitter, "twitter")

if __name__ == "__main__":
    main()