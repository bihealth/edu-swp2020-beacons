class Variant:
    """Input variants"""
    def __init__(self, chr, pos, res, alt):
        self.chr = chr
        self.pos = pos
        self.res = res
        self.alt = alt

class AnnotatedVariant():
    """
    Output true or false"""
    def __init__(self, var, occ):
        self.var = var
        self.occ = occ
        
def parse_var(inp):
    """
    Input: variant string 
    Output: variant objec(t parses an input string to a variant object or variant 
    objectto string"""
    if isinstance(inp, str):
        strin_spli = inp.split(",")
        new_var = Variant(strin_spli[0],strin_spli[1], strin_spli[2], strin_spli[3])
    else:
        var_list = inp.__dict__.values()
        new_var = ','.join(var_list)
    return new_var
