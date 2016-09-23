from recommenders.collabrativefiltering.bpr import BPR
from recommenders.collabrativefiltering.item_cf import ItemCF
from recommenders.collabrativefiltering.biased_fm import BiasedFM
from recommenders.collabrativefiltering.average import AVERAGE
from recommenders.collabrativefiltering.top_n import TopN
from recommenders.collabrativefiltering.user_cf import UserCF
from recommenders.collabrativefiltering.bpmtmf import BPMTMF
from recommenders.collabrativefiltering.bpmf import BPMF
from recommenders.collabrativefiltering.pmf import PMF
from recommenders.contentbased.ecc import ECC
from recommenders.contentbased.hft import HFT

class AlgFactory():

    @staticmethod
    def create(name, path, parameters):
        if name == 'TopN':
            return TopN(path, parameters)
        elif name == 'BiasedFM':
            return BiasedFM(path, parameters)
        elif name == 'AVERAGE':
            return AVERAGE(path, parameters)
        elif name == 'UserCF':
            return UserCF(path, parameters)
        elif name == 'ItemCF':
            return ItemCF(path, parameters)
        elif name == 'BPR':
            return BPR(path, parameters)
        elif name == 'BPMTMF':
            return BPMTMF(path, parameters)
        elif name == 'BPMF':
            return BPMF(path, parameters)
        elif name == 'PMF':
            return PMF(path, parameters)
        elif name == 'ECC':
            return ECC(path, parameters)
        elif name == 'HFT':
            return HFT(path, parameters)
