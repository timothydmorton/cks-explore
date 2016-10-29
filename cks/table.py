import pandas as pd
import os, re
from cryptography.fernet import Fernet

from keputils import koiutils as ku, koiname

from .cfg import DATADIR

KEY = open(os.path.join(DATADIR,'fernet.key')).read()

def parse_cell(s):
    return float(s.replace('$',''))

def encrypt_file(filename, cryptfile, key=KEY):
    raw = open(filename).read()
    cipher_suite = Fernet(key)
    fout = open(cryptfile, 'w')
    fout.write(cipher_suite.encrypt(raw))
    fout.close()
    
class CryptTable(object):
    def __init__(self, filename, key=KEY):
        self.filename = filename
        self.key = key
        self._df = None
        
    @property
    def _file_string(self):
        """Returns single string of file contents
        """
        if self.key is None:
            return open(self.filename).read()
        else:
            cipher_suite = Fernet(self.key)
            raw = open(self.filename).read()
            return cipher_suite.decrypt(raw)
        
    @property
    def df(self):
        if self._df is None:
            self._df = self._parse_table(self._file_string)
        return self._df
        
    def _parse_table(self, fstring):
        raise NotImplementedError
    
class SpecTable(CryptTable):
    def __init__(self, filename=os.path.join(DATADIR,'spec.tex.crypt'), key=KEY):
        super(SpecTable, self).__init__(filename, key)

    def _parse_table(self, fstring):
        kois = []
        teffs = []
        loggs = []
        fehs = []
        vsinis = []
        Kmags = []
        unc_Kmags = []
        Jmags = []
        unc_Jmags = []
        Hmags = []
        unc_Hmags = []
        for line in fstring.splitlines():
            line = line.split('&')
            m = re.search('(\d+)-(\w+)?', line[0])
            if not m:
                print(line)
            kois.append(int(m.group(1)))
            teffs.append(parse_cell(line[1]))
            loggs.append(parse_cell(line[2]))
            fehs.append(parse_cell(line[3]))
            vsinis.append(parse_cell(line[4]))
            s = ku.DATA.ix[koiname(m.group(1))]
            Jmags.append(s.koi_jmag)
            unc_Jmags.append(s.koi_jmag_err)
            Hmags.append(s.koi_hmag)
            unc_Hmags.append(s.koi_hmag_err)
            Kmags.append(s.koi_kmag)
            unc_Kmags.append(s.koi_kmag_err)

        df = pd.DataFrame({'koi':kois, 'Teff':teffs, 'logg':loggs, 
                        'feh':fehs, 'vsini':vsinis, 
                        'J':Jmags, 'J_unc':unc_Jmags,
                        'H':Hmags, 'H_unc':unc_Hmags,
                        'K':Kmags, 'K_unc':unc_Kmags})
        df.index = df.koi
        return df
