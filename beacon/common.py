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


class AnnVar:
    def __init__(self, chr, pos, ref, alt, occ):
        """
        Creates AnnVar Object.

        :param chr: chr of input variant
        :param pos: pos of input variant
        :param ref: ref of input variant
        :param alt: alt of input variant
        :param occ: occurence of variant in database
        """
        self.chr = chr
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.occ = occ


class Info(AnnVar):
    def __init__(self, varCount, population, statistic, frequency, phenotype):
        """
        Creates Info Object and is subclass of AnnVar.

        :param varCount: #variants in database for query
        :param population: list of tuple in which population and how often query variant exist
        :param statistic: statistic of output data
        :param frequency: frequency of allels in variant
        :param phenotype: phenotype information
        """
        self.varCount = varCount
        self.population = population
        self.statistic = statistic
        self.frequency = frequency
        self.phenotype = phenotype


def parse_var(inp):
    """
    Parses an input string to a variant object.

    :param inp: variant string
    :return: variant object
    """
    strin_spli = inp.split("-")
    new_var = Variant(strin_spli[0], strin_spli[1], strin_spli[2], strin_spli[3])
    return new_var
