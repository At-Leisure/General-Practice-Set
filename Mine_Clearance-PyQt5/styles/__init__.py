

def read_qss(path :str, encoding:str):
    with open(path,'r',encoding=encoding) as f:
        text = ''.join(f.readlines())
    return text