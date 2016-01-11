import gensim
import string
import pickle

def transform_bow(docs,q_docs,dct,i): # add docs
##    # create a duplicate var, because of pythons var passing antics
    res_docs = {}
    print 'Storing docs as bow'
    for d in docs:
        res_docs[d] = {}
        try:
            abst = docs[d]['abstract']
            res_docs[d]['abstract'] = dct.doc2bow(abst.lower().split())
        except:
            # we do nothing here, what you see below is absolutely the whim of a whimsical mind
            tuiy = 2
        tit = docs[d]['title']
        res_docs[d]['title'] = dct.doc2bow(tit.lower().split())
    print 'Actually Storing'
    temp = 'test_docs_bow_'+str(i)
    with open(temp,'wb') as f:
        pickle.dump(res_docs,f)
    
    res_q_docs = {}
    for d in q_docs:
        res_q_docs[d] = {}
        try:
            title = q_docs[d]['title']
            desc = q_docs[d]['desc']
        except:
            print q_docs[d]
        res_q_docs[d]['title'] = dct.doc2bow(title.lower().split())
        res_q_docs[d]['desc'] = dct.doc2bow(desc.lower().split())
        res_q_docs[d]['results'] = q_docs[d]['results']

    temp = 'test_q_bow_'+str(i)
    with open(temp,'wb') as f:
        pickle.dump(res_q_docs,f)


docs_direc = 'data/raw/test_docs_stemmed.pickle'
q_direc = 'data/raw/test_querry_results_stemmed.pickle'
dct_direc = 'data/dcts/dict'


print 'Loading Data from',str(docs_direc)
with open(docs_direc,'rb') as f:
    d = pickle.load(f)

print 'Loading querries from',str(q_direc)
with open(q_direc,'rb') as f:
    q = pickle.load(f)

for i in range(5,6):
    dct_d = dct_direc+str(i)
    print dct_d
    dct = gensim.corpora.Dictionary.load(dct_d)
    # print dct
    transform_bow(d,q,dct,i)

