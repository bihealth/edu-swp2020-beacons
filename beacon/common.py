# module beacon.common
"""
...prevents variant class for software
"""


class Variant:
    def __init__(self, chr, pos, ref, alt):
        """
        Creates Variant Object.

        :param chr: chr of input variant
        :param pos: pos of input variant
        :param ref: ref of input variant
        :param alt: alt of input variant
        """
        self.chr = chr
        self.pos = pos
        self.ref = ref
        self.alt = alt


def parse_var(inp):
    """
    Parses an input string to a variant object.

    :param inp: variant string
    :return: variant object
    """
    strin_spli = inp.split("-")
    new_var = Variant(strin_spli[0], strin_spli[1], strin_spli[2], strin_spli[3])
    return new_var
