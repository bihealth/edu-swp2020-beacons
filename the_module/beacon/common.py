class Variant:
    """Input variants"""
    def __init__(self, chr, pos, res, alt):
        self.chr = chr
        self.pos = pos
        self.res = res
        self.alt = alt

class AnnotatedVariant():
    """Output true or false"""
    def __init__(self, var, occ):
        self.var = var
        self.occ = occ
        
class VariantStringParser:
    """ variant object parses an input string to a variant object or variant 
        objectto string """
    def __init__(self, var_str):
        pass
    def parse_var(self, var_str): 
        """Input: variant string 
        Output: variant object parses an input string to a variant object or variant 
        objectto string"""
        pass
