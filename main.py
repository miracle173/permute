from itertools import chain

def compose(imagelist1,imagelist2):
    # stretch smaller imagelist
    if len(imagelist1)==len(imagelist2):
        il1=imagelist1
        il2=imagelist2
    elif len(imagelist1)<len(imagelist2):
        il1=[imagelist1[i] if i<len(imagelist1) else i for i in range(len(imagelist2))]
        il2=imagelist2
    elif len(imagelist2)<len(imagelist1):
        il1=imagelist1
        il2=[imagelist2[i] if i<len(imagelist2) else i for i in range(len(imagelist1))]
    # compose lists
    result=[0]*len(il1)
    for i in range(len(il1)):
        result[i]=il2[il1[i]-1]
    plen=len(result)
    for i in range(len(result)-1,-1,-1):
        if result[i]==i+1:
            plen=i
        else:
            break
    return(tuple(result[:plen]))

def is_imagelist(imagelist):
    return(sorted(imagelist)==list(range(1,len(imagelist)+1)))

def is_cyclelist(cyclelist):
    l=list(chain.from_iterable(cyclelist))
    l.sort()

    

def cycleform(imagelist):
    g=imagelist[:]
    cyclelist=[]
    for i in range(len(g)):
        #print("0:",i)
        cycle=[]
        t=i+1
        while g[t-1]!=0:
            #print("1:",t,g[t-1])
            cycle.append(t)
            hold=g[t-1]
            g[t-1]=0
            t=hold
            #print("2:",t,g[t-1])
        #print("9:",cycle)
        if len(cycle)>1:
            cyclelist.append(cycle[:])
    return(cyclelist)

def imageform(cyclelist):
    imagelist=[]
    for cycle in cyclelist:
        p=cycle[-1]
        for e in cycle:
            if p>len(cycle):
                imagelist.extend([0]*(p-len(imagelist)))
            imagelist[p-1]=e
            p=e
    for i in range(len(imagelist)):
        if imagelist[i]==0:
            imagelist[i]=i+1
    return(imagelist)

def dict_from_cycleform(cyclelist):
    permdict={}
    for cycle in cyclelist:
        p=cycle[-1]
        for e in cycle:
            permdict[p]=e
            p=e
    return(permdict)

def dict_from_imageform(imagelist):
    permdict={}
    for i in range(len(imagelist)):
        if imagelist[i]!=i+1:
            permdict[i+1]=imagelist[i]
    return(permdict)
  





class permutation(object):
    def __init__(self,data):
        if isinstance(data,list):
            pass
        elif isinstance(data, permutation):
            pass

p=[5,7,2,1,3,4,6]
#p=[1,2,3,4,5,6,7]
print(p) 
print(cycleform(p))

c=[[2,3,4],[6,7]]
print(imageform(c))

p1=[2,1,3,4]
p2=[4,3,2,1]
print()
print(p1)
print(p2)
print(compose(p1,p2))
print(compose(p2,p1))
print(compose(p1,p1))
print(compose(p,p2))
print(compose(p2,p))