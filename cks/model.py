import os
import pandas as pd
import numpy as np
from isochrones import StarModel

from .table import SpecTable
from .cfg import DATADIR

from keputils import koiname

spec_df = SpecTable().df
dfAV = pd.read_table(os.path.join(DATADIR, 'koi_maxAV.txt'), delim_whitespace=True,
                     index_col=0, names=['koi','AV'])

def get_maxAV(koinum):
    return dfAV.ix[koiname(koinum)].AV

class CKSStarModel(StarModel):
    def __init__(self, ic, koinum, skip_bands=None, **kwargs):
        self.koinum = koinum
        s = spec_df.ix[koinum]
        props = {b:(s[b], s['{}_unc'.format(b)]) for b in ['J','H','K']}
        props.update(dict(Teff=(s.Teff, 116), logg=(s.logg, 0.07), feh=(s.feh, 0.04)))
        props.update(kwargs)
        
        if skip_bands is not None:
            [props.pop(b, None) for b in skip_bands]

        maxAV = get_maxAV(koinum)
        super(CKSStarModel, self).__init__(ic, name=self.koinum, maxAV=maxAV, **props)

