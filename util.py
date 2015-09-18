def trace(collection):
    cursor = collection.find()
    for line in  cursor: print line

def fetch(collection):
    cursor = collection.find()
    return [line for line in cursor]

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

def test_clean():
	a = {'b':8,'c':{'d':9,'e':{'f':{'g':8}}}}
	b = clean(a,['c.e.f.g'])
	print b    

if __name__== '__main__':
	test_clean()
