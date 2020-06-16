'''
14.6.
added 
subgroupX
'''
DEBUGPRINT=False

compose_count=0

from math import gcd
from frozendict import frozendict
from random import seed, shuffle

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
    global compose_count
    compose_count+=1
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
    input:
        'perm': 
            a permutation (internal representation)
        'n': 
            an integer
    output:
        return: 
            the permutation perm raised to the n-th power
    '''
    if n<0:
        return(invert(powerof(perm,-n)))
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
    input: 
        'group': a set of permutation that form a group
    output:
        return: a 3-tuple
            c1: (elementlist) list of the elements of the set
                the first element is the identity
                if it wasn't already in group it is added
            c2: (symbol)
                a dictionary that contains a printable symbol for each permutation of elementlist
            c3: (val) 
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
    'elementlist': 
        is an iterable of n permutations
    'symbol': 
        is a dictionary that mpas each permutation or each product of two permutations of elementlist to a printable symbol
    output: None
    sideeffects:
        print_group1 prints the n x  n - Caley table of the permutations of element lists
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
        'generators': 
            a list of permutations
        'descritption': 
            a title that will be printed out
    output:
        return:
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

def extract_integer(expr):
    s=1
    ls=0
    for c in expr:
        if c=='-':
            s*=-1
            ls+=1
        else:
            break
    n=0
    ln=0
    for c in expr[ls:]:
        if ord('0')<= ord(c)<=ord('9'):
            n*=10
            n+=int(c)
            ln+=1
        else:
            break
    if ln==0:
        n=s
    else:
        n*=s
    return((expr[:ls+ln],expr[ls+ln:],n))

def print_error(expr,pos):
    print("error")
    print(expr) 
    print(' '*(pos-1)+'^')

def calc_expression(expr,val):
    if DEBUGPRINT:
        print("calc_expression ==> '"+expr+"'" )
    if expr=='':
        if DEBUGPRINT:
            print("parse ==> ''")
            print("    finished")
        return (True,identity(),0,'')
    if expr[0]=='(':
        level=0
        pstack=[]
        for i,c in enumerate(expr):
            if c==')':
                level-=1
                pstack.pop()
            if c=='(':
                level+=1
                pstack.append(i)
            if level==0:
                break
        if level>0:
            return (False,None,pstack.pop()+1,'missing closing )')
        else:  
            nxtr=extract_integer(expr[i+1:])
            if DEBUGPRINT:
                print("    part 1: ('"+expr[1:i]+"')"+nxtr[0])
                print("    part 2: "+nxtr[1])
            result1=calc_expression(expr[1:i],val)
            if not (result1[0]):
                errpos=result1[2]+1
                if DEBUGPRINT:
                    print_error(expr,errpos)
                return(result1[0],result1[1],errpos,result1[3])
            perm=result1[1]
            if nxtr[2]!=1:
                perm=powerof(perm,nxtr[2])
            result1=(result1[0],perm,result1[2],result1[3])
            if (nxtr[1]==''):
                return result1
            result2=calc_expression(nxtr[1],val)
            if not result2[0]:
                errpos=result2[2]+i+len(nxtr[0])+1
                if DEBUGPRINT:
                    print_error(expr,errpos)
                return(result2[0],result2[1],errpos,result2[3])
            return((True,compose(result1[1],result2[1]),0,''))
    elif expr[0]==')':
        errpos=1
        if DEBUGPRINT:
            print_error(expr,errpos)
        return(False,None,errpos,'no opening (')
    else:
        perm=val.get(expr[0],None)
        if perm is None:
            errpos=1
            if DEBUGPRINT:
                print_error(expr,errpos)
            return((False,None,errpos,'invalid element'))
        nxtr=extract_integer(expr[1:])
        if DEBUGPRINT:
            print("    part 1: '"+expr[0]+"'"+nxtr[0])
            print("    part 2: "+nxtr[1])
        if nxtr[2]!=1:
            perm=powerof(perm,nxtr[2])
        result=calc_expression(nxtr[1],val)
        if not result[0]:
            errpos=result[2]+len(nxtr[0])+1
            if DEBUGPRINT:
                print_error(expr,errpos)
            return(result[0],None,errpos,result[3])
        else:
            return((True,compose(perm,result[1]),0,''))

def calc_sets(line,symbol,val):
    complexes=line.split('*')
    if len(complexes)==1:
        return(False)
    if len(complexes)!=2:
        print("invalid set operation: more than one '*' operator")
        return True
    left=complexes[0].split()
    right=complexes[1].split()
    if len(left)==0:
        print("invalid set operation: no left complex")
        return True
    if len(right)==0:
        print("invalid set operation: no right complex")
        return True
    product=[]
    for c1 in left:
        perm1=val.get(c1,None)
        if perm1 is None:
            print("invalid set operation: symbol '"+c1+"' is invalid'")
            return (True)
        for c2 in right:
            perm2=val.get(c2,None)
            if perm2 is None:
                print("invalid set operation: symbol '"+c2+"' is invalid'")
                return (True)
            perm=compose(perm1,perm2)
            product.append(symbol[perm])
    e=symbol[identity()]
    product=list(set(product))
    if e in product:
        product.remove(e)  
        product.sort()  
        product.insert(0,e)
    else:
        product.sort()  
    outline=''
    first=True
    for c in product:
        if first:
            outline=c
            first=False
        else:
            outline+=' '+c
    print(outline)
    return(True)
    

        


def interpreter(elementlist,symbol,val):
    # read loop:
    print("starting interpreter ....")
    while True:
        inp=input('$ ')
        parts=inp.split()
        if not parts:
            continue
        if inp==':q':
            break
        if inp==':p':
            #print table
            print_group1(elementlist,symbol)
            continue
        if parts[0]==':r':
            # rename elements
            symb1=parts[1]
            symb2=parts[2]
            perm1=val.get(symb1,None)  
            perm2=val.get(symb2,None)  
            if perm1 is None:
                print("'"+symb1+"' is not a valid symbol'")
                continue
            if perm2 is None:
                print("'"+symb2+"' is not a valid symbol'")
                continue
            ind1=elementlist.index(perm1)
            ind2=elementlist.index(perm2)
            symbol[perm1]=symb2
            symbol[perm2]=symb1
            val[symb1]=perm2
            val[symb2]=perm1
            elementlist[ind1]=perm2
            elementlist[ind2]=perm1
            continue
        if parts[0]==':s':
            # swap elements positions
            symb1=parts[1]
            symb2=parts[2]
            perm1=val.get(symb1,None)  
            perm2=val.get(symb2,None)  
            if perm1 is None:
                print("'"+symb1+"' is not a valid symbol'")
                continue
            if perm2 is None:
                print("'"+symb2+"' is not a valid symbol'")
                continue
            ind1=elementlist.index(perm1)
            ind2=elementlist.index(perm2)
            elementlist[ind1]=perm2
            elementlist[ind2]=perm1
            continue
        is_set_calculation=calc_sets(inp,symbol,val)
        if is_set_calculation:
            continue
        result=calc_expression(inp,val)
        if not result[0]:
            print("ERROR")
            print(inp)
            print(' '*(result[2]-1)+'^')
            print(result[3])
            continue
        print(inp+" = "+symbol[result[1]])

# interpreter(idesc[0],idesc[1],idesc[2])

########################################
#### Group Operations
########################################

def subgroup(generators):
    '''
    input:
        'generators':
            a list of permutations
    output:
        return:
            a set of elements of the group generated by generators
    '''
    assert isinstance(generators,(list,set,tuple))
    generated=set([identity()])
    fringe=set([identity()])
    while fringe:
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

def subgroupX(generators, reduced=None):
    '''
    input:
        'generators':
            a list of permutations
        'reduced':
            an variable containuig an empty list
    output:
        return:
            a set of elements of the group generated by generators
        'reduced':
            a sublist of generators that still generates the group
    '''
    assert isinstance(generators,(list,set,tuple))
    generated=set([identity()])
    if reduced is  None:
        reduced=set()
    else:
        assert(isinstance(reduced,set))
        reduced.clear()
    removed_generators=set()
    fringe=set([identity()])
    shuffled_generators=list(generators)
    shuffle(shuffled_generators)
    for new_gen in shuffled_generators:
        if DEBUGPRINT:
            print("next generator => ",to_cycle(new_gen))
        if new_gen in removed_generators:
            if DEBUGPRINT:
                print("    already removed")
            continue
        if new_gen in generated:
            if DEBUGPRINT:
                print("    generated by others")
            removed_generators.add(new_gen)
            continue
        new_fringe=set()
        for p1 in generated.copy():
            element=compose(p1,new_gen)
            if DEBUGPRINT:
                print("compose  => ",to_cycle(element),"=",to_cycle(p1),"*",to_cycle(new_gen))
            if element not in generated:
                if DEBUGPRINT:
                    print("new element to fringe and generated  => ",to_cycle(element))
                new_fringe.add(element)
                generated.add(element)
        for p1 in reduced:
            for p2 in fringe:
                element=compose(p1,p2)
                if element not in generated:
                    generated.add(element)
                    new_fringe.add(element)
        fringe=new_fringe.copy()
        reduced.add(new_gen)
        if DEBUGPRINT:
            print("fringe:",list(map(to_cycle, fringe)))
            print("reduced:", list(map(to_cycle, reduced))) 
            print("generated:", list(map(to_cycle, generated))) 
    if DEBUGPRINT:
        print("processing remaining fringe")
    if DEBUGPRINT:
        print("fringe:",list(map(to_cycle, fringe)))
        print("reduced:", list(map(to_cycle, reduced))) 
        print("generated:", list(map(to_cycle, generated))) 
    while fringe:
        new_fringe=set()
        for p1 in reduced:
            for p2 in fringe:
                element=compose(p1,p2)
                if element not in generated:
                    if DEBUGPRINT:
                        print("compose  => ",to_cycle(element),"=",to_cycle(p1),"*",to_cycle(new_gen))
                        print("new element to fringe and generated  => ",to_cycle(element))
                    generated.add(element)
                    new_fringe.add(element)
        fringe=new_fringe.copy()
        if DEBUGPRINT:
            print("fringe:",list(map(to_cycle, fringe)))
            print("reduced:", list(map(to_cycle, reduced))) 
            print("generated:", list(map(to_cycle, generated))) 

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
assert powerof(p((3,5,7,2),(6,4,8)),-1)==invert(p((3,5,7,2),(6,4,8)))
assert powerof(p((3,5,7,2),(6,4,8)),0)==identity()
assert powerof(p((3,5,7,2),(6,4,8)),12345)==p((3,5,7,2))
assert orderof(identity())==1


'''
sg=subgroup(examples["R3E8R4"][1])
idesc=describe_group1(sg,examples["R3E8R4"][0])
interpreter(idesc[0],idesc[1],idesc[2])
'''

#sg=subgroupX(examples["R3E8R4"][1])

ll=(p((1,2)),p((3,4)),p((1,2),(3,4)))
#ll=[p((1,2))]
# sg1=subgroup(ll) 
# print("## generators")
# print(ll)
# print("## subgroup")
# print(sg1)
DEBUGPRINT=False
compose_count=0
ll=[p((1,2)),p((1,3)),p((1,4)),p((1,5)),p((1,6)),p((1,7))]
compose_count=0
sg1=subgroup(ll)
subgroup_compose_count=compose_count
bb=set() 
seed(12345)
seed(None)
compose_count=0
sg2=subgroupX(sg1,bb)
print("## reduced")
print(len(sg1))
print("## subgroup")
print(len(sg2))
print(len(bb))
print(subgroup_compose_count)
print (compose_count)
compose_count=0
sg3=subgroupX(list(bb),bb)
print(len(bb))
print (compose_count)
