from utils import text_sum, last_word

class Wrapper():

    """
                            column 1                                            column 2
        The brown fox jumped into the darkest hole of depression. ||| Lorem ipsum mandatorem t ominuos nebula.
        All his friends told him to go to a psych consult but he didnt wanted. ||| ryphaza is the most funny hidden code of gta san andreas.
    """
    separator = ' ||| '
    special_char = {
        'break': '\n',
        'tab': '\t'
    }

    def __init__(self, text, col_width, separation_size):
        self.col_width = col_width
        self.raw_text = text
        self.text_table = []
        self.sep_size = separation_size
  
    def _text2matrix(self):
        lines = self.raw_text.splitlines()
        res = []
        for l in lines:
            cols = [words.split(' ') for words in l.split(self.separator)]
            res.append(cols)
        self.text_table = res
            
    def _fit_width(self):
        self._text2matrix()
        lines_lenght = len(self.text_table)
        l = 0
        while l < lines_lenght:
            for c in range(0,len(self.text_table[l])):
                txt = text_sum(self.text_table[l][c])
                if not len(txt) > self.col_width:
                    self.text_table[l][c] = txt
                    continue
                index = last_word(self.text_table[l][c], self.col_width)
                next_line = self.text_table[l][c][index:]
                self.text_table[l][c] = text_sum(self.text_table[l][c][:index])
                if l+1 >= lines_lenght:
                    self.text_table.append([[]] * len(self.text_table[l]))
                    lines_lenght += 1
                self.text_table[l+1][c] = next_line + self.text_table[l+1][c] 
            l += 1 

    def wrap(self):
        self._fit_width()
        res= ""
        for l in self.text_table:
            line = ""
            for c in l:
                offset = self.col_width - len(c)
                _fit = ""
                if offset != 0:
                    _fit += ' ' * offset
                if not l.index(c) >= len(l) -1:
                    _fit += '\t'.expandtabs(self.sep_size)
                line += c + _fit 
            res += line + '\n'
        return res

    
if __name__ == "__main__":
    w = Wrapper("The brown fox jumped into the darkest hole of depression. ||| Lorem ipsum mandatorem t ominuos nebula.\n"\
         "All his friends told him to go to a psych consult but he didnt wanted. ||| ryphaza is the most funny hidden code of gta san andreas.",
         30, 90
    ) 
    print(w.wrap())
    print('\n')
    #print(w.text_table)
    