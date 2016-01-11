import gensim
import pickle
import random
import math
import time
import math

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
    try:
        res = res/temp
    except ZeroDivisionError:
        return -1
    return res


def transform_bow(docs,q_docs,dct): # add docs
##    # create a duplicate var, because of pythons var passing antics
    print 'Converting docs to bow'
    for d in docs:
        try:
            abst = docs[d]['abstract']
            docs[d]['abstract'] = dct.doc2bow(abst.lower().split())
        except:
            # we do nothing here, what you see below is absolutely the whim of a whimsical mind
            tuiy = 2
        tit = docs[d]['title']
        docs[d]['title'] = dct.doc2bow(tit.lower().split())

    print 'Converting Querries to bow'

    for d in q_docs:
        try:
            title = q_docs[d]['title']
            desc = q_docs[d]['desc']
        except:
            print str(q_docs[d]),'Error ocurred'
        q_docs[d]['title'] = dct.doc2bow(title.lower().split())
        q_docs[d]['desc'] = dct.doc2bow(desc.lower().split())


def load_model(n = 128,t = 'tfidf',id = 5):
    mod_name = 'data/models/'
    if t == 'tfidf':
        mod_name += str(t)+'_'+str(id)
        mod = gensim.models.TfidfModel.load(mod_name)
    elif t == 'hdp':
        mod_name += str(t)+'_'+str(id)
        mod = gensim.models.HdpModel.load(mod_name)
    elif t == 'lda':
        mod_name += str(t)+'_'+str(n)+'_'+str(id)
        mod = gensim.models.LdaModel.load(mod_name)
    elif t == 'lsi':
        mod_name += str(t)+'_'+str(n)+'_'+str(id)
        mod = gensim.models.LsiModel.load(mod_name)
    return mod

def bow2mod(docs, q_docs, mod):
    for d in docs:
        temp = {}
        try:
            abst = docs[d]['abstract']
            docs[d]['abstract'] = mod[abst]
        except:
            poi = 2
        tit = docs[d]['title']
        docs[d]['title'] = mod[tit]
      
    for d in q_docs:
        tit = q_docs[d]['title']
        desc = q_docs[d]['desc']
        q_docs[d]['title'] = mod[tit]
        q_docs[d]['desc'] = mod[desc]

def get_data(mode = 'train',t_ = 'tfidf',n_ = 64):
    if mode == 'train':
        docs_direc = 'data/bow/train_docs_bow_5'
        q_direc = 'data/bow/q_bow_5'
        dct_direc = 'data/dcts/dict5'
        
        print 'Loading Dictionary'
        dct = gensim.corpora.Dictionary.load(dct_direc)
        
        print 'Loading Model',str(t_),str(n_)
        mod = load_model(t = t_,n = n_)
        
        print 'Loading Data from',str(docs_direc)
        with open(docs_direc,'rb') as f:
            d = pickle.load(f)

        print 'Loading querries from',str(q_direc)
        with open(q_direc,'rb') as f:
            q = pickle.load(f)

    else:
        docs_direc = 'data/raw/test_docs_stemmed.pickle'
        q_direc = 'data/raw/test_querry_results_stemmed.pickle'
        dct_direc = 'data/dcts/dict5'
    
        print 'Loading Dictionary'
        dct = gensim.corpora.Dictionary.load(dct_direc)
    
        print 'Loading Model',str(t_),str(n_)
        mod = load_model(t = t_,n = n_)
        
        print 'Loading Data from',str(docs_direc)
        with open(docs_direc,'rb') as f:
            d = pickle.load(f)

        print 'Loading querries from',str(q_direc)
        with open(q_direc,'rb') as f:
            q = pickle.load(f)

        print 'Creating bow'
        transform_bow(d,q,dct)
        
    return d,q,mod
