from math import gcd
from frozendict import frozendict

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

# Exception raised van invalid permustion was input
class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class DuplicateElement(InputError):
    pass
class MissingElement(InputError):
    pass
class NoElementList(InputError):
    pass
class InvalidItem(InputError):
    pass

##############################################
#### Conversion ##############################
##############################################

def from_image(imagelist):
    '''
    convert a permutation represented as imagelist to the internal representation
    '''
    perm={}
    for k,v in enumerate(imagelist):
        if k!=v-1:
            perm[k+1]=v
    return(frozendict(perm))

def from_cycle(cyclelist):
    '''
    convert a permutation represented as cyclelist to the internal representation
    '''
    perm={}
    for cycle in cyclelist:
        p=cycle[-1]
        for e in cycle:
            perm[p]=e
            p=e
    return(frozendict(perm))

def to_cycle(perm):
    '''
    convert a permutation from its internal representation to a cycle list
    '''

    cycles=[]
    mydict=dict(perm)
    for k in sorted(list(mydict)):
        nextelement=k
        cycle=[]
        while mydict[nextelement]!=0:
            thiselement=nextelement
            nextelement=mydict[thiselement]
            cycle.append(thiselement)
            mydict[thiselement]=0
        if len(cycle)>0:
            cycles.append(tuple(cycle))
    return(tuple(cycles))

def to_image(perm):
    '''
    convert a permutation from its internal representation to an image list
    '''
    if perm==identity():
        return(())
    image=[i+1 for i in range(max(perm))]
    for k,v in perm.items():
        image[k-1]=v 
    return(tuple(image))



##############################################
#### Input - Ouput (slow) ####################
##############################################

def check_imagelist(imagelist):
    ''' 
    checks if input is a valid imagelist.
    an list or tuple is a valid imagelist if it is the 
    permutation of 1,...,n for a positive integer n
    '''
    if not (isinstance(imagelist,list) or isinstance(imagelist,tuple)):
        raise NoElementList(imagelist, "'is not a list or tuple")
    sorted_imagelist=sorted(imagelist)
    for v in imagelist:
        if not isinstance(v,int):
            raise InvalidItem(imagelist, "'%s' is not an integer"%v)
        if v<=0:
            raise InvalidItem(imagelist, "'%d' is not a positive integer"%v)
    first=True
    for item in sorted_imagelist:
        if first:
            last_item=item
            first=False
        else:
            if item==last_item:
                raise DuplicateElement(imagelist, "duplicate value '%d'"%item)
            last_item=item    
    for i,v in enumerate(sorted_imagelist):
        if i+1 != v:
            raise MissingElement(imagelist, "'missing value %d"%(i+1))
    return

def check_cyclelist(cyclelist):
    ''' 
    checks if input is a valid cycle list.
    an list or tuple is a valid cycle list if is a list or tuple
    of cyclelist. A cyle is a list or tupble of positive integers
    to cycles mcannot have a number in common.
    '''
    if not (isinstance(cyclelist,list) or isinstance(cyclelist,tuple)):
        raise NoElementList(cyclelist, "'is not a list or tuple")
    itemlist=[]
    for cycle in cyclelist:
        if not (isinstance(cycle,list) or isinstance(cycle,tuple)):
            raise InvalidItem(cyclelist, "'%s' is not a list or tuple"%(cycle))
        if cycle==[] or cycle==():
            raise InvalidItem(cyclelist,"'%s' is an empty  list or tuple"%(str(cycle)))

        for item in cycle:
            if not isinstance(item,int):
                raise InvalidItem(cyclelist,"'%s' is not an integer"%(item))
            elif item<=0:
                raise InvalidItem(cyclelist,"'%s' not a positive integer"%(item))
        itemlist.extend(cycle)
    itemlist.sort()
    first=True
    found=False
    for item in itemlist:
        if first:
            last_item=item
            first=False
        else:
            if item==last_item:
                duplicate=item
                found=True
                break
            last_item=item
    if found:
        invalidlist=[]
        for cycle in cyclelist:
            if duplicate in cycle:
                invalidlist.append(cycle)
        raise DuplicateElement(cyclelist,"the cycles %s contain the duplicate value %s"%(invalidlist,duplicate))
    return
    # is_cyclelist([[1, 2, 3], [11, 8, 9, 7], [4, 5]])

def to_permutation(*args):
    '''
    convert the arguments to a permutation
    args are some integers, then the list of these integers should be interpreted as imagelist
    if args are some lists or tuples of integers, than these lists or tuples should be interpreted as check_cyclelist'''
    if not args:
        # empy to_permutation
        return(from_image([]))
    if isinstance(args[0],int):
        check_imagelist(args)
        return from_image(args)
    if isinstance(args[0],list) or isinstance(args[0],tuple):
        check_cyclelist(args)
        return from_cycle(args)
    raise InvalidItem(args,"invalid item '%s')%str(args[0])")


################################################
#### Operation and Calculations ################
#### depending of internal representation ######
################################################

def identity():
    ''' 
    returns the identity permutation
    '''
    return(frozendict({}))

def compose(perm1, perm2):
    '''
    compose(perm1,perm2) calculates perm1 * perm2,
    (perm1 * perm2)(x)=(perm1(perm2(x))), forall x
    '''
    domain=set(perm1).union(set(perm2))
    return frozendict({k : perm1.get(perm2.get(k,k),perm2.get(k,k)) for k in domain if perm1.get(perm2.get(k,k),perm2.get(k,k))!=k})

def invert(perm):
    return (frozendict({v:k for k,v in perm.items()}))

################################################
#### Operation and Calculations ################
#### independing of internal representation ####
################################################


def orderof(perm):
    '''
    returns the order of a permutation
    '''
    # to_cycle(perm):
    first=True
    result=1
    for cycle in to_cycle(perm):
        if first:
            result=len(cycle)
            first=False
        else:
            q=len(cycle) 
            result=result*q//gcd(result,q)
    return result

def powerof(perm,n):
    ''' 
    returns the permutation perm raised to the n-th power
    '''
    if n<0:
        return(powerof(perm,n))
    if n==0:
        return identity()
    if n%2==1:
        return(compose(perm,powerof(perm,n-1)))
    else:
        r=powerof(perm,n//2)
        return(compose(r,r))


################################################
#### Table - Output ############################
################################################


def gen_itemnames1(group):
    '''
    input: a set of permutation that form a group
    output:
        elementlist: list of the elements of the set
            the first element is the identity
            if it wasn't already in group it is added
        symbol:
            a dictionary that contains a printable symbol for each permutation of elementlist
        val: 
            the inverse of symbol:
            val[symbol[perm]])=perm, forall perm in elementlist
    '''
    group=group.copy()
    symbol={}
    val={}
    i=ord('a')
    for g in group:
        if g!=identity():
            if chr(i)=='e':
                i+=1
            if chr(i)==chr(ord('z')+1):
                i=ord('A')
            symbol[g]=chr(i)
            val[chr(i)]=g
            i+=1
        else:
            symbol[g]='e'
            val['e']=g
    symbol[identity()]='e'
    val['e']=identity()
    group.discard(identity())
    elementlist=[identity()]
    elementlist.extend(list(group))
    return((elementlist,symbol,val))
    

def print_group1(elementlist,symbol):
    '''
    elementlist is an iterable of n permutations
    symbol is a dictionary that mpas each permutation or each product of two permutations of elementlist to a printable symbol
    print_group1 pints the n x  n - Caley table of the permutations of element lists
    '''
    line='  |'
    for b in elementlist:
        line+=' '+symbol[b]
    print(line)
    line='--+'
    for b in elementlist:
        line+='-'+'-'
    print(line)
    for a in elementlist:
        line=symbol[a]+' |'
        for b in elementlist:
            line+=' '+symbol[compose(a,b)]
        print(line)

def describe_group1(generators, description):
    '''
    input:
        generators: a list of permutations
        descritption: a title that will be printed out
    output:
        itemdesc:
            a 3-tuple:
                component 1:  the list of elements of the group generated by 'generators', the first element in the list is the identity
                component 2: a dictionary that contains a printable symbol for each permutation of the list in the 1st components
                component 3: the inverse of component 2
            this 3-tuple is similar to the 3-tuple geneated by gen_itemnames1
            
    '''

    assert isinstance(generators,(tuple,list,set))
    assert isinstance(description,str)
    sg=subgroup(generators)
    itemdesc=gen_itemnames1(sg)
    print(description)
    print("Erzeugende:")
    for perm in generators:
        print(itemdesc[1][perm],to_image(perm),to_cycle(perm))
    #print_group1(sg,itemdesc[0],itemdesc[1])
    print_group1(itemdesc[0],itemdesc[1])
    return(itemdesc)
########################################
#### Group Operations
########################################

def subgroup(generators):
    assert isinstance(generators,(list,set,tuple))
    generated=set([identity()])
    fringe=set([identity()])
    i=0
    while fringe:
        i+=1
        new_fringe=set()
        for p1 in generators:
            for p2 in fringe:
                element=compose(p1,p2)
                #print(i,element)
                if element not in generated:
                    generated.add(element)
                    new_fringe.add(element)
        fringe=new_fringe
    return(generated)

def normalizer(generators, group):
    assert generators, (list,set,tuple)
    assert group, (list,set,tuple)
    groupdict={a:invert(a) for a in group}
    normalgroup=set([identity()])
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
        homomorphic_group.add(from_image(imagelist))
    return(homomorphic_group,coset,homomorphism)


p=to_permutation

o=compose
i=invert
e=powerof




examples={}

examples["Z2"]=("Z modulo 2",
[p((1,2))])

examples["Z3"]=("Z modulo 3",
[p((1,2,3))])

examples["Z4"]=("Z modulo 4",
[p((1,2,3,4))])

examples["Z2xZ2"]=("direct product Z2 x Z2",
[p((1,2)),p((3,4))])

examples["S3"]=("permutations of 3 elements",
[p((1,2,3)),p((1,2))])

examples["R2E3SH"]=("Spiegelungen des gleichseitigen Dreiecks",
[p((1,2)),p((1,3)),p((2,3))])

examples["R2E4SD"]=("Spiegelungen des Quadrats um Diagonale",
[p((1,3)),p((2,4))])

examples["R2E4SdSs"]=("Spiegelungen des Quadrats um Diagonale und Seitenhalbierende",
[p((1,3)),p((2,4)),p((1,2),(3,4)),p((1,4),(2,3))])

examples["R2E4SdSsR4"]=("Spiegelungen des Quadrats um Diagonale und Seitenhalbierende und Drehung um 90 Grad",
[p((1,3)),p((2,4)),p((1,2),(3,4)),p((1,4),(2,3)),p((1,2,3,4))])

examples["R3E4R3"]=("Drehung des Teraeders",
[p((1,2,4)),p((2,3,4)),p((1,2,3))])

examples["R3E8R4"]=("Drehung des Würfels",
[p((2,3,4,1),(5,6,7,8)),p((6,7,3,2),(8,4,1,5)),p((1,2,6,5),(7,8,4,3))])


'''
for k,ex in examples.items():
    print()
    descr=describe_group1(ex[1],ex[0])
'''
ex=examples["R3E8R4"]
# descr=describe_group1(ex[1],ex[0])

### checks 
#### convert input
assert p(1,2,3,4,5,6)==identity()
assert p(3,2,1)==p((1,3))
assert p((1,2,3,4,5))==p((2,3,4,5,1))
assert p(3,2,1)==from_image([3,2,1])
assert from_image([3,2,1])==from_image((3,2,1))
assert from_cycle([[1,2,3],[5,6]])==from_cycle([[2,3,1],[6,5]])
assert from_cycle([[1,2,3],[5,6]])==from_cycle([(1,2,3),[5,6]])
assert from_cycle([[1,2,3],[5,6]])==from_cycle(((1,2,3),[5,6]))
assert from_cycle([[1,2,3],[5,6]])==from_cycle([(1,2,3),(5,6)])
assert from_cycle([[1,2,3],[5,6]])==from_cycle(((1,2,3),(5,6)))
assert from_cycle([[1,2,3],[5,6]])==from_cycle(([1,2,3],[5,6]))
assert to_image(from_image((1,3,5,4,2)))==(1,3,5,4,2)
assert to_image(identity())==()
assert to_cycle(identity())==()
assert from_image(())==identity()
assert from_image([])==identity()
assert from_cycle(())==identity()
assert from_cycle([])==identity()
assert to_cycle(from_cycle([[1,2,3],[5,6]]))==((1,2,3),(5,6))
assert to_cycle(from_image(to_image(from_cycle(((1,2),(4,11,9,7),(6,12,5))))))==((1,2),(4,11,9,7),(5,6,12))
assert compose(p((1,2,3),(5,6)),p((2,4),(1,6)))==p((1,5,6,2,4,3))
assert compose(p((1,2,3),(5,6)),identity())==p((1,2,3),(5,6))
assert compose(identity(),p((1,2,3),(5,6)))==p((1,2,3),(5,6))
assert compose(identity(),identity())==identity()
assert invert(p((3,5,7,2),(6,4)))==p((7,5,3,2),(6,4))
assert compose(invert(p((3,5,7,2),(6,4))),p((3,5,7,2),(6,4)))==compose(p((3,5,7,2),(6,4)),invert(p((3,5,7,2),(6,4))))
assert orderof(p((3,5,7,2),(6,4,8)))==12
assert orderof(powerof(p((3,5,7,2),(6,4,8)),2))==6
assert powerof(p((3,5,7,2),(6,4,8)),79)==compose(powerof(p((3,5,7,2),(6,4,8)),23),powerof(p((3,5,7,2),(6,4,8)),56))
assert powerof(p((3,5,7,2),(6,4,8)),12345)==p((3,5,7,2))
assert orderof(identity())==1

subgroup([p((1,2,3,4))])
subgroup(examples["R3E8R4"][1])

print(len(normalizer([examples["R3E8R4"][1][0]],subgroup(examples["R3E8R4"][1]))))
print(len(subgroup(examples["R3E8R4"][1])))

sg=(normalizer([p((1,3),(2,4),(5,7),(6,8))],subgroup(examples["R3E8R4"][1])))
idesc=describe_group1(sg,"normalizer")


sg=subgroup(examples["R3E4R3"][1])
idesc=describe_group1(sg,examples["R3E4R3"][0])

#sg=(normalizer([p((1,2))],subgroup(examples["R3E8R4"][1])))
#idesc=describe_group1(sg,"normalizer")

''' p1='c'
p2='j'
print("subgroup [%s,%s]"%(p1,p2))
t=subgroup([idesc[2][p1],idesc[2][p2]])
t.discard(identity())
ll=[identity()]
ll.extend(t)
print_group1(ll,idesc[1])

idesc=describe_group1([p((1,2)),p((1,3)),p((4,5)),p((4,6))],"arbitrary")
print(len(idesc[0]))
for f in idesc[0]:
    print(orderof(f)) '''

from collections import Counter
print()
cnt=Counter()
sg=subgroup([p((1,2)),p((1,3)),p((1,4)),p((1,5))])
for g in sg:
    cnt[orderof(g)]+=1
for k,v in sorted(cnt.items()):
    print(k,v)
print(len(sg))

#sg=subgroup([p((1,2,3)),p((4,5)),p((1,2))])
#print(len(sg))
#idesc=describe_group1([p((1,2,3)),p((4,5)),p((1,2))],"subgreoup of S5")

sg=subgroup([p((1,2,3,4,5)),p((1,2,3))])
print(len(sg))
for g in sg:
    cnt[orderof(g)]+=1
for k,v in sorted(cnt.items()):
    print(k,v)
print(len(sg))

nl=normalizer([p((6,7))],sg)
qg=quotientgroup(sg,nl)