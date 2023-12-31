import sys
from torchmetrics.functional import pairwise_cosine_similarity
import torch
from typing import List

class StyleClassifier():
    def __init__(self, 
                 embed_generator,
                 styles: List[str]):
        
        self.styles = styles
        self.embed_generator = embed_generator
        self.temperature = 0.5
        self.prompt_embeddings = torch.stack([torch.Tensor(self.embed_generator.text2embed("a photo of {} style clothes".format(s))) for s in styles])

    
    @torch.no_grad()
    def forward(self, anc, pos, device):
        pos_similarity = pairwise_cosine_similarity(pos.to(device), self.prompt_embeddings.squeeze(1).to(device))
        anc_similarity = pairwise_cosine_similarity(anc.to(device), self.prompt_embeddings.squeeze(1).to(device))

        logits = (pos_similarity + anc_similarity)/2
        
        # logits = torch.min(torch.stack([anc_similarity, pos_similarity]), 0).values
        # logits = torch.nn.functional.softmax(logits / self.temperature, dim=1).detach()
        return logits

    def idx2stl(self, idx):
        return self.styles[idx]
        
    def stl2idx(self, stl):
        return self.styles.index(stl)