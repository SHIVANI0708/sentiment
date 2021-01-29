from textblob import TextBlob
import statistics
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer 
from flask import Flask, jsonify, request,render_template


def clean_text(cmnt):
    #Remove RT
    cmnt = re.sub(r'RT', '', cmnt)
    
    #Fix &
    cmnt = re.sub(r'&amp;', '&', cmnt)
    
    #Remove punctuations
    cmnt = re.sub(r'[?!.;:#-//,@]', '', cmnt)
    
    #Convert to lowercase to maintain consistency
    cmnt=cmnt.lower()

    #Tokenization
    cmnt=nltk.word_tokenize(cmnt)
    
    
    #lemmatization
    lemma = WordNetLemmatizer()
    for i in cmnt:
        lemma.lemmatize(i, pos="v")
    
    #Stopwords remove
    cmnt = " ".join([w for w in cmnt if w not in stopwords.words('english')])
    
    
    return (cmnt)

app = Flask(__name__)

@app.route("/",methods=["GET"])
def index():
    return render_template("test.html",sentiment=100*100)

@app.route("/analysis",methods=["GET"])
def calc():
    l1 = []
    file = open(r"dataset.txt","r+")
    for line in file.read().split('\n'):
        x = clean_text(line)
        analysis = TextBlob(x)
        #correct spelling
        analysis = analysis.correct()
        s=analysis.sentiment.polarity   
        l1.append(s)
    x=statistics.mean(l1)
    print("Percentage :{}%".format(x*100))
    file.close()
    return str(x*100)
    

if __name__=="__main__":
    app.run(port=3000)
