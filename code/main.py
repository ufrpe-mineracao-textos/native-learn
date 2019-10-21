import os
import re
import math
import string
from itertools import combinations

import nltk
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from util.preprocess import prepData, AutoStemm
from util.util import save_stemms

# --- Tirando referências -----

path = r'../datasets/'
data_list = os.listdir(path)
prep = prepData(path)

# prep.label_data('text-label.csv')
# sufixes = pd.read_csv('sufix.csv')['sufix']

dataset = prep.get_datasets()
for name, data in zip(dataset.keys(), dataset.values()):

    print('Processando: ', name)
    scripture = data['Scripture']

    try:

        stem = AutoStemm(scripture, name)

        stem.freq_counter()

        sufixies = stem.get_sufix_freq().keys()
        s_freqs = stem.get_letter_freq().values()

        stem.freq_counter()
        letter_freq = stem.get_letter_freq()
        stemmed_words = stem.stem_words()
        save_stemms(stemmed_words, name)

        all_coo = []

        for suf, s_freq in zip(sufixies, s_freqs):

            ls_freq = 1
            for l in suf:
                l_freq = letter_freq.get(l)
                ls_freq *= l_freq
            co_o = s_freq * math.log((s_freq / ls_freq), 10)
            all_coo.append((suf, co_o))

        all_coo.sort(key=lambda tup: tup[1])

        signature = {}
        sel_stem = []
        temp = 0
        print('Finding stems: ', end='')

        stemmed = pd.read_csv('stemmed/' + name + '.csv')

        for tupl in all_coo[:100]:

            print('#', end='')
            stems = stemmed[stemmed['sufix'] == tupl[0]]['stems']

            for ste in list(stems):
                related_sufix = stemmed[stemmed['stems'] == ste]['sufix'].drop_duplicates()
                words = stemmed[stemmed['stems'] == ste]['words'].drop_duplicates()

                if len(list(related_sufix)) >= 2 and len(list(stems)) <= 5:
                    signature[ste] = words
                    try:
                        sel_stem.append(ste)
                    except TypeError:
                        print(stems)
                        print(stem)
                        breakpoint()
        print()

        df = pd.DataFrame(signature)

        df.to_csv('stems/' + name + '.csv', index=False)

    except TypeError:
        file = open('logs.txt', 'a')
        exp = TypeError
        file.write(name)
        file.write(str(exp.__traceback__))
