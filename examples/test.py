import pprint

data = [{6,'A'},(5,'R'),{2:'O'},{1:'C'},[3,'N'], {'hah,trick':{4:'G'}},7,'T',8,'U',9,'L',10,'A',{15:'S'},{14:'N'},{11:'T'},{12:'I'}]

res, i = [], 0
while i < len(data):
    if isinstance(data[i],set) or isinstance(data[i], tuple):
        res.append(sorted(data[i], key=lambda x: not isinstance(x, int)))
    elif isinstance(data[i],dict):
        k,v = list(data[i].items())[0]
        if isinstance(v,dict):
            k,v = list(v.items())[0]
        res.append(
            [
                k if isinstance(k, int) else v,
                v if isinstance(k, int) else k
            ]
        )
    elif isinstance(data[i],list):
        res.append(
            [
                data[i][0] if isinstance(data[i][0], int) else data[i][1],
                data[i][1] if isinstance(data[i][0], int) else data[i][0]
            ]
        )
    elif isinstance(data[i], int):
        res.append([data[i],data[i+1]])
        i+=1
    i+=1
print(''.join( _[1] for _ in sorted(res,key=lambda x: x[0])))