import sys
from collections import Counter, OrderedDict
import re
#from xml.etree import ElementTree as ET
from xml.dom import minidom
#import dicttoxml
#import pysrt #GPL
import srt #MIT license
import nltk
#import nltk.data
from nltk import WordNetLemmatizer, pos_tag
from nltk.stem import SnowballStemmer, PorterStemmer 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize, regexp_tokenize
from textblob import TextBlob
import spacy #MIT license support farsi
from spacy.symbols import NOUN, VERB, ADJ, ADV

import log

#dicttoxml.set_debug(False)

USE_SPACY = True


TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
        return TAG_RE.sub('', text)

def escape_xml(s):
    s = s.replace('&', '&amp;')
    s = s.replace('"', '&quot;')
    s = s.replace('\'', '&apos;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    return s

if __name__ == '__main__':
    log.set_loglevel(6)
 
    root = minidom.Document() 
    xml = root.createElement('Padington')  
    root.appendChild(xml) 

    #verbsChild = root.createElement('verbs') 
    #nounsChild = root.createElement('nouns') 

    #xml.appendChild(verbsChild)
    #xml.appendChild(nounsChild)


    subs = None
    raw = ""
    #subs = pysrt.open("Corpse.Bride.2005.srt")
    with open("Corpse.Bride.2005.srt", "r") as f:
        subs = srt.parse(f.read())
        for s in subs:
            #raw += s.text + '\n'
            raw += s.content + '\n'
    log.info("convert srt file to raw string")
   

    symbols = {NOUN:('noun', 0, {}), VERB:('verb', 0, {}), ADJ:('adjective', 0, {}), ADV:('adverb', 0, {})}
    if USE_SPACY:
        #nlp = spacy.load('en')
        nlp = spacy.load('en_core_web_sm')

        doc = nlp(remove_tags(raw))
        log.info("remove html tag")
        for sent in doc.sents:
            for token in sent:
                if len(token.lemma_) <= 1:
                    continue

                name, length, d = symbols.get(token.pos, ("", 0, {}))
                #print(d, token.pos, symbols)
                if name:
                    info = d.setdefault(token.lemma_, {'counter':0, 'example':set() })
                    #print(info)

                    info['counter'] += 1
                    info['example'].add(sent.text.strip())
                    #print(token.lemma_, info['counter'], info['example'])

                    symbols[token.pos] = (name, length+1, d)

                #print(d)
                #print(sent)
                #print(token.pos_, token.lemma_)
                
                #if token.lemma_ == 'd' or token.lemma_ == 'm':
                #    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                #                token.shape_, token.is_alpha, token.is_stop, sent.text.strip())
                #print(token.lemma_, token.text, "(", sent.text.strip(), ")")

        for symbol, (name, length, d) in symbols.items():

            s = sorted(d.items(), reverse=True, key = lambda k:(k[1]['counter'], k[0] ))

            symbol_xml = root.createElement(escape_xml(name)) 
            symbol_xml.setAttribute('length', str(length))
            for k, v in s:
                if not escape_xml(k).isalnum():
                    log.warning("key "+ escape_xml(k) + " is not valid name")
                    continue

                word_xml = root.createElement(escape_xml(k)) 
                count = v['counter']
                word_xml.setAttribute('count', str(count))
                examples = v['example']
                for example in examples:
                    item = root.createElement('item')
                    text = root.createTextNode(escape_xml(example))
                    item.appendChild(text)

                    word_xml.appendChild(item)

                symbol_xml.appendChild(word_xml)
            
            xml.appendChild(symbol_xml)



            #odict = OrderedDict(s)


            #x = dicttoxml.dicttoxml(odict, custom_root=name, attr_type=False)

            #y = minidom.parseString(x).firstChild
            #y.setAttribute('length', str(length))

            #for child in y.childNodes:
            #    print(len(child.childNodes))
            #    examples = child.getElementsByTagName('example')
            #    print(examples.childNodes)
            #    child.setAttribute('count', counter.nodeValue)
            #    #child.removeChild(counter)
            #    #print("remove")


        with  open("padington.xml","w") as f:
            xml.writexml(f)

        #print(xml)
        #dom = minidom.parseString(xml) 
        #print(dom.toprettyxml()) 

            #print(k, v['counter'], v['example'][0])
            #nounsChild.setAttribute('')



        #for token in doc:
        #    #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
        #    #                    token.shape_, token.is_alpha, token.is_stop)
        #    if token.pos_ == "NOUN":
        #        print(token.text, token.lemma_)
    else:
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

        all_word_tokens = []
        sentences = sent_tokenize(raw)
        for sentence in sentences:
            print(sentence)

            word_tokens = word_tokenize(sentence) 
            #word_tokens = regexp_tokenize(sentence, "[\w']+") 

            print(word_tokens)
            #filtered = [w for w in word_tokens if not w.lower() in stop_words and w.isalpha()] 
            #print(filtered)
            
            #removed_stopwords = [w for w in word_tokens if not w.lower() in stop_words] 
            #tokens = [lemma.lemmatize(word, pos = "v") for word in removed_stopwords]
            #tokens = [lemma.lemmatize(word, pos = "n") for word in tokens]
            #print(tokens)
            print(pos_tag(word_tokens))
            
            #blob = TextBlob(sentence)
            #print(blob.tags)
            #print(blob.noun_phrases)
            
            #word_tokens = regexp_tokenize(sentence, "[\w']+") 
            #print(word_tokens)
            #print(pos_tag(word_tokens))

            #print(pos_tag(removed_stopwords))
            #print(pos_tag(tokens))

            #for each_seq in pos_tag(word_tokens):
            #    for tuples in each_seq:
            #        print(tuples[0], tuples[1])

            
            #tokens = [snowball.stem(word) for word in removed_stopwords]
            #tokens = [porter.stem(word) for word in removed_stopwords]
            #print(tokens)


            #all_word_tokens += filtered
            print()

    #word_count = Counter(all_word_tokens)
    #print(word_count.most_common(10))

