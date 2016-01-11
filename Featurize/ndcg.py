import math

def compute_dcg(ranking):
    res = ranking[0]
    temp = []
    temp.append(ranking[0])
    n = len(ranking)
    for i in range(1,n):
        num = (ranking[i])
        den = math.log(1+i,2)
        temp.append(num/den)
        res += num/den
    return res

def get_ndcg(a,q_res,n=None): # (q, docs, n_ = 10):
    
    sorted_a = sorted(a.items(), key = lambda b:b[1])
    temp = []
    if n == None:
        n = len(sorted_a)
    for i in range(n):
        temp.append(sorted_a[n-i-1])
    sys_ranking = []
    for i in temp:
        key = i[0]
        if key in q_res:
            sys_ranking.append(q_res[key])
        else:
            sys_ranking.append(0)
    sys_score = compute_dcg(sys_ranking)
    if sys_score == 0:
        return 0
    #sys_ranking = sorted(sys_ranking, reverse = True)
    ideal_ranking = sorted(q_res.items(), key = lambda b:b[1], reverse = True)
    temp = []
    for i in range(n):
        try:
            temp.append(ideal_ranking[i][1])
        except IndexError:
            temp.append(sys_ranking[i])
    
    ideal_score = compute_dcg(temp)
    res = sys_score/ideal_score
    return res
q_res = {90366836: 1, 90225921: 2, 90004738: 1, 90246659: 2, 90199428: 1, 89118853: 1, 90362116: 1, 91255745: 1, 89150892: 1, 89259146: 1, 91058368: 2, 91064589: 1, 88051601: 1, 89178898: 2, 91327507: 1, 91108884: 1, 91223317: 1, 88271257: 2, 88245402: 1, 91121051: 1, 89347868: 2, 91223327: 2, 88286880: 1, 90064880: 1, 91062947: 1, 89293732: 2, 90275878: 2, 91215404: 1, 91374642: 1, 88164275: 1, 91247113: 1, 90196474: 1, 89194681: 2, 89170112: 1, 90191520: 2, 91039556: 1, 89201734: 1, 88067911: 1, 91249224: 1, 88276078: 1, 90182092: 1, 88164173: 1, 89280077: 1, 88302928: 1, 88108497: 1, 91206627: 1, 91249250: 1, 89073622: 2, 91283663: 1, 90355293: 1, 88265695: 1, 88223968: 2, 91003233: 1, 88205922: 1, 89190627: 1, 91157348: 2, 91003217: 2, 90258152: 2, 89268073: 2, 88105965: 2, 90116078: 2, 91283711: 1, 91241456: 1, 91281649: 1, 90283636: 2, 90294389: 1, 88230648: 2, 91234977: 2, 89089018: 2, 88324735: 1, 90123388: 1, 91237884: 1, 90029310: 1, 90366847: 1}
ret_res = {91255745: 0.679573557006969, 91028610: 0.6026743715369246, 88161929: 0.6757505811313486, 88063116: 0.5505686668304093, 89060631: 0.5509538364420478, 91003233: 0.5597351090819518, 90063916: 0.6538883297726849, 91351665: 0.8150335809716162, 88164275: 0.5964921474175612, 91283711: 0.6105318804125035}

for i in range(1,11):
    print str(i),str(get_ndcg(ret_res,q_res,i))