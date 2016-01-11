import pickle

with open('querry_content.pickle','rb') as f:
    db_q = pickle.load(f)
    
with open('qrels.ohsu.batch.87') as f:
    f = f.readlines()
    for line in f:
        line = line.strip().split('\t')
        db_q[line[0]]['results'][int(line[1])] = int(line[2])
        
    
