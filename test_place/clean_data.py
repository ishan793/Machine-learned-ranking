import pickle

f_error = open('Error_log.txt','w')
def get_vals(doc,c):
    global f
    res = {}
    a = doc.split('\n')
##        Value of flag:
##        0 - irrel
##        1 - id
##        2 - title
##        3 - abst
    flag = ''
    for line in a:
        if flag == 1:
            try:
                res['id'] = int(line.strip())
            except:
                st = 'Error in text: '+line+' '+str(count)
                print st
                print doc
                f_error.write(st)
        elif flag == 2:
            res['title'] = str(line.strip())
        elif flag == 3:
            res['abstract'] = str(line.strip())
        else:
            pass
        if line == '.U':
            flag = 1
        elif line == '.T':
            flag = 2
        elif line == '.W':
            flag = 3
        else:
            flag = 0
    return res

print 'Starting to read text'                
with open('ohsumed.88-91','r') as f:
    count = 0
    res = ''
    temp = []
    f = f.readlines()
    for line in f:
        count += 1
        res += line
        if line[0:2] == '.I':
            temp.append(res)
            res = ''
    temp.append(res)

print 'Cleaning data'
db = {}
temp = temp[1:]
count = 0
for i in temp:
    count += 1
    a = get_vals(i,count)
    new = {}
    for key in a:
        if key != 'id':
            new[key] = a[key]
    try:
        db[a['id']] = new
    except:
        print count

print 'Saving data'
pickle.dump(db,open('test_data.pickle','wb'))
