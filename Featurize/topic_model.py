import gensim
import string
import pickle
import random

def make_model(docs,dct,typ = 'lda',n = None):
    if typ == 'lda':
        model = gensim.models.ldamodel.LdaModel(docs,id2word = dct,num_topics = n)
    elif typ == 'hdp':
        model = gensim.models.hdpmodel.HdpModel(docs,id2word = dct)
    elif typ == 'lsi':
        temp = gensim.models.tfidfmodel.TfidfModel(docs)
        tf_idf_docs = temp[docs]
        model = gensim.models.lsimodel.LsiModel(tf_idf_docs,id2word = dct, num_topics = n)
    elif typ == 'tfidf':
        model = gensim.models.tfidfmodel.TfidfModel(docs)
    return model

def compute_sim(a,b):
    x = {}
    for i in a:
        x[i[0]] = i[1]
    y = {}
    for i in b:
        y[i[0]] = i[1]

    res = 0
    norm_x = 0
    for i in x:
        norm_x += x[i]*x[i]
        if i in y:
            res += x[i]*y[i]
    norm_y = 0
    for i in y:
        norm_y += y[i]*y[i]
    temp = (norm_x*norm_y)**0.5
    res = res/temp
    return res

def get_docs(docs,q_docs):
    
    all_docs = []
    # make corpus
    print 'Adding documents to list'
    for d in docs:
        try:
            temp = docs[d]['abstract']
            q = docs[d]['title']
            all_docs.append(temp)
        except:
            q = docs[d]['title']
        all_docs.append(q)
        
    # add to corpus
    print 'Adding querries to list'
    for d in q_docs:
        try:
            temp = q_docs[d]['title']
            q = q_docs[d]['desc']
        except:
            print d
    all_docs.append(temp)
    all_docs.append(q)
    return all_docs

# ------------- actual ------------- #
ind = 5
doc_name  = 'data/bow/train_docs_bow_'+str(ind)
q_name = 'data/bow/q_bow_'+str(ind)
dct_direc = 'data/dcts/dict'+str(ind)

print 'Loading Documents'
with open(doc_name) as f:
    docs = pickle.load(f)

print 'Loading Querries'
with open(q_name,'rb') as f:
    q_docs = pickle.load(f)

data = get_docs(docs,q_docs)
dct = gensim.corpora.Dictionary.load(dct_direc)
# mod = gensim.models.TfidfModel(data)
# mod.save('./data/models/tfidf_'+str(ind))

typ = 'lsi'
n = 100
mod_save = './data/models/'+str(typ)+'_'+str(n)+'_'+str(ind)
print 'Making model'
mod = make_model(data,dct,typ,n)
print 'Saving to',str(mod_save)
mod.save(mod_save)



