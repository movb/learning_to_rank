from collections import Counter
import numpy as np

def score_idf(N, n, smooth=0.5):
    if smooth==0:
        if n==0:
            return 0
        else:
            return np.log(N/n)
    return np.log((N - n + smooth)/(n+smooth))

def score_bm25_internal(N, query_terms, inverted_terms, doc_terms, doc_len, avg_doc_len, k1, b, idf_smooth):
    result = 0.0
    for term in query_terms:
        idf = score_idf(N, inverted_terms[term], idf_smooth)
        result += idf * (doc_terms[term]*(k1 + 1))/(doc_terms[term] + k1*(1 - b + b*(doc_len/avg_doc_len)))
    return result
        
def score_bm25(index, query, title, body, k1=1.5, b=0.75, idf_smooth=0):
    query_terms = index.normalize_string(query)
    title_terms = index.normalize_string(title)
    body_terms = index.normalize_string(body)

    title_score = score_bm25_internal( index.N,
                                       query_terms,
                                       index.term_to_title,
                                       Counter(title_terms),
                                       len(title_terms),
                                       index.avg_title_length,
                                       k1, b, idf_smooth )
    body_score  = score_bm25_internal( index.N,
                                       query_terms,
                                       index.term_to_body,
                                       Counter(body_terms),
                                       len(body_terms),
                                       index.avg_title_length,
                                       k1, b, idf_smooth )
    whole_score = score_bm25_internal( index.N,
                                       query_terms,
                                       index.term_to_whole,
                                       Counter(title_terms) + Counter(body_terms),
                                       len(title_terms) + len(body_terms),
                                       index.avg_title_length + index.avg_body_length,
                                       k1, b, idf_smooth )

    return title_score, body_score, whole_score