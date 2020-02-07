def text_sum(list_of_str,spacer=''):
    res = ''
    for txt in list_of_str:
        if isinstance(str,txt):
            raise TypeError('All elements must be instance of str')
        res += txt + spacer
