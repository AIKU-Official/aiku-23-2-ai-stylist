import os
import json
import random
from collections import OrderedDict, defaultdict

import pandas as pd

import torch
import torch.nn as nn
from torch import Tensor, LongTensor
from torch.utils.data import Dataset, DataLoader, random_split

from typing import Optional, Dict, List, Set, Tuple

from copy import deepcopy

BASE_PATH = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

TRAIN_PAIRS_PATH = BASE_PATH + '/data/polyvore_cleaned/train.json'
VALID_PAIRS_PATH = BASE_PATH + '/data/polyvore_cleaned/valid.json'
TEST_PAIRS_PATH = BASE_PATH + '/data/polyvore_cleaned/test.json'

TOP_EMBEDS_PATH = BASE_PATH + '/data/polyvore_cleaned/top_embeds.json'
BOTTOM_EMBEDS_PATH = BASE_PATH + '/data/polyvore_cleaned/bottom_embeds.json'

class StyleAwareNetDataset(Dataset):
    def __init__(
        self,
        path,
        ):
        super(StyleAwareNetDataset, self).__init__()
        self.top_embeds = self._preprocess_embeds(TOP_EMBEDS_PATH)
        self.bottom_embeds = self._preprocess_embeds(BOTTOM_EMBEDS_PATH)
        self.anc_ids, self.pos_df = self._preprocess_pairs(path)
        
    def __len__(self):
        return len(self.anc_ids)
    

    def __getitem__(self, idx):
        anc_id = self.anc_ids[idx]
        pos_id = random.choice(self.pos_df.loc[anc_id]['bottom_id'])
        neg_ids = self._get_neg_sample(anc_id, n=10)

        anc = torch.Tensor(self.top_embeds.loc[anc_id]['embed'])
        pos = torch.Tensor(self.bottom_embeds.loc[pos_id]['embed'])
        negs = torch.stack([torch.Tensor(self.bottom_embeds.loc[neg_id]['embed']) for neg_id in neg_ids])
        return anc, pos, negs
    

    def _preprocess_pairs(self, path):
        df = pd.read_json(path)\
            .drop_duplicates(subset=['top_id', 'bottom_id'])\
            .groupby(['top_id', 'y'])\
            .agg({'bottom_id' : list})
        pos_df = df.xs(1, level='y')
        anc_ids = pos_df.index
        return anc_ids, pos_df
    
    def _get_neg_sample(self, anc_id, n=64):
        crit = set(self.pos_df.loc[anc_id]['bottom_id'])
        neg_ids = set()
        while len(neg_ids) < n:
            tmp = random.choice(self.bottom_embeds.index)
            if tmp not in crit:
                neg_ids.add(tmp)
        return list(neg_ids)

    def _preprocess_embeds(self, path):
        return pd.read_json(path)
    

def get_dataset():
    train_dataset = StyleAwareNetDataset(TRAIN_PAIRS_PATH)
    valid_dataset = StyleAwareNetDataset(VALID_PAIRS_PATH)
    test_dataset = StyleAwareNetDataset(TEST_PAIRS_PATH)
    return train_dataset, valid_dataset, test_dataset

if __name__ == '__main__':
    t, v, test = get_dataset()
    print(len(t[0]))