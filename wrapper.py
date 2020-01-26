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
        ctx = {
            'col': 0,
        }
        lines = self.raw_text.splitlines(keepends=True)
        res = []
        for l in lines:
            cols = l.split(self.separator)
            res.append(cols)
        self.text_table = res
            




if __name__ == "__main__":
    w = Wrapper("The brown fox jumped into the darkest hole of depression. ||| Lorem ipsum mandatorem t ominuos nebula.\n"\
         "All his friends told him to go to a psych consult but he didnt wanted. ||| ryphaza is the most funny hidden code of gta san andreas."
    )
    w._text2matrix()
    print(w.text_table[0][0],'\n',w.text_table[1][0])