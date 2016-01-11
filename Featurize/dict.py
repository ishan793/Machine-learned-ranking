import gensim
import string
import pickle
import nltk.stem as ns

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don\'t', 'should', 'now']
stop_words += [str(i) for i in range(500)]
stop_words += ['p','also','less','per','percent','year','one','hundred','two','may','might','could','two','three','four','five','six','seven','nine','ten','patients','effect','effects','patient']


def get_docs(docs,q_docs):
    res = []
    for d in docs:
        try:
            temp = docs[d]['abstract']
            res.append(str(temp))
        except:
            poi = 2
        q = docs[d]['title']
        res.append(str(q))
      
    for d in q_docs:
        try:
            temp = q_docs[d]['title']
            q = q_docs[d]['desc']
        except:
            print d
        res.append(str(temp))
        res.append(str(q))
    return res

def make_dictionary(docs,stoplist,lower_freq = 1,save_direc = 'f_name'):
    # collect statistics about all tokens
    dictionary = gensim.corpora.Dictionary(d.lower().split() for d in docs)
    # remove stop words and words that appear only once
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq <= lower_freq]
    dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
    dictionary.compactify()
    dictionary.save(save_direc)
    return dictionary

docs_direc = 'data/raw/ohsumed_docs_stemmed.pickle'
q_direc = 'data/raw/querry_content_stemmed.pickle'
dct_direc = 'data/dcts/dict'

print 'Loading Data'
with open(docs_direc,'rb') as f:
    d = pickle.load(f)

print 'Loading querries'
with open(q_direc,'rb') as f:
    q = pickle.load(f)

print 'Getting docs'
docs = get_docs(d,q)
print len(docs)

stemmer = ns.PorterStemmer()
stop_list = []
for w in stop_words:
    stop_list.append(stemmer.stem(w))

for i in range(1,6):
    print 'Making dictionary for i =',str(i)
    direc = dct_direc+str(i)
    dct = make_dictionary(docs,stop_list,i,direc)
    print dct

