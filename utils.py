import pickle

def get_document(fd, index, doc_id):
    pos = index[doc_id]
    fd.seek(pos)
    line = fd.readline()
    parts = line.strip().split('\t')
    
    if len(parts) !=3:
        return "", ""
    
    return parts[1], parts[2]


def save_to_file(obj, file_name):
    with open(file_name, "wb") as fd:
        pickle.dump(obj, fd)
        

def load_from_file(file_name):
    with open(file_name, "rb") as fd:
        return pickle.load(fd)


def load_queries(file_name):
    queries = {}
    with open(file_name, 'rt') as fd:
        for line in fd:
            parts = line.strip().split('\t')
            queries[int(parts[0])] = parts[1]
    
    return queries


def load_test(file_name):
    queries = []
    with open(file_name, 'rt') as fd:
        for line in fd:
            parts = line.strip().split('\t')
            q_id = int(parts[0])
            docs = eval(parts[1])
            
            queries.append((q_id, docs))
    return queries


def load_train(file_name):
    queries = []
    with open(file_name, 'rt') as fd:
        for line in fd:
            parts = line.strip().split('\t')
            q_id = int(parts[0])
            docs = eval(parts[1])
            clicks = eval(parts[2])
            
            queries.append((q_id, docs, clicks))
    return queries


def copy_model(old, new):
    new.file_name = old.file_name
    new.norm_method = old.norm_method
    new.debug = old.debug
    new.save_normalized = old.save_normalized
    new.title_terms = old.title_terms
    new.body_terms = old.body_terms
    new.term_to_title = old.term_to_title
    new.term_to_body = old.term_to_body
    new.morph = old.morph

    new.N = old.N
    new.title_lengths = old.title_lengths
    new.body_lengths = old.body_lengths
    new.avg_title_length = old.avg_title_length
    new.avg_body_length = old.avg_body_length
    return new
    

eng_text = 'qwertyuiop[]asdfghjkl;\'\zxcvbnm,./'
rus_text = 'йцукенгшщзхъфывапролджэ\ячсмитьбю.'
eng_rus_dict = dict(zip(eng_text, rus_text))

def translate(text):
    out = ''
    for x in text:
        if x in eng_rus_dict:
            out += eng_rus_dict[x]
        else:
            out += x
    return out