import pickle

def get_vals(doc):
    a = doc.split('\n')
    flag = 0
    res = {}
    for i in a:
        if flag == 1:
            res['desc'] = i
            flag = 0
        else:
            pass
        if '<desc>' in i:
            flag = 1
        elif '<title>' in i:
            res['title'] = i[8:]
        elif '<num>' in i:
            res['id'] = i[14:]
        else:
            pass
    return res

flag = 0
with open('query.ohsu.1-63','r') as f:
    f = f.readlines()
    st = ''
    res = []
    for line in f:
        if flag == 1:
            st += line
        if line.strip() == '<top>':
            flag = 1
        elif line.strip() == '</top>':
            flag = 0
            res.append(st)
            st = ''
db = {}
for i in res:
    a = get_vals(i)
    temp = {}
    for key in a:
        if key != 'id':
            temp[key] = a[key]
    temp['results'] = {}
    db[a['id']] = temp

with open('qrels.ohsu.batch.87') as f:
    f = f.readlines()
    for line in f:
        line = line.strip().split('\t')
        db[line[0]]['results'][int(line[1])] = int(line[2])
        
with open('querry_content.pickle','wb') as f:
    pickle.dump(db,f)
