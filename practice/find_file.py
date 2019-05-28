import os

## Just only find file once,if find file,return right now
def find_file(name,path='.'):
    if not name or isinstance(name,str):return
    dirs = [os.path.join(path,x) for x in os.listdir(path)]
    for x in dirs:
        if os.path.isfile(x) and name in x:
            return x
        elif os.path.isdir(x):
            ret = find_file(name,path=x)
            if ret is not None: return ret
    return
if __name__ == '__main__':
    print(find_file('User_Conf.dic'))
