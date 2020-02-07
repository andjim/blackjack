from utils import text_sum

class Wrapper():

    """
                            column 1                                            column 2
        The brown fox jumped into the darkest hole of depression. ||| Lorem ipsum mandatorem t ominuos nebula.
        All his friends told him to go to a psych consult but he didnt wanted. ||| ryphaza is the most funny hidden code of gta san andreas.
    """
    separator = '|||'
    special_char = {
        'break': '\n',
        'tab': '\t' 
    }

    def __init__(self, text, col_width=0):
        self.col_width = col_width
        self.raw_text = text
        self.text_table = []
  
    def _text2matrix(self):
        lines = self.raw_text.splitlines(keepends=True)
        res = []
        for l in lines:
            cols = l.split(self.separator)
            res.append(cols)
        self.text_table = res
            
    def _fit_width(self):
        l = 0
        lines = len(self.text_table)
        while l < lines:
            c = 0
            for c in range(0,len(self.text_table[l])):
                if len(self.text_table[l][c]) <= self.col_width:
                    continue
                words = self.text_table[l][c].split(' ')
                index = 0
                for w in words:
                    pass
                for_next_line = self.text_table[l][c][self.col_width:]
                self.text_table[l][c] = self.text_table[l][c][:self.col_width]
                if lines <= l+1:                    
                        self.text_table.append(['']*len(self.text_table[l]))
                        lines += 1
                self.text_table[l+1][c] = "%s %s" % (for_next_line, self.text_table[l+1][c])
            l += 1
                
                
                
if __name__ == "__main__":
    w = Wrapper("The brown fox jumped into the darkest hole of depression. ||| Lorem ipsum mandatorem t ominuos nebula.\n"\
         "All his friends told him to go to a psych consult but he didnt wanted. ||| ryphaza is the most funny hidden code of gta san andreas.",
         30
    )
    w._text2matrix()
    w._fit_width()
    print(w.text_table)