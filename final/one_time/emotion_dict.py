import pandas as pd


def getEmotionDict():
    emotions = {}
    df = pd.read_csv("Emotion_Lexicon-Removed-Refactored.csv", usecols=["Emotion", "Positive", "Negative", "Anger","Anticipation", "Disgust","Fear","Joy","Sadness","Surprise","Trust"])
    for index, row in df.iterrows():
        emotions[row["Emotion"]] = (row["Positive"], row["Negative"], row["Anger"], row["Anticipation"], row["Disgust"],row["Fear"],row["Joy"],row["Sadness"],row["Surprise"],row["Trust"]);
    return emotions
# print(getEmotionDict().get("happy", None))