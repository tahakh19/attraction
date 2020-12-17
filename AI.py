import sys
from collections import Counter
import pysrt
import nltk
#import nltk.data
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

import log

if __name__ == '__main__':
    log.set_loglevel(6)

    nltk.download('punkt')
    nltk.download('stopwords')

    stop_words = set(stopwords.words("english"))  # load stopwords

    #print(stop_words)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    sub = pysrt.open("Corpse.Bride.2005.srt")
    raw = ""
    for s in sub:
        raw += s.text + '\n'


    sentences = sent_tokenize(raw)
    for sentence in sentences:
        #print(text)
        #tokens = tokenizer.tokenize(text)
        #print(tokens)
        #tokens = sent_tokenize(text)
        print(sentence)
        word_tokens = word_tokenize(sentence) 
        print(word_tokens)
        filtered = [w for w in word_tokens if not w.lower() in stop_words and w.isalpha()] 
        print(filtered)
        #for token in tokens:
        #    #print(token)
        #    word_tokens = word_tokenize(token) 
        #    print(word_tokens)
        #    filtered = [w for w in word_tokens if not w in stop_words] 
        #    print(filtered)
        print()

    #tokens = word_tokenize(raw)
    #print(tokens)
    #word_count = Counter(tokens)
    #print(word_count)
    #print(word_count.most_common(10))

   

    #for s in sub:
    #    print("TESTTEST:", s)
    #log.debug(stop_words)

    #word_tokens = word_tokenize(sub)  
    #filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    #log.debug(filtered_sentence)

