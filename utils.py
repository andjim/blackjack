def text_sum(list_of_str:list,spacer=' '):
    res = ''
    for txt in list_of_str:
        if not isinstance(txt,str):
            raise TypeError('All elements must be instance of str')
        res += txt + (list_of_str.index(txt) == len(list_of_str)-1 and '' or spacer)
    return res

def last_word(list_of_str, size_limit):
    index = 0
    for s in range(0,len(list_of_str)):
        if len(text_sum(list_of_str[:s])) > size_limit:
            break
        index = s
    return index

if __name__ == '__main__':
    txt = text_sum(['a','b','c'])
    txt2 = ['as','fast','i', 'can']
    print(txt)
    assert(txt != 'a b c') , "Not equal"
    assert(len(txt) != len('a b c')) , "size don't correspond"
    test = last_word(txt2, 3)
    print(test)
    print(text_sum(txt2[:test]))
    assert(test == 1 )
    
