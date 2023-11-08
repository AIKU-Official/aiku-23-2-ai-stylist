import argparse
import torch
import numpy as np

from tqdm import tqdm
from copy import deepcopy
from torch.optim import Adam, lr_scheduler
from model.loss import PairwiseRankingLoss


class Trainer:
    def __init__(self, model, train_dataloader, valid_dataloader, optimizer, scheduler, device, TrainingArgs):
        self.model = model
        self.optimizer = optimizer
        self.train_dataloader = train_dataloader
        self.valid_dataloader = valid_dataloader
        self.scheduler = scheduler
        self.device = device
        self.TrainingArgs = TrainingArgs

        self.best_model = None
        self.best_optimizer = None

    def train(self):
        lowest_loss = np.inf

        for epoch in range(self.TrainingArgs.n_epochs):
            train_loss = self._train(self.train_dataloader, epoch)
            valid_loss = self._validate(self.valid_dataloader, epoch)

            if valid_loss <= lowest_loss:
                lowest_loss = valid_loss
                self.best_model = deepcopy(self.model.state_dict())
                self.best_optimizer = deepcopy(self.optimizer.state_dict())

    def _train(self, dataloader, epoch):
        self.model.train()

        epoch_iterator = tqdm(dataloader)

        losses = 0.0
        for iter, batch in enumerate(epoch_iterator, start=1):
            self.optimizer.zero_grad()

            source_embed, pos_embed, neg_embeds = batch
            pos = self.model(source_embed.to(self.device), pos_embed.to(self.device))
            neg = torch.mean(torch.stack([self.model(source_embed.to(self.device), neg_embed.to(self.device)) for neg_embed in neg_embeds]), dim=0)

            loss = PairwiseRankingLoss(pos, neg)
            loss.backward()
            self.optimizer.step()
            self.scheduler.step()

            losses += loss.item()
            epoch_iterator.set_description(
                'Train | Epoch: {:03}/{:03} | loss: {:.5f}'.format(epoch + 1, self.TrainingArgs.n_epochs, losses / iter)
                )
        
        return losses / iter


    @torch.no_grad()
    def _validate(self, dataloader, epoch):
        self.model.eval()

        epoch_iterator = tqdm(dataloader)

        losses = 0.0

        for iter, batch in enumerate(epoch_iterator, start=1):
            source_embed, pos_embed, neg_embeds = batch
            pos = self.model(source_embed.to(self.device), pos_embed.to(self.device))
            neg = torch.mean(torch.stack([self.model(source_embed.to(self.device), neg_embed.to(self.device)) for neg_embed in neg_embeds]), dim=0)
            loss = PairwiseRankingLoss(pos, neg)
                
            losses += loss.item()

            epoch_iterator.set_description(
                'Validation | Epoch: {:03}/{:03} | loss: {:.5f}'.format(epoch + 1, self.TrainingArgs.n_epochs, losses / iter)
                )
                
        return losses / iter

