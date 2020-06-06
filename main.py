from itertools import chain
def normalize(imagelist):
    plen=len(imagelist)
    for i in range(len(imagelist)-1,-1,-1):
        if imagelist[i]==i+1:
            plen=i
        else:
            break
    return(tuple(imagelist[:plen]))

def compose(imagelist1,imagelist2):
    # stretch smaller imagelist
    if len(imagelist1)==len(imagelist2):
        il1=imagelist1
        il2=imagelist2
    elif len(imagelist1)<len(imagelist2):
        il1=[imagelist1[i] if i<len(imagelist1) else i+1 
            for i in range(len(imagelist2))]
        il2=imagelist2
    elif len(imagelist2)<len(imagelist1):
        il1=imagelist1
        il2=[imagelist2[i] if i<len(imagelist2) else i+1 
            for i in range(len(imagelist1))]
    # compose lists
    result=[0]*len(il1)
    for i in range(len(il1)):
        #result[i]=il2[il1[i]-1]
        result[i]=il1[il2[i]-1]
    return(normalize(result))

def invert(imagelist):
    l=[(imagelist[i],i) for i in range(len(imagelist))]
    l.sort()
    return(normalize(tuple(t[1]+1 for t in l)))

def exponentialize(imagelist,n):
    if n<0:
        return(exponentialize(invert(imagelist),-n))
    elif n==0:
        return(())
    else:
        result=exponentialize(imagelist,n//2)
        result=compose(result,result)
        if n%2==1:
            result=compose(result,imagelist)
        return(tuple(result))
                
    
def is_imagelist(imagelist):
    return(sorted(imagelist)==list(range(1,len(imagelist)+1)))

def is_cyclelist(cyclelist):
    if [item for item in cyclelist if (True if not isinstance (item,int) else item<=0)]:
        return False
    l=[item for sublist in cyclelist for item in sublist]
    return len(l)==len(set(i))

def is_dictrepr(dictperm):
    pass

def from_imageform(imagelist):
    perm={}
    for k,v in enumerate(imagelist):
        if k!=i-1:
            perm[k]=i
    return(perm)

def from_cycleform(cyclelist):
    perm={}
    for cycle in cyclelist:
        p=cycle[-1]
        for e in cycle:
            perm[p]=e
            p=e
    return(perm)

def cycleform(imagelist):
    g=list(imagelist[:])
    cyclelist=[]
    for i in range(len(g)):
        cycle=[]
        t=i+1
        while g[t-1]!=0:
            cycle.append(t)
            hold=g[t-1]
            g[t-1]=0
            t=hold
        if len(cycle)>1:
            cyclelist.append(tuple(cycle[:]))
    return(tuple(cyclelist))

def imageform(cyclelist):
    imagelist=[]
    for cycle in cyclelist:
        p=cycle[-1]
        for e in cycle:
            if p>len(imagelist):
                imagelist.extend([0]*(p-len(imagelist)))
            imagelist[p-1]=e
            p=e
    for i in range(len(imagelist)):
        if imagelist[i]==0:
            imagelist[i]=i+1
    return(tuple(imagelist))
    #imageform([[1,2,3]])

def subgroup(generators):
    generated=set([()])
    fringe=set([()])
    i=0
    while fringe:
        new_fringe=set()
        for p1 in generators:
            for p2 in fringe:
                element=compose(p1,p2)
                #print(p1,p2,element)
                if element not in generated:
                    generated.add(element)
                    new_fringe.add(element)
        fringe=new_fringe
    return(generated)

def normalizer(generators, group):
    groupdict={a:invert(a) for a in group}
    normalgroup=set([()])
    fringe=subgroup(generators).difference(normalgroup)
    while fringe:
        normalgroup=normalgroup.union(fringe)
        new_fringe=normalgroup.copy()
        for (g,invg) in groupdict.items():
            for f in fringe:
                new_fringe.add(compose(compose(g,f),invg))

        fringe=subgroup(new_fringe).difference(normalgroup)
    return(normalgroup)

def centralizer(group):
    groupdict={a:invert(a) for a in group}
    centralgroup=set() 
    for (a,inva) in groupdict.items():
        for (b,invb) in groupdict.items():
            centralgroup.add(compose(compose(a,b),compose(inva,invb)))
    return(centralgroup)

def quotientgroup(group, normalgroup):
    homomorphism={}
    coset=[]
    mygroup=group.copy()
    #first=True
    while mygroup:
        # if not first:
        #     g=mygroup.pop()
        # else:
        #     first=False 
        #     g=()
        g=mygroup.pop()
        coset.append({compose(g,n) for n in normalgroup})
        k=len(coset)
        homomorphism.update({x:k for x in coset[-1]})
        mygroup=mygroup.difference(coset[-1])
    homomorphic_group=set()
    for coset_a in coset:
        imagelist=[]
        for a in coset_a:
            break
        for coset_b in coset:
            for b in coset_b:
                break
            imagelist.append(homomorphism[compose(a,b)])
        homomorphic_group.add(normalize(imagelist))
    return(homomorphic_group,coset,homomorphism)


p=imageform
c=cycleform
o=compose
i=invert
e=exponentialize


sg=subgroup([(2,1,4,5,6,7,3)]) #10
print("subgroup:",sg)
print("of order:",len(sg))
print("center:",centralizer(sg))
sg=subgroup([(2,1,5,4,3,6),(6,2,3,4,5,1)]) #12
print("subgroup:",sg)
print("of order:",len(sg))
print("center:",centralizer(sg))

sg=subgroup([(2,1,5,4,6,3),(8,2,3,4,5,6,7,1)]) #18

print("subgroup:",sg)
print("of order:",len(sg))
nl=normalizer([(2, 1)],sg) #6
print("normalizer:",nl) 
print("of order:",len(nl))
fg=quotientgroup(sg,nl)
print("factorgroup:",fg[0])
nl=normalizer([(1, 2, 5, 4, 6, 3)],sg) #3
print("normalizer:",nl) 
print("of order:",len(nl))
fg=quotientgroup(sg,nl)
print("factorgroup:",fg[0])
nl=normalizer([(2, 8, 5, 4, 6, 3, 7, 1)],sg) #9
print("normalizer:",nl) 
print("of order:",len(nl))
nl=normalizer([(2, 1)],sg) #9
print("normalizer:",nl) 
print("of order:",len(nl))
#print(normalizer([(6, 2, 3, 4, 5, 1)],sg)) #12

#c(o(p(((2,1),)),o(p(((3,1),)),o(p(((4, 1),)),p(((1, 2, 3, 4),))))))
#c(o(p(2,1),p(3,1),p(4,1),p(1,2,3,4))
print("center:",centralizer(sg))

sg=subgroup([p([(1,2)]),p([(1,3)]),p([(1,4)])])
print(len(sg))
cl=centralizer(sg)
print("center:",len(cl))
fg=quotientgroup(sg,cl)
print("factorgroup:",fg[0])