import os
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import pandas as pd

from config.settings import BASE_DIR


class PreProcessing():
    def __init__(self) -> None:
        self._load_corpus(os.path.join(BASE_DIR, "core/corpus"))
        pass

    def _load_corpus(self, corpus_path):
        stopwords = open(corpus_path+"/stopwords.txt", 'r')
        normalisasi = open(corpus_path+"/normalisasi.txt", 'r')
        self.stopwords = stopwords.read().splitlines()
        self.normalisasi = normalisasi.read().splitlines()

    def _cleaning(self,tweet):
        # Hapus pencatuman username di tweet ex:@jokowi    
        _tweet = re.sub(r"@[\w]*", "", tweet)
        # Hapus hyperlink  
    #     _tweet =  re.sub(r"https?:\/\/.*[\r\n]*", "", _tweet)
        _tweet =  re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL', _tweet)
        # Hapus Special Character    
        _tweet = re.sub(r"[()\"#/@;:<>{}*`'+=~|.!?,]", "", _tweet)
        _tweet = re.sub('[^a-zA-Zа-яА-Я]+', ' ', _tweet)
        # Remove multiple space 
        _tweet = re.sub("\s\s+", " ", _tweet)
        # Remove Emoji
        _regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
        return re.sub(_regrex_pattern, "", _tweet)
    
    # Stopword 
    def _stopword(self,tweet):
        _tweet = [w for w in tweet if not w in self.stopwords]
        return _tweet

    # Normalisasi (Ubah kata alay atau typo)
    def _normalisasi(self,tweet):
        temp = tweet
        for w in self.normalisasi:
            try:
                w_ = w.split(',')
                if tweet.index(w_[0]):
                    temp = [w_[1] if word == w_[0] else word for word in tweet]
            except:
                continue
        return temp

    def _tokenizing(self,tweet):
        if not isinstance(tweet, str): return
        return tweet.split()

    # Casefolding
    def _casefolding(self,tweet):
        tweet = str(tweet).lower()
        return tweet

    # Steeming
    def _steeming(self,tweet):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        tweet = stemmer.stem(" ".join(tweet))
        return tweet.split()


    def _normalization(self,tweet): 
        cleaning = self._cleaning(tweet)
        casefolding = self._casefolding(cleaning)
        tokenizing = self._tokenizing(casefolding)
        normalisasi = self._normalisasi(tokenizing)
        stopword = self._stopword(normalisasi)
        steeming = self._steeming(stopword)
    
        return [cleaning, casefolding, tokenizing, normalisasi, stopword, steeming]

    def callback(self, x):
        cleaning, casefolding, tokenizing, normalisasi, stopword, steeming = self._normalization(x)
        return pd.Series({'cleaning': cleaning, 'casefolding': casefolding, 'tokenizing': tokenizing,'normalisasi':normalisasi,'stopword': stopword,'steeming': steeming, 'cleaned': " ".join(steeming)})
