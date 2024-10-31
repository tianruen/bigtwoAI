import copy
import math
import random
from typing import List, Optional, Tuple
from collections import deque

import pandas as pd

import torch
import torch.nn as nn
import torch.optim as optim

import big_two_AI as bt
import preprocess
import model

class ModifyGame(bt.BigTwoGame):   
    def __init__(self, game:bt.BigTwoGame, player_idx:int) -> None:
        game = copy.deepcopy(game)
        self.original_game = game
        self.players = [p for p in game.players]
        self.bot_play = 0   # to record the number of times bot plays. If more than 3, then its agent turn        
        self.player_idx = player_idx
        self.game_hist = game.game_hist
        self.cur_player = game.cur_player
        self.combine_bot()
        
    def combine_bot(self):
        self.bot = bt.Player("CombBot", "Bot")
        for idx, player in enumerate(self.players):
            if idx != self.player_idx:
                self.bot.hand.extend(player.hand)
        self.bot.hand.sort()
        self.players = [self.players[self.player_idx], self.bot]
                
    def next_player(self, cur_player):
        if self.bot_play == 3:
            self.bot_play = 0
            return self.players[0] # since the agent is always the first player
        else:
            self.bot_play += 1
            return self.bot

class BigTwoState():
    def __init__(self, game:ModifyGame) -> None:
        self.game = game
        self.player = self.game.cur_player
        self.table_cards = next((p_c[1] for p_c in self.game.game_hist[-3:][::-1] if p_c[1] is not None), None)   # p_c: (player, played_cards)
        
    def get_available_actions(self):
        return self.player.get_available_actions(self.table_cards)
        
    def move(self, action:List[bt.Card]):
        self.game.play_turn(action)
        return BigTwoState(self.game)
    
    def is_terminal(self):
        return self.game.game_over()
        
    def get_reward(self):
        winner_idx = [len(p.hand) == 0 for p in self.game.players].index(True)
        return 1 if winner_idx == 0 else -1 # index is always 0 for the playing agent
        
class MCTSNode():
    def __init__(self, state:BigTwoState, parent:Optional["MCTSNode"]=None, prior_prob:float=0) -> None:
        self.state = state      # cards that are played
        self.parent = parent
        self.children = {}
        self.num_visits = 0
        self.q_value = 0        # define as W(s,a) in the paper
        self.prior_prob = prior_prob
    
    def __repr__(self) -> str:
        return f"{self.state.game.game_hist[-1][1]}" if len(self.state.game.game_hist) > 0 else "None"
        
    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_available_actions())
    
    def upper_confidence_tree(self, c_param=1.4) -> Optional["MCTSNode"]:
        choices_weights = []
        for child in self.children.values():
            Q = child.q_value / child.num_visits if child.num_visits > 0 else 0
            U = c_param * child.prior_prob * math.sqrt(self.num_visits) / (1 + child.num_visits)
            choices_weights.append(Q + U)
        # choices_weights = [
        # child.q_value / child.num_visits + c_param * child.prior_prob * math.sqrt(self.num_visits) / (1 + child.num_visits) if child.num_visits > 0 else child.prior_prob
        # for child in self.children
        # ]
        argmax = choices_weights.index(max(choices_weights))
        return list(self.children.values())[argmax]
        # return self.children[argmax]
    
    def visit_distribution(self, tau=1.5):
        dist = {}
        total_visit = sum([child.num_visits ** (1/tau) for child in self.children.values()])
        for child in self.children.values():
            action = child.state.game.game_hist[-1][1]
            action = tuple(action) if action else action
            dist[preprocess.encode(action)] = child.num_visits ** (1/tau) / total_visit
        return dist
    
    def expand(self, policy_value_network):        
        p = preprocess.Preprocess(self.state.game.original_game)
        # features = torch.tensor(p.get_hand_cards() + p.get_history(), dtype=torch.float)
        features = torch.tensor(p.create_features(), dtype=torch.float)
        avail_actions = self.state.get_available_actions()
        avail_act_binary = torch.zeros(len(preprocess.all_actions))
        one_index = [preprocess.encode(tuple(act)) if act else preprocess.encode(act) for act in avail_actions]
        avail_act_binary[one_index] = 1
        # none_binary = torch.tensor([1]) if self.state.table_cards is not None else torch.tensor([0])
        # avail_act_binary = torch.cat([avail_act_binary, none_binary])
        with torch.no_grad():
            features = features.unsqueeze(0)
            avail_act_binary = avail_act_binary.unsqueeze(0)
            prior_probabilities, value = policy_value_network(features, avail_act_binary)
            prior_probabilities = nn.Softmax(dim=1)(prior_probabilities)
        
        for action in avail_actions:
            state_ = copy.deepcopy(self.state)  # to avoid changing the state of the current node
            next_state = state_.move(action)
            idx = preprocess.encode(tuple(action)) if action else preprocess.encode(action)
            prior = prior_probabilities[0][idx]    # get prior probability
            child_node = MCTSNode(state=next_state, parent=self, prior_prob=prior)  # define mcts node
            # if all([repr(child_node) != repr(child) for child in self.children]):
            action = tuple(action) if action else action
            self.children[action] = child_node
            # self.children.append(child_node)
                
        return value.item()
    
    def backpropagate(self, state_value):
        self.num_visits += 1
        self.q_value += state_value
        if self.parent:
            self.parent.backpropagate(state_value)
    
class MCTS():
    def __init__(self, root: MCTSNode) -> None:
        self.root = root
        
    def search(self, policy_network, num_iterations=100, c_param=1.4, tau=1.5):
        for _ in range(num_iterations):
            node = self.root
            while not node.state.is_terminal():
                # print(i, node)
                if len(node.children) == 0:
                    # print(i, node, "expand")
                    # print(i, node.state.get_available_actions(), "available actions")
                    state_value = node.expand(policy_network)
                    node.backpropagate(state_value)
                    break
                node = node.upper_confidence_tree(c_param)
            if node.state.is_terminal():
                # print("END-----------------------------------")
                reward = node.state.get_reward()
                node.backpropagate(reward)
                
        dist = self.root.visit_distribution(tau)
        idx = torch.multinomial(torch.tensor(list(dist.values())), 1, replacement=False).item()
        # chosen_node = self.root.children[idx]
        chosen_node = list(self.root.children.values())[idx]
        action = preprocess.decode(list(dist.keys())[idx])
        action = list(action) if action else action
        # list(dist.keys())[idx]
        return chosen_node, action, dist
        # TODO: either stick to previous, where output the node OR change it to output the card
        best_action = node.best_child.state.game.game_hist[-1][1]
        return node.best_child, dist

def get_node(node, game: bt.BigTwoGame):
    player_idx = game.players.index(game.cur_player)
    mod_game = ModifyGame(game, player_idx)
    state = BigTwoState(mod_game)
    node_ = MCTSNode(state)
    
    if len(game.game_hist) < 4:
        return node_
    game_hist = game.game_hist[-4:]
    for _, card in game_hist:
        card = tuple(card) if card else card
        if card in node.children:
            node = node.children[card]
        else:
            return node_
    node.state = state
    return node

if __name__ == "__main__":
    input_dim, output_dim, hidden_dim = 143, 18880, 256
    dpg = model.deepPG(input_dim, output_dim, hidden_dim)
    dpg.load_state_dict(torch.load("alphazero.pt"))
    

    memory = deque(maxlen=100000)

    for i in range(100):
        print(f"-------- Match {i} --------")
        p1, p2, p3, p4 = "A", "B", "C", "D"
        t1, t2, t3, t4 = "Agent", "Agent", "Agent", "Agent"
        p_t = zip([p1,p2,p3,p4], [t1,t2,t3,t4])
        game = bt.BigTwoGame(p_t)

        self_play_data = []
        while not game.game_over():
            player_idx = game.players.index(game.cur_player)
            
            if f"node{player_idx}" not in locals():
                mod_game = ModifyGame(game, player_idx)
                state = BigTwoState(mod_game)
                locals()[f"node{player_idx}"] = MCTSNode(state)
            else:
                locals()[f"node{player_idx}"] = get_node(locals()[f"node{player_idx}"], game)
                
            # node = MCTSNode(state)
            mcts_ = MCTS(locals()[f"node{player_idx}"])
            node, action, dist = mcts_.search(dpg, 100)
            
            print(game.cur_player.name)
            table_card = next((p_c[1] for p_c in game.game_hist[-3:][::-1] if p_c[1] is not None), None)
            print(f"Available action: {game.cur_player.get_available_actions(table_card)}")
            print(f"Played: {action}")
            
            p = preprocess.Preprocess(game)
            # features = torch.tensor(p.get_hand_cards() + p.get_history(), dtype=torch.float)
            # features = torch.tensor(p.create_features(), dtype=torch.float)
            features = p.create_features()
            self_play_data.append((player_idx, features, dist))

            game.play_turn(action)

        game.display_winner()
            
        winner_idx = game.players.index(game.winner)
        for i, f, d in self_play_data:
            if i == winner_idx:
                memory.append((f, d, 1))
            else:
                memory.append((f, d, -1))
                
        df = pd.DataFrame(memory, columns=["features", "dist", "reward"])
        df.to_csv("memory2.csv", index=False)
    
        
        
        
        
        
    
    
    
    
#     if player_idx == 0:
#         if 'node0' not in locals():
#             node0 = MCTSNode(state)
#         node0 = get_node(node0, game)
#     elif player_idx == 1:
#         if 'node1' not in locals():
#             node1 = MCTSNode(state)
#         node1 = get_node(node1, game)
#     elif player_idx == 2:
#         if 'node2' not in locals():
#             node2 = MCTSNode(state)
#         node2 = get_node(node2, game)
#     elif player_idx == 3:
#         if 'node3' not in locals():
#             node3 = MCTSNode(state)
#         node3 = get_node(node3, game)
    
    
    
    
    
#     player_idx = game.players.index(game.cur_player)
#     mod_game = ModifyGame(game, player_idx)
    
#     if len(game.game_hist) < 4:
#         state = BigTwoState(mod_game)
#         node = MCTSNode(state)
        
#         locals()["abc"] = 5
#         abc
        
#         if player_idx == 0:
#             nnode
    
#     if player_idx == 0:
#         hist_card = game.game_hist[-3] if len(game.game_hist) > 0 else None
        
        
        
#         hist_card1 = game.game_hist[-3][1] if len(game.game_hist) > 0 else None
#         hist_card2 = game.game_hist[-2][1] if len(game.game_hist) > 0 else None
#         hist_card3 = game.game_hist[-1][1] if len(game.game_hist) > 0 else None
#         nodeA = copy.deepcopy(nodeA.children[hist_card1].children[hist_card2].children[hist_card3])
    
#     mcts_ = MCTS(f"node{player_idx}")   # variable    
    
    
#     player_idx = game.players.index(game.cur_player)
#     mod_game = ModifyGame(game, player_idx)
#     state = BigTwoState(mod_game)
#     node = MCTSNode(state)
#     mcts_ = MCTS(node)
#     node, action, dist = mcts_.search(dpg)
    
#     print(game.cur_player.name)
#     table_card = next((p_c[1] for p_c in game.game_hist[-3:][::-1] if p_c[1] is not None), None)
#     print(f"Available action: {game.cur_player.get_available_actions(table_card)}")
#     print(f"Played: {action}")
        
#     game.play_turn(action)
# game.display_winner()

    
    
#     new_node = copy.deepcopy(node.children[25].children[8].children[1])
    
    
    
    
    
    
    
    
#     import numpy as np

# class MCTSNode:
#     def __init__(self, state, parent=None):
#         self.state = state          # Current game state
#         self.parent = parent        # Parent node
#         self.children = {}          # Child nodes (action -> child node)
#         self.visit_count = 0        # Number of times the node was visited
#         self.total_value = 0        # Total value (for computing Q)
#         self.prior_prob = 0         # Prior probability from the policy network
#         self.is_expanded = False    # If the node has been expanded

#     def expand(self, action_priors):
#         """Expand the node by creating child nodes for all possible actions."""
#         self.is_expanded = True
#         for action, prob in action_priors:
#             if action not in self.children:
#                 self.children[action] = MCTSNode(self.state.perform_action(action), parent=self)
#                 self.children[action].prior_prob = prob

#     def update(self, value):
#         """Update the node with a new value estimate."""
#         self.visit_count += 1
#         self.total_value += value

#     def q_value(self):
#         """Return the average value (Q) of the node."""
#         return self.total_value / self.visit_count if self.visit_count > 0 else 0


# class MCTS:
#     def __init__(self, policy_value_fn, c_puct=1.0, n_simulations=1600):
#         """
#         Monte Carlo Tree Search (MCTS) algorithm for AlphaGo Zero.

#         Args:
#             policy_value_fn: Function that takes in a state and outputs action priors and state value.
#             c_puct: Constant to control exploration vs. exploitation.
#             n_simulations: Number of MCTS simulations per move.
#         """
#         self.policy_value_fn = policy_value_fn  # Neural network for policy and value
#         self.c_puct = c_puct                    # Exploration/exploitation constant
#         self.n_simulations = n_simulations      # Number of simulations

#     def search(self, root):
#         """Run MCTS for n_simulations starting from the root node."""
#         for _ in range(self.n_simulations):
#             node = root
#             search_path = [node]

#             # Selection: Traverse the tree until reaching a leaf node
#             while node.is_expanded:
#                 action, node = self.select(node)
#                 search_path.append(node)

#             # Expansion: Expand the leaf node using the policy network
#             action_priors, leaf_value = self.policy_value_fn(node.state)
#             node.expand(action_priors)

#             # Backpropagation: Update the nodes along the path with the value estimate
#             self.backpropagate(search_path, leaf_value)

#     def select(self, node):
#         """
#         Select an action using the PUCT formula:
#         U(s, a) = Q(s, a) + c_puct * P(s, a) * sqrt(N(s)) / (1 + N(s, a))
#         """
#         best_action, best_node = None, None
#         best_score = -np.inf
#         total_visits = np.sqrt(sum(child.visit_count for child in node.children.values()))

#         for action, child in node.children.items():
#             q = child.q_value()
#             u = self.c_puct * child.prior_prob * total_visits / (1 + child.visit_count)
#             score = q + u

#             if score > best_score:
#                 best_score = score
#                 best_action, best_node = action, child

#         return best_action, best_node

#     def backpropagate(self, search_path, value):
#         """Propagate the value back through the search path."""
#         for node in reversed(search_path):
#             node.update(value)
#             value = -value  # Reverse the value for the opponent's perspective

#     def get_action_probabilities(self, root, temperature=1.0):
#         """
#         Return the action probabilities based on visit counts.
#         The higher the visit count, the more confident the algorithm is about that action.
#         """
#         action_visits = [(action, child.visit_count) for action, child in root.children.items()]
#         actions, visits = zip(*action_visits)
#         visit_counts = np.array(visits, dtype=np.float32)
        
#         if temperature == 0:
#             # Select action deterministically (highest visit count)
#             probs = np.zeros_like(visit_counts)
#             probs[np.argmax(visit_counts)] = 1.0
#         else:
#             # Apply temperature (typically used for more exploration in early stages)
#             visit_counts = visit_counts ** (1 / temperature)
#             probs = visit_counts / np.sum(visit_counts)
        
#         return actions, probs

#     def get_best_move(self, root):
#         """Select the move with the highest visit count."""
#         actions, probs = self.get_action_probabilities(root, temperature=0)
#         return actions[np.argmax(probs)]


# # Example policy and value function (you would use a neural network here)
# def dummy_policy_value_fn(state):
#     """
#     A dummy function that simulates the neural network output for policy (action probabilities)
#     and value (expected win rate).
#     """
#     action_priors = [(action, 1.0 / len(state.get_legal_actions())) for action in state.get_legal_actions()]
#     value = np.random.uniform(-1, 1)  # Dummy value representing win probability
#     return action_priors, value

# # Example usage with a dummy game state:
# class GameState:
#     """Dummy class to simulate game logic."""
#     def get_legal_actions(self):
#         return [0, 1, 2, 3]  # Dummy actions

#     def perform_action(self, action):
#         return GameState()  # Returns a new game state

# # Example use of MCTS:
# root_state = GameState()
# root_node = MCTSNode(root_state)
# mcts = MCTS(dummy_policy_value_fn)
# mcts.search(root_node)

# # Get the best move based on the MCTS search
# best_move = mcts.get_best_move(root_node)
# print(f"Best move: {best_move}")
