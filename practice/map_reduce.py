from functools import reduce


def normalize(name):
    first=name[0].upper()
    latter = name[1:].lower()
    return first+latter

L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)

def prod(l):
    return reduce(lambda x,y:x*y,l)

print(prod([3,5,7,9]))

def str2float(s):
    def char2num(s):
        digits = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
        return digits[s]

    def charset(s):
        digits,fraction = s.split('.')
        digits=reduce(lambda x,y:x*10+y,map(char2num,digits))
        fraction=reduce(lambda x,y:x/10+y,map(char2num,fraction[::-1]))
        return digits+fraction/10

    return charset(s)

print('str2float(\'123.456\') =', str2float('123.456'))
if abs(str2float('123.456') - 123.456) < 0.00001:
    print('测试成功!')
else:
    print('测试失败!')
