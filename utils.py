import pickle


class DocWrap():
    def __init__(self, file_name, index_file):
        self.fd = open(file_name,'rt')
        self.index = load_from_file(index_file)
    
    def get(self, doc_id):
        return get_document(self.fd, self.index, doc_id)
        

def build_index(data_file, max_lines=None):
    documents = {}
    with open(data_file, "rt") as fd:
        pos=0
        line_num = 0
        #for line_num, line in enumerate(fd):
        while True:
            line = fd.readline()
            if not line:
                break
        
            parts = line.strip().split('\t')
            doc_id = int(parts[0])

            documents[doc_id] = pos          
            pos = fd.tell()
            
            line_num += 1
            if max_lines and max_lines==line_num:
                break
    
    return documents

def get_document(fd, index, doc_id):
    pos = index[doc_id]
    fd.seek(pos)
    line = fd.readline()
    parts = line.strip().split('\t')
    
    if len(parts) <= 1:
        return "" , ""
    elif len(parts) == 2:
        return parts[1], ""
    
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


stop_words = [
    'и', 'в', 'во', 'не', 'он', 'на', 'я', 'с',
    'что', 'как', 'когда', 'где', 'кто', 'куда',
    'со', 'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за',
    'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему',
    'теперь', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него',
    'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может',
    'они','тут', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их',
    'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под',
    'будет', 'ж', 'тогда', 'этот', 'того', 'потому', 'этого','какой', 'совсем','ним',
    'здесь', 'этом', 'один','почти', 'мой','тем', 'чтобы', 'нее', 'сейчас', 'были',
    'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой', 'хоть',
    'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего','них',
    'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою','этой', 'перед','иногда',
    'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю', 'между' ]