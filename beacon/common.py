class Variant:
    """Input variants"""

    def __init__(self, chr, pos, ref, alt):
        self.chr = chr
        self.pos = pos
        self.ref = ref
        self.alt = alt


def parse_var(inp):
    """
    Input: variant string 
    Output: variant objec(t parses an input string to a variant object or variant 
    objectto string"""
    strin_spli = inp.split("-")
    new_var = Variant(strin_spli[0], strin_spli[1], strin_spli[2], strin_spli[3])
    return new_var
