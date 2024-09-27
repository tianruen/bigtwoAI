import copy
import math
import random
from typing import List, Optional, Tuple

import big_two_AI as bt

class ModifyGame(bt.BigTwoGame):
    def __init__(self, player_names_types:List[Tuple[str,str]]) -> None:
        self.players = [bt.Player(n, t) for n, t in player_names_types]
        self.deck = bt.Deck()
        self.distribute_cards()
        self.combine_bot()
        self.starting_player()
        self.bot_play = 1 if self.cur_player.type not in ["Agent", "AI"] else 0   # to record the number of times bot plays. If more than 3, then its agent turn        
        self.game_hist = []
        
    def combine_bot(self):
        self.bot = bt.Player("CombBot", "Bot")
        for player in self.players:
            if player.type not in ["Agent", "AI"]:
                self.bot.hand.extend(player.hand)
        self.players = [player for player in self.players if player.type in ["Agent", "AI"]]
        self.players.append(self.bot)
                
    def next_player(self, cur_player):
        if self.bot_play > 3:
            self.bot_play = 0
            return self.players[0] # since the agent is always the first player
        else:
            self.bot_play += 1
            return self.bot
        
class BigTwoState():
    def __init__(self, game:ModifyGame) -> None:
        self.game = copy.deepcopy(game)
        self.player = self.game.cur_player
        self.table_cards = next((p_c[1] for p_c in self.game.game_hist[-3:][::-1] if p_c[1] is not None), None)   # p_c: (player, played_cards)
        
    def available_actions_indi(self, hand_cards:List[List[bt.Card]]):
        first_round = []
        if self.table_cards is not None:
            cards_length = len(self.table_cards)
            if cards_length == 1:
                available_actions = bt.findSingle(hand_cards, self.table_cards)
            elif cards_length == 2:
                available_actions = bt.findDouble(hand_cards, self.table_cards)
            elif cards_length == 3:
                available_actions = bt.findTriple(hand_cards, self.table_cards)
            elif cards_length == 5:
                available_actions = bt.findFiveCardsCombo(hand_cards, self.table_cards)
            available_actions.append(None)
        else:
            available_actions = []
            available_actions.extend([[card] for card in hand_cards])                         # Add possible Single plays
            available_actions.extend(bt.Combo.filter_cards_combinations_23(hand_cards, 2))       # Add possible Double plays
            available_actions.extend(bt.Combo.filter_cards_combinations_23(hand_cards, 3))       # Add possible Triple plays
            available_actions.extend(bt.Combo.filter_cards_combinations_5(hand_cards))           # Add possible Five Cards combo
            first_round = [act for act in available_actions if bt.Card("Diamonds", "3") in act]
        return first_round if first_round else available_actions
    
    def get_available_actions(self):
        if self.player.type in ["Agent", "AI"]:
            return self.available_actions_indi(self.player.hand)
        else:
            available_actions = []
            for player in self.game.players:
                if player.type not in ["Agent", "AI"]:
                    available_actions.extend(self.available_actions_indi(player.hand))
            return available_actions
    
    def move(self, action:List[bt.Card]):
        self.game.play_turn(action)
        return BigTwoState(self.game)
    
    def is_terminal(self):
        return self.game.game_over()
        # return len(self.game.cur_player.hand) == 0
        
    def get_reward(self):
        winner_idx = [len(p.hand) == 0 for p in self.game.players].index(True)
        return 1 if self.game.players[winner_idx].type in ["Agent", "AI"] else 0
        # return 1 if the agent (with index 0) win the game, otherwise 0

class MCTSNode():
    def __init__(self, state:BigTwoState, parent:Optional["MCTSNode"]=None, parent_action:List[bt.Card]=None) -> None:
        self.state = state      # cards that are played
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.num_visits = 0
        self.num_wins = 0
        
    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_available_actions())
    
    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.num_wins / child.num_visits) + c_param * math.sqrt((2 * math.log(self.num_visits) / child.num_visits))
            for child in self.children
        ]
        argmax = choices_weights.index(max(choices_weights))
        return self.children[argmax]
            
    def expand(self):
        action = random.choice(self.state.get_available_actions())
        next_state = self.state.move(action)
        child_node = MCTSNode(state=next_state, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node
    
    def backpropagate(self, reward):
        self.num_visits += 1
        self.num_wins += reward
        if self.parent:
            self.parent.backpropagate(reward)
        
class MCTS():
    def __init__(self, root:MCTSNode) -> None:
        self.root = root
    
    def search(self, num_iterations=10):
        result = 0
        for i in range(num_iterations):
            node = self.tree_policy()
            reward = self.rollout_policy(node.state)
            node.backpropagate(reward)
            
            result += reward
            print(result, "/", i+1)
            
        return self.root.best_child()
    
    def tree_policy(self) -> MCTSNode:
        node = self.root
        while not node.state.is_terminal():
            if not node.is_fully_expanded():
                return node.expand()
            else:
                node = node.best_child()
        return node
    
    def rollout_policy(self, state:BigTwoState):
        state_ = copy.deepcopy(state)
        while not state_.is_terminal():
            action = random.choice(state_.get_available_actions())
            state_ = state_.move(action)
        return state_.get_reward()

if __name__ == "__main__":
    p1, p2, p3, p4 = "A", "B1", "B2", "B3"
    t1, t2, t3, t4 = "Agent", "Bot", "Bot", "Bot"
    p_t = zip([p1,p2,p3,p4], [t1,t2,t3,t4])
    game = ModifyGame(p_t)
    print(game.cur_player)
    
    state = BigTwoState(game)
    root = MCTSNode(state)
    mcts_ = MCTS(root)
    best_action = mcts_.search()
    
    
    
    
    
    
# class Node:
#     def __init__(self, state, parent=None):
#         self.state = state
#         self.parent = parent
#         self.children = []
#         self.visits = 0
#         self.value = 0

#     def is_fully_expanded(self):
#         return len(self.children) == len(self.state.get_legal_actions())

#     def best_child(self, c_param=1.4):
#         choices_weights = [
#             (child.value / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
#             for child in self.children
#         ]
#         return self.children[choices_weights.index(max(choices_weights))]

#     def expand(self):
#         action = random.choice(self.state.get_legal_actions())
#         next_state = self.state.move(action)
#         child_node = Node(next_state, self)
#         self.children.append(child_node)
#         return child_node

#     def update(self, reward):
#         self.visits += 1
#         self.value += reward

# class MCTS:
#     def __init__(self, root):
#         self.root = root

#     def search(self, iterations=1000):
#         for _ in range(iterations):
#             node = self.tree_policy()
#             reward = self.default_policy(node.state)
#             self.backup(node, reward)
#         return self.root.best_child(c_param=0)

#     def tree_policy(self):
#         node = self.root
#         while not node.state.is_terminal():
#             if not node.is_fully_expanded():
#                 return node.expand()
#             else:
#                 node = node.best_child()
#         return node

#     def default_policy(self, state):
#         while not state.is_terminal():
#             action = random.choice(state.get_legal_actions())
#             state = state.move(action)
#         return state.get_reward()

#     def backup(self, node, reward):
#         while node is not None:
#             node.update(reward)
#             node = node.parent
            