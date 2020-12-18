import sys
from collections import Counter
#import pysrt #GPL
import srt #MIT license
import nltk
#import nltk.data
from nltk import WordNetLemmatizer, pos_tag
from nltk.stem import SnowballStemmer, PorterStemmer 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize, regexp_tokenize

import log

if __name__ == '__main__':
    log.set_loglevel(6)

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')

    stop_words = set(stopwords.words("english"))  # load stopwords

    #print(stop_words)
    #tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    lemma = WordNetLemmatizer()
    porter = PorterStemmer()
    snowball = SnowballStemmer("english")


    subs = None
    raw = ""
    #subs = pysrt.open("Corpse.Bride.2005.srt")
    with open("Corpse.Bride.2005.srt", "r") as f:
        subs = srt.parse(f.read())
        for s in subs:
            #raw += s.text + '\n'
            raw += s.content + '\n'

    all_word_tokens = []
    sentences = sent_tokenize(raw)
    for sentence in sentences:
        print(sentence)

        word_tokens = word_tokenize(sentence) 
        #word_tokens = regexp_tokenize(sentence, "[\w']+") 

        print(word_tokens)
        #filtered = [w for w in word_tokens if not w.lower() in stop_words and w.isalpha()] 
        #print(filtered)
        removed_stopwords = [w for w in word_tokens if not w.lower() in stop_words] 
        tokens = [lemma.lemmatize(word, pos = "v") for word in removed_stopwords]
        tokens = [lemma.lemmatize(word, pos = "n") for word in tokens]
        print(tokens)

        print(pos_tag(word_tokens))
        print(pos_tag(removed_stopwords))
        print(pos_tag(tokens))
        
        #tokens = [snowball.stem(word) for word in removed_stopwords]
        #tokens = [porter.stem(word) for word in removed_stopwords]
        #print(tokens)


        #all_word_tokens += filtered
        print()

    #word_count = Counter(all_word_tokens)
    #print(word_count.most_common(10))

