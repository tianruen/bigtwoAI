from typing import List, Tuple, Dict

import torch
import torch.nn as nn
import torch.optim as optim

import preprocess

# input_dim, output_dim, hidden_dim = 104, 18880, 256
# input_dim: 143 - hand card, opponent hand caard, history card OR 104 - hand card, history card
# output_dim: total actions + None + value
class deepPG(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dim) -> None:
        super().__init__()
        self.net = nn.Sequential(nn.Linear(input_dim, hidden_dim),
                                 nn.ReLU(),
                                 nn.Linear(hidden_dim, hidden_dim),
                                 nn.ReLU(),
                                 nn.Linear(hidden_dim, output_dim))
        self.optimizer = optim.Adam(self.net.parameters())
        
    def transform_action_distribution(self, action_dist:Dict[int, float]):
        """Given the action distribution in dictionary form, transform it to get:
        1. available moves in binary form
        2. the distribution of the moves

        Args:
            action_dist (Dict[int, float]): key is the action, value is the proportion of visiting the action
        """
        
        key_tensor = [torch.tensor(list(d.keys())) for d in action_dist]
        max_len = max(t.shape[0] for t in key_tensor)
        key_tensor = [nn.functional.pad(t, (0, max_len-t.shape[0]), mode="constant", value=t[0]) for t in key_tensor]
        indices = torch.stack(key_tensor)
        ones = torch.ones(indices.shape)
        avail_act_binary = torch.zeros(indices.shape[0], len(preprocess.all_actions))
        avail_act_binary.scatter_(1, indices, ones)
        
        val_tensor = [torch.tensor(list(d.values())) for d in action_dist]
        val_tensor = [nn.functional.pad(t, (0, max_len-t.shape[0]), mode="constant", value=t[0]) for t in val_tensor]
        values = torch.stack(val_tensor)
        pi = torch.zeros(indices.shape[0], len(preprocess.all_actions))
        pi.scatter_(1, indices, values)
        
        return avail_act_binary, pi
        
    def forward(self, x, avail_actions):
        x = self.net(x)
        raw_prob = x[:, :-1] + (avail_actions - 1) * 1e9
        value = x[:, -1]
        
        return raw_prob, torch.tanh(value)
        # return nn.Softmax(dim=1)(raw_prob), torch.tanh(value)
    
    def train(self, state:List[int], action_dist:Dict[int, float], rewards:int, regularise_lambda:float=0):
        state = torch.tensor(state, dtype=torch.float)
        rewards = torch.tensor(rewards, dtype=torch.float)
        
        if len(state.shape) == 1:
            state = state.unsqueeze(0)
            rewards = rewards.unsqueeze(0)
        
        # get available actions and the distribution of the actions
        avail_act_binary, pi = self.transform_action_distribution(action_dist)
        # forward pass
        pred_prob, v = self.forward(state, avail_act_binary)    
        # calculate loss
        mse_loss = nn.MSELoss()(v, rewards)
        cross_entropy_loss = nn.CrossEntropyLoss()(pred_prob, pi)
        l2_norm = sum([(param**2).sum() for param in self.net.parameters()])
        
        loss = mse_loss + cross_entropy_loss + regularise_lambda*l2_norm
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss