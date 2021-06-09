import re
from emotion_dict import getEmotionDict
patterns = []
adverbs = frozenset(["not", "also", "very", "often", "however", "too", "usually", "really", "early", "never", "always", "sometimes", "together", "likely", "simply", "generally", "instead", "actually", "again", "rather", "almost", "especially", "ever", "quickly", "probably", "already", "below", "directly", "therefore", "else", "thus", "easily", "eventually", "exactly", "certainly", "normally", "currently", "extremely", "finally", "constantly", "properly", "soon", "specifically", "ahead", "daily", "highly", "immediately", "relatively", "slowly", "fairly", "primarily", "completely", "ultimately", "widely", "recently", "seriously", "frequently", "fully", "mostly", "naturally", "nearly", "occasionally", "carefully", "clearly", "essentially", "possibly", "slightly", "somewhat", "equally", "greatly", "necessarily", "personally", "rarely", "regularly", "similarly", "basically", "closely", "effectively", "initially", "literally", "mainly", "merely", "gently", "hopefully", "originally", "roughly", "significantly", "totally", "twice", "elsewhere", "everywhere", "obviously", "perfectly", "physically", "successfully", "suddenly", "truly", "virtually", "altogether", "anyway", "automatically", "deeply", "definitely", "deliberately", "hardly", "readily", "terribly", "unfortunately", "forth", "briefly", "moreover", "strongly", "honestly", "previously", "as", "there", "when", "how", "so", "up", "out"])
degreeTuple = ["Positive", "Negative","Anger"	,"Anticipation",	"Disgust"	,"Fear"	,"Joy",	"Sadness"	,"Surprise",	"Trust"]

allAfter = "\s+(.[^.,_-]*)"
justAfter = "\s+(\w+(?= )*)"
query = "I am feeling"
query2 = "I feel"
d = getEmotionDict()
def extractNext(text, queryText = query):
    res = []
    matches = re.findall(queryText+justAfter, text)
    # print(text, matches)
    if len(matches) == 0: return None
    else:
        for match in matches:
            word = match
            end = re.search(queryText+justAfter, text).end()
            start = end - len(match)
            res.append({"match" : word,  "start" : start, "end":end, "text": text, "emotion": None, "degree_tuple" : None, "validity" : False})
    return res
    
def isEmotion(c):
    candidates = [c, c+"ness" ,c[:-1]+"ness" , c+"ment", c+"ation", c+"tion", c+"sion"]
    if(len(c)>3):
        candidates.append(c[:-3]+"ence")
        candidates.append(c[:-2]+"ness")
    for i in candidates:
        val = d.get(i, None)
        if val:
            # print(i)
            return val
    return False

def emotionSearch(results):
    for result in results:
        candidate = result["match"].lower()
        a = isEmotion(candidate)
        if a:
            result["emotion"] = candidate
            result["degree_tuple"] = dict(zip(degreeTuple, a))
            result["validity"] = any(a)
        else:
            if candidate in adverbs:
                nextCandidate = extractNext(result["text"], candidate)[0]["match"]
                a = isEmotion(nextCandidate)
                if a:
                    result["emotion"] = nextCandidate
                    result["degree_tuple"] = dict(zip(degreeTuple, a))
                    result["validity"] = any(a)
def preprocess(txt):
    return txt.replace("I’m", "I am").replace("I'm", "I am")

samples= [
"Got my hair chopped off and I am feeling myself! (Before pic included)",
"Was called un-dateable due to being a virgin and I am feeling very hurt and confused.",
"I am feeling a shitload of anxiety about Natasha Helfer's disciplinary council, and I just figured out why.",
"Today is day three of not drinking, and I’m feeling very sad and depressed. I’ve been crying and very down. I can’t think of very many positive things. I don’t necessarily want a drink, but I’m just feeling sad. Is this normal? Any suggestions to get out of this funk"
]


def ProcessEmotions(data):
    res = []
    
    cleaned_text = preprocess(data)
    a = extractNext(cleaned_text)
    if a is None: return None
    res.extend(a)
    emotionSearch(res)
    return res

# print(ProcessEmotions(samples))