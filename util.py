def trace(collection):
    cursor = collection.find()
    for line in  cursor: print line

def fetch(collection):
    cursor = collection.find()
    return [line for line in cursor]

def has_key(dic,ki):
    try: dic[ki] = dic[ki]
    except KeyError: return False
    return True

def clean(dictionary, attributes):
 
    for a in attributes: 
        banana = a.split('.')
        if len(banana) > 1 : 
        	print '--'
        	PARENT = banana.pop(0)
        	CHILD = '.'.join(banana)
        	dictionary[PARENT] = clean(dictionary[PARENT], [CHILD] )            
        else:
        	del dictionary[a]
    return dictionary

"""

    Testing Clean:

    def test_clean():
         a = {'b':8,'c':{'d':9,'e':{'f':{'g':8}}}}
         b = clean(a,['c.e.f.g'])
         print b   
""" 

class DotNotation:
    def __init__(self, **entries): 
        self.__dict__.update(entries)
        for key in entries:
            if type(entries[key]) is dict:
                setattr(self,key,DotNotation(**getattr(self,key)))



def objectify(func_to_decorate):
    def wrapper(*args, **kwargs):
        result = func_to_decorate(*args, **kwargs)
        return DotNotation(**result)
    return wrapper
