# module beacon.common
"""
...prevents variant class for software
"""


class Variant:
    """
    Creates Variant Object.

    :param chr: chr of input variant
    :param pos: pos of input variant
    :param ref: ref of input variant
    :param alt: alt of input variant
    """

    def __init__(self, chr, pos, ref, alt):
        self.chr = chr
        self.pos = pos
        self.ref = ref
        self.alt = alt


class AnnVar:
    """
    Creates AnnVar Object.

    :param chr: chr of input variant
    :param pos: pos of input variant
    :param ref: ref of input variant
    :param alt: alt of input variant
    :param occ: occurence of variant in database
    """

    def __init__(self, chr, pos, ref, alt, occ, error=None):
        self.chr = chr
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.occ = occ
        self.error = error


class Info(AnnVar):
    """
    Creates Info Object and is subclass of AnnVar.

    :param varCount: #variants in database for query
    :param population: list of tuple in which population and how often query variant exist
    :param statistic: statistic of output data
    :param frequency: frequency of allels in variant
    :param phenotype: phenotype information
    """

    def __init__(
        self,
        chr,
        pos,
        ref,
        alt,
        occ,
        error,
        varCount,
        population,
        statistic,
        frequency,
        phenotype,
    ):
        self.varCount = varCount
        self.population = population
        self.statistic = statistic
        self.frequency = frequency
        self.phenotype = phenotype
        AnnVar.__init__(self, chr, pos, ref, alt, occ, error)


def parse_var(inp):
    """
    Parses an input string to a variant object.

    :param inp: variant string
    :return: variant object
    """
    new_var = Variant(inp["chr"], inp["pos"], inp["ref"], inp["alt"])
    return new_var
