from textblob import TextBlob
import statistics
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer 



file = open(r"comments.txt","a+")
comment=input("Enter comment: ")


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
    #print(cmnt)
    
    #lemmatization
    lemma = WordNetLemmatizer()
    for i in cmnt:
        lemma.lemmatize(i, pos="v")
    
    #Stopwords remove
    cmnt = " ".join([w for w in cmnt if w not in stopwords.words('english')])
    #print (cmnt)
    
    
    return (cmnt)

    
x = clean_text(comment)
#print(x)

file.write("{}\n".format(x))
file.close()

l1=[]
pos_count = 0
pos_correct = 0
with open(r"comments.txt","r") as file:
    for line in file.read().split('\n'):
        analysis = TextBlob(line)
        #correct spelling
        analysis = analysis.correct()
        print (analysis)

        if analysis.sentiment.polarity >= 0:
            if analysis.sentiment.polarity > 0.1:
                pos_correct += 1
            pos_count +=1
        s=analysis.sentiment.polarity   
        l1.append(s)
            
x=statistics.mean(l1)
print("Percentage :{}%".format(x*100))
neg_count = 0
neg_correct = 0

with open(r"comments.txt","r") as file:
    for line in file.read().split('\n'):
        analysis = TextBlob(line)
         #correct spelling
        analysis = analysis.correct()
        #print (analysis)

        if analysis.sentiment.polarity <= 0:
            if analysis.sentiment.polarity <= 0.1:
                neg_correct += 1
            neg_count +=1
            
#print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
#print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))
file.close(