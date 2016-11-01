import re, os
import numpy as np
import pandas as pd
import pdb
import logging
from multiprocessing import Pool

from .cfg import CKSDIR
from isochrones.summary import make_summary_df as _make_summary_df

def make_summary_df(directory, **kwargs):
    """Makes summary quantile df for all starmodels (*.h5) in directory 
    """

    modeldir = os.path.join(CKSDIR, 'starmodels', directory, 'models')
    return _make_summary_df(modeldir, **kwargs)