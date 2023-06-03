def return_next(lst):
    if len(lst) >1:
        result = lst[-2]
        if 'static' not in result and 'favico' not in result:
            return result
        else: return '/'
    else:
        return '/'
    

def coll_to_int(coll):
    result = ''
    for i in coll:
        if i.isdigit():
            result = result+i
        else:
            continue
    if result != None and result != '':
        return int(result)
    else:
        return 1