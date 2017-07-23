from collections import Counter, defaultdict
import utils
import sys
import numpy as np

class Index:
    def __init__(self, file_name, norm_method = 'norm', debug=0):
        self.file_name = file_name
        self.norm_method = norm_method
        self.debug = debug
        self.term_to_title = defaultdict(int)
        self.term_to_body = defaultdict(int)
        self.term_to_whole = defaultdict(int)
        
        self.N = 0
        self.title_lengths = {}
        self.body_lengths = {}
        self.whole_lengths = {}
        self.avg_title_length = 0
        self.avg_body_length = 0
        
        self.unigram_filter = None
        self.bigram_filter = None
        self.char_trigram_filter = None
        self.stop_words = []
        self.fd = open(self.file_name,'rt')
        
    def build(self):
        self.fd.seek(0, 0)
        for line in self.fd:
            parts = line.strip().split('\t')
            if len(parts) == 3:
                doc_id, title, body = parts
            elif len(parts) == 2:
                doc_id, title = parts
                body = ''
            elif len(parts) == 1:
                doc_id, title, body = parts[0], '', ''
            else:
                continue

                doc_id = int(doc_id)

                if self.debug > 1:
                    sys.stderr.write('\rProcessing document {}: {}'.format(doc_id, title))

                title_terms = self.normalize_string(title)
                body_terms = self.normalize_string(body)

                self.title_lengths[doc_id] = len(title.split())
                self.body_lengths[doc_id] = len(body.split())
                self.whole_lengths[doc_id] = self.title_lengths[doc_id] + self.body_lengths[doc_id]

                for term in set(title_terms):
                    self.term_to_title[term] += 1
                for term in set(body_terms):
                    self.term_to_body[term] += 1
                for term in set(body_terms + title_terms):
                    self.term_to_whole[term] += 1

                self.N += 1

                if self.debug > 0:
                    if (self.N % 100) == 0:
                        sys.stderr.write('\rProcessed documents {}'.format(self.N))

        self.avg_title_length = np.sum(list(self.title_lengths.values())) / float(len(self.title_lengths))
        self.avg_body_length = np.sum(list(self.body_lengths.values())) / float(len(self.body_lengths))
        
    def normalize_string(self, doc):
        terms = doc.strip().split(' ')
        terms = [term for term in terms if term not in self.stop_words]
        return self.normalize(terms)
    
    def normalize(self, terms):
        normalized_terms = []
        terns = [term.lower() for term in terms]
        
        if self.norm_method == 'none':
            if self.unigram_filter is not None:
                normalized_terms = [term for term in terms if term in self.unigram_filter]
            else:
                normalized_terms = terms
        elif self.norm_method == 'word_bigrams':
            for i in range(0,len(terms)-1):
                bigram = terms[i]+" "+terms[i+1]
                if self.bigram_filter is not None:
                    if bigram in self.bigram_filter:
                        normalized_terms.append(bigram)
                else:
                    normalized_terms.append(terms[i]+" "+terms[i+1])
        elif self.norm_method == 'char_trigrams':
            for term in terms:
                trigrams = self.make_trigrams(term)
                if self.char_trigram_filter is not None:
                    trigrams = [trigram for trigram in trigrams if trigram in self.char_trigram_filter]
                normalized_terms.extend(self.make_trigrams(term))                
                
        return normalized_terms
    
    def make_trigrams(self, term):
        trigrams = []
        for i in range(0,len(term)-2):
            trigrams.append(term[i:i+3])
        return trigrams
    
    def save(self, prefix):
        utils.save_to_file(self.title_terms, prefix+"title_terms.pkl")
        utils.save_to_file(self.body_terms, prefix+"body_terms.pkl")
        #utils.save_to_file(self.doc_title_terms, prefix+"doc_title_terms.pkl")
        #utils.save_to_file(self.doc_body_terms, prefix+"doc_body_terms.pkl")
        
    def load(self, prefix):
        self.title_terms = utils.load_from_file(prefix+"title_terms.pkl")
        self.body_terms = utils.load_from_file(prefix+"body_terms.pkl")
        #self.doc_title_terms = utils.load_from_file(prefix+"doc_title_terms.pkl")
        #self.doc_body_terms = utils.load_from_file(prefix+"doc_body_terms.pkl")