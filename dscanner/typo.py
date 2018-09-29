import tldextract

#missing-dot typos : www.example.com -> wwwexample.com
def mis_dot(prs,sd,lpsp):
    misd=[]

    if prs != "":
        td = prs+sd+"."+lpsp
        misd.append(td)
        
    return misd

#omission typos: www.example.com -> www.exmple.com
def char_omi(prs,sd,lpsp):
    base = sd
    omi=[]

    if len(base)>1:
        for i in range(len(base)):
            str_del = list(base)
            del str_del[i]      #対象インデックスの削除
            o = "".join(str_del)
            od = prs+"."+o+"."+lpsp
            omi.append(od)
                
    return omi

#permutation typos : www.example.com -> www.examlpe.com
def char_permu(prs,sd,lpsp):
    base = sd
    permu=[]
    
    for i in range(len(base)):

        if i == len(base)-1:
            break
    
        tmp = base

        if base[i+1] != base[i]:
            start = base[:i]
            middle = base[i+1] + base[i]  #文字の入れ替え
            last = base[i+2:]
            p= start + middle +last
            pd =prs+"."+p+"."+lpsp
            permu.append(pd)

    return permu

#replacement typos : www.example.com -> www.ezample.com
def char_replace(prs,sd,lpsp,next_key):

    base = sd
    rep=[]
    for i in range(len(base)):
        nk=next_key[base[i]]

        for s in nk:
            start = base[:i]
            middle = s       #対象キーの隣接キーに置換
            last = base[i+1:]
            p= start + middle +last
            pd =prs+"."+p+"."+lpsp
            rep.append(pd)
    return rep

#insertion typos: www.example.com -> www.exxample.com
def char_insert(prs,sd,lpsp,next_key):
    base = sd
    ins = []
    
    for i in range(len(base)):
        klist=next_key[base[i]]

        dk=base[:i]+base[i]+base[i]+base[i+1:] #対象キーそのものを挿入 www.exxample.com
        br = prs+"."+dk+"."+lpsp
        ins.append(br)
        
        for s in klist:
            start = base[:i]
            middle = base[i]+s   #対象キーの隣接キーを挿入  www.exzample.com
            last = base[i+1:]
            p= start + middle +last
            pd =prs+"."+p+"."+lpsp
            ins.append(pd)
        
    return ins


def deldot(domain):
    res=[]

    for i in domain:
        if i[0] == ".":
            res.append(i[1:])
        else:
            res.append(i)

    return res


def near_urls(domain):
    
    #QWERTY配列における各キーに隣接するキーの辞書    
    next_key={'q':['w','a','1','2'],'w':['q','e','s','a','2','3'],'e':['w','s','d','r','3','4'],'r':['e','d','f','t','4','5'],'t':['r','f','g','y','5','6'],'y':['t','g','h','u','6','7'],'u':['y','h','j','i','7','8'],'i':['u','j','k','o','8','9'],'o':['i','k','l','p','9','0'],'p':['o','l'],'a':['q','w','s','z'],'s':['w','e','d','x','z','a'],'d':['e','r','f','c','x','s'],'f':['r','t','g','v','c','d'],'g':['t','y','h','b','v','f'],'h':['y','u','j','n','b','g'],'j':['u','i','k','m','n','h'],'k':['i','o','l','m','j'],'l':['o','p','k'],'z':['a','s','x'],'x':['z','s','d','c'],'c':['x','d','f','v'],'v':['c','f','g','b'],'b':['v','g','h','n'],'n':['b','h','j','m'],'m':['n','j','k'],'-':['0','p'],'1':['1','2','q'],'2':['1','q','w','3'],'3':['2','w','e','4'],'4':['3','e','r','5'],'5':['4','r','t','6'],'6':['5','t','y','7'],'7':['6','y','u','8'],'8':['7','u','i','9'],'9':['8','i','o','0'],'0':['9','o','p','-']}
    
    typo_domain=[]
    
    if "http://" in domain:
        domain=domain.replace("http://","")

    if "https://" in domain:
        domain=domain.replace("https://","")

    
    ext = tldextract.extract(domain)
    prs = ext.subdomain
    sd = ext.domain
    lpsp = ext.suffix

    
    typo_domain.extend(mis_dot(prs,sd,lpsp))
    typo_domain.extend(char_omi(prs,sd,lpsp))
    typo_domain.extend(char_permu(prs,sd,lpsp))
    typo_domain.extend(char_replace(prs,sd,lpsp,next_key))
    typo_domain.extend(char_insert(prs,sd,lpsp,next_key))

    typo_domain = sorted(list(set(typo_domain)))  #重複削除とソート

    if prs == "":
        typo_domain = deldot(typo_domain)
        #subdomainがない場合、最初にドットがついてしまうので、それを削除

    return typo_domain



if __name__ == '__main__':

    domain="https://www.example.com"
    result=[]
    result=near_urls(domain)

    for i in result:
        print(i)
