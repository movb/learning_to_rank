import sys

docs_set = set()
broken_set = set()
with open(sys.argv[1],'rt') as fs:
    for line in fs:
        parts = line.strip().split('\t')
        if len(parts) == 0:
            print("Empty line")
            continue
        if len(parts) != 3:
            print("Broken id: {}".format(int(parts[0])))
            broken_set.add(int(parts[0]))
            
        docs_set.add(int(parts[0]))

docs_normed_set = set()
broken_normed_set = set()
with open(sys.argv[2],'rt') as fs:
    for line in fs:
        parts = line.strip().split('\t')
        if len(parts) == 0:
            print("Normed Empty line")
            continue
        if len(parts) != 3:
            print("Broken normed id: {}".format(int(parts[0])))
            broken_normed_set.add(int(parts[0]))

        docs_normed_set.add(int(parts[0]))

with open(sys.argv[3],'wt') as fs:
    for doc_id in docs_set.difference(docs_normed_set):
        print(doc_id,file=fs)

with open(sys.argv[4],'wt') as fs:
    for doc_id in broken_set:
        print(doc_id,file=fs)

with open(sys.argv[5],'wt') as fs:
    for doc_id in broken_normed_set:
        print(doc_id,file=fs)
