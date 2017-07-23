import pymorphy2
import sys

cache = dict()
morph = pymorphy2.MorphAnalyzer()

def norm_word(word):
    if word in cache:
        return cache[word]
    parsed = morph.parse(word)
    if len(parsed) == 0:
        cache[word] = word
        return word
    cache[word] = parsed[0].normal_form    
    return parsed[0].normal_form

def norm_sentence(sentence):
    out = []
    for word in sentence.split(' '):
        out.append(norm_word(word))
    return " ".join(out)

with open(sys.argv[1],"rt") as fd, open(sys.argv[2],"wt") as outd:
    for line in fd:
        parts = line.strip().split('\t')
        if len(parts) == 1:
            parts.extend(["",""])
        if len(parts) == 2:
            parts.append("")
        if len(parts) == 0:
            continue
        print("\t".join([parts[0],norm_sentence(parts[1]),norm_sentence(parts[2])]),file=outd)

        
