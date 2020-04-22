from sys import stderr, stdin
from os import system
import argparse
from random import randint



### STRUCTURES #######
symbols = {}
objs = []
printobjs = []



### TYPE CLASSES #######

class type_Base():
    def __init__(self, name, objType):
        self.name = name
        self.type = objType
        self.attributes = {}
    def __str__(self):
        attrs = ', '.join([f'<{self.attributes[attr]}>' for attr in self.attributes])
        return f'[{self.name}] ({self.type}) {attrs}'

    def build(self):
        print(f'building object {self}')
            
    def hasAttr(self, key):
        return key in self.attributes

    def setAttr(self, key, attr):
        self.attributes[key] = attr

    def printAttr(self):
        print(self.name, '(int)')
        for attr in self.attributes:
            print(f'  <{attr}> ', end='')
            self.attributes[attr].build()

    def getValue(self):
        if not hasattr(self, 'value'):
            print('uh oh! {self.name} does not have a value!')
        else:
            return self.value

class type_Integer(type_Base):
    def __init__(self, name):
        super().__init__(name, 'int')
    def build(self):
        self.value = self.attributes['range'].getValue()
        self.output = str(self.value) + '\n'
        print(f'{self.name} now holds the value {self.value}')

class type_Line(type_Base):
    def __init__(self, name):
        super().__init__(name, 'Line')

    def setAttr(self, key, attr):
        if key == 'val' and key in self.attributes:
            self.attributes['val'].addVal(attr)
        else:
            self.attributes[key] = attr

    def build(self):
        print(str(self.attributes['val']))
        self.value = [obj.value for obj in self.attributes['val'].vals]
        self.output = ' '.join([str(val) for val in self.value]) + '\n'

class type_Matrix(type_Base):
    def __init__(self, name):
        super().__init__(name, 'Matrix')
    def build(self):
        self.rows = self.attributes['rows'].getValue()
        self.cols = self.attributes['cols'].getValue()
        rangeobj = self.attributes['range']
        self.value = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(rangeobj.getValue())
            self.value.append(row)
        self.output = ''.join( [' '.join([str(i) for i in row])+'\n' for row in self.value]    )
        for row in self.value:
            for c in row:
                self.output

class type_Print(type_Base):
    def __init__(self, name):
        super().__init__(name, 'print')
        self.obj = symbols[name]
    def flush(self, f):
        if not hasattr(self, 'obj'):
            print('ummm... this print statement doesn\'t have an object?')
        elif not hasattr(self.obj, 'output'):
            print('[{self.name}] is not ready to print.')
        else:
            f.write(self.obj.output)



### ATTR CLASSES #######

class attr_Size():
    def __init__(self, line):
        try:
            self.value = int(line)
        except ValueError:
            self.value = symbols[line]
    def __str__(self):
        return f'size [{self.value.name}]'
    def build(self):
        print(f'size object: {self.value}')
    def getValue(self):
        return self.value.getValue()

class attr_Range():
    def __init__(self, line):
        minTerm = line.split(',')[0]
        maxTerm = line.split(',')[1]

        self.min = int(minTerm[1:])
        if minTerm[0] == '(':
            self.min+=1

        self.max = int(maxTerm[:-1])
        if maxTerm[-1] == ')':
            self.max-=1
    def __str__(self):
        return f'range [{self.min},{self.max}]'
    def build(self):
        print(str(self))
    def getValue(self):
        return randint(self.min, self.max)

class attr_Values():
    def __init__(self, line):
        self.vals = [symbols[line]]
    def __str__(self):
        return ', '.join([f'[{val.name}]({val.type})' for val in self.vals])
    def build(self):
        print(str(self))
    def addVal(self,attr):
        self.vals.append(attr.vals[0])
        


### INPUT PARSING #######

# list types by name
types = {
    'int': type_Integer,
    'Line': type_Line,
    'Matrix': type_Matrix,
    'print': type_Print,
}

# list attr objects by name
attrs = {
    'range': attr_Range,
    'rows': attr_Size,
    'cols': attr_Size,
    'val': attr_Values,
}

def parse_Attr(line, obj):
    key = line.split()[0]
    val = ''.join(line.split()[1:])

    try:
        # build our attribute object
        attr = attrs[key](val)
    except KeyError:
        print(f'not a valid attribute for type {obj.type}: {key}')
        raise KeyError
    obj.setAttr(key, attr)

def parse_Type(line):
    obj_Type = line.split()[0]
    obj_Name = line.split()[1]

    obj = types[obj_Type](obj_Name)

    if obj_Type == 'print':
        printobjs.append(obj)
    else:
        # add object to symbol table to retreive by name
        symbols[obj_Name] = obj
        # add object to symbol table to retreive in order
        objs.append(obj)
    return obj

obj = None
def parseInput():
    while True:
        line = stdin.readline()
        if not line:
            break
        elif line[0] == '\n':
            continue
        elif line[0] == ' ' or line[0] == '\t':
            parse_Attr(line, obj)
        else:
            obj = parse_Type(line)




### MAIN #######

#PARSING ARGUMENTS
parser = argparse.ArgumentParser(description='Build test cases for programming challenges.')
parser.add_argument('exc', metavar='exec', type=str, help='executable to produce output')
parser.add_argument('-c', metavar='count', type=int, help='range of test numbers', default=10)
parser.add_argument('-o', metavar='test-dir', type=str, help='target tests directory', default='./tests')
parser.add_argument('-s', metavar='start', type=int, help='test number to start on', default=1)

print('PARSING ARGS')

args = parser.parse_args()
print(args)

exc = args.exc
start = args.s
count = args.c
targetdir = args.o

print(f'using executable: {exc}')
print(f'making {count} test cases starting with {start}')
print(f'putting tests in {targetdir}')
print()

print('PARSING INPUT:')
parseInput()
print()

print('SYMBOL TABLE:')
for symbol in symbols:
    print(f'  {symbols[symbol]}')
print()

print('BUILDING TESTS:')
for i in range(start,count+start):
    testname = 't{0:02d}'.format(i)
    print(f'BUILDING {testname}')
    for obj in objs:
        print(f'  building {obj}')
        print(f'    ',end='')
        obj.build()
    print()

    tinfilename = f'{targetdir}/{testname}.in'
    f = open(tinfilename,'w')
    for obj in printobjs:
        print(tinfilename + ' <--- ' + str(obj))
        obj.flush(f)
    f.close()

    toutfilename = f'{targetdir}/{testname}.out'
    system(f'{exc} < {tinfilename} > {toutfilename}')


    print('t{0:02d} ok\n'.format(i))










