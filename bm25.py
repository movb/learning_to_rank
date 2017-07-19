import pymorphy2
from collections import Counter, defaultdict
import utils
import sys
import numpy as np

class BM25:
    def __init__(self, file_name, norm_method = 'norm', debug=0, save_normalized=None):
        self.file_name = file_name
        self.norm_method = norm_method
        self.debug = debug
        self.save_normalized = save_normalized
        self.title_terms = Counter()
        self.body_terms = Counter()
        #self.doc_title_terms = defaultdict(Counter)
        #self.doc_body_terms = defaultdict(Counter)
        self.term_to_title = defaultdict(list)
        self.term_to_body = defaultdict(list)
        self.morph = pymorphy2.MorphAnalyzer()
        
        self.N = 0
        self.title_lengths = {}
        self.body_lengths = {}
        self.avg_title_length = 0
        self.avg_body_length = 0
        
        self.bigram_filter = set()
        
    def build(self):
        with open(self.file_name,'rt') as fd:
            if self.save_normalized is not None:
                normalized_fd = open(self.save_normalized, "wt")
            for line in fd:
                parts = line.strip().split('\t')
                if len(parts) != 3:
                    continue
                    
                doc_id, title, body = parts
                doc_id = int(doc_id)
                
                if self.debug > 1:
                    sys.stderr.write('\rProcessing document {}: {}'.format(doc_id, title))
                
                title_terms = self.normalize_string(title)
                body_terms = self.normalize_string(body)
                
                if self.save_normalized is not None:
                    print("{}\t{}\t{}".format(doc_id, " ".join(title_terms), " ".join(body_terms)), file=normalized_fd)
                
                self.title_terms.update(title_terms)
                self.body_terms.update(body_terms)
                
                #self.doc_title_terms[doc_id].update(title_terms)
                #self.doc_body_terms[doc_id].update(body_terms)
                
                self.title_lengths[doc_id] = len(title)
                self.body_lengths[doc_id] = len(body)
                
                for term in set(title_terms):
                    self.term_to_title[term].append(doc_id)
                for term in set(body_terms):
                    self.term_to_body[term].append(doc_id)
                    
                self.N += 1
                
                if self.debug > 0:
                    if (self.N % 100) == 0:
                        sys.stderr.write('\rProcessed documents {}'.format(self.N))
        
        self.avg_title_length = np.sum(list(self.title_lengths.values())) / float(len(self.title_lengths))
        self.avg_body_length = np.sum(list(self.body_lengths.values())) / float(len(self.body_lengths))
        
        if self.save_normalized is not None:
            normalized_fd.close()
        
    def normalize_string(self, doc):
        terms = doc.strip().split(' ')
        return self.normalize(terms)
    
    def normalize(self, terms):
        normalized_terms = []
        
        if self.norm_method == 'none':
            normalized_terms = terms
        elif self.norm_method == 'norm':
            for term in terms:
                if len(term)==0:
                    continue
                parses = self.morph.parse(term)
                if len(parses) > 0:
                    normalized_term = parses[0].normal_form
                else:
                    normalized_term = term
                normalized_terms.append(normalized_term)
        elif self.norm_method == 'word_bigrams':
            for i in range(0,len(terms)-1):
                bigram = terms[i]+" "+terms[i+1]
                if bigram in self.bigram_filter:
                    normalized_terms.append(terms[i]+" "+terms[i+1])
        elif self.norm_method == 'char_trigrams':
            for term in terms:
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
        
    def idf(self, n):
        if n==0:
            return 0    
        return np.log(self.N/n)
    
    def idf2(self, n, smooth=0.5):
        return np.log((self.N - n + smooth)/(n+smooth))
    
    def score_bm25_internal(self, query_terms, inverted_terms, doc_terms, doc_len, avg_doc_len, k1, b, smooth_idf=False):
        result = 0.0
        for term in query_terms:
            if not smooth_idf:
                idf = self.idf(len(inverted_terms[term]))
            else:
                idf = self.idf2(len(inverted_terms[term]))
            result += idf * (doc_terms[term]*(k1 + 1))/(doc_terms[term] + k1*(1 - b + b*(doc_len/avg_doc_len)))
        return result
        
    def score_bm25(self, query, title, body, k1=1.5, b=0.75, smooth_idf=False):
        query_terms = self.normalize_string(query)
        title_terms = self.normalize_string(title)
        body_terms = self.normalize_string(body)
        
        title_score = self.score_bm25_internal( query_terms,
                                                self.term_to_title,
                                                Counter(title_terms),
                                                len(title_terms),
                                                self.avg_title_length,
                                                k1, b, smooth_idf )
        body_score  = self.score_bm25_internal( query_terms,
                                                self.term_to_body,
                                                Counter(body_terms),
                                                len(body_terms),
                                                self.avg_title_length,
                                                k1, b, smooth_idf )

        return title_score, body_score              