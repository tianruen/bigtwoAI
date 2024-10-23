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
        # return 1 if self.game.players[winner_idx].type in ["Agent", "AI"] else 0
        # return 1 if the agent (with index 0) win the game, otherwise 0
        
        return len(self.game.bot.hand) - len(self.game.players[0].hand)     # game.players[0] is the agent

class MCTSNode():
    def __init__(self, action, state:BigTwoState, parent:Optional["MCTSNode"]=None) -> None:
        self.id = action        # Top card on table / Action that leads to this node
        self.state = state      # cards that are played
        self.parent = parent
        self.children = []
        self.num_visits = 1
        self.num_wins = 0
    
    def __repr__(self) -> str:
        return f"{self.state.game.game_hist[-1][1]}" if len(self.state.game.game_hist) > 0 else "None"
        
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
        print(self)
        action = random.choice(self.state.get_available_actions())
        print(action)
        print("")
        for action in self.state.get_available_actions():
            state_ = copy.deepcopy(self.state)  # to avoid changing the state of the current node
            next_state = state_.move(action)
            child_node = MCTSNode(action=action, state=next_state, parent=self)
        # if all([repr(child_node) != repr(child) for child in self.children]):
            self.children.append(child_node)
        
        child_node = random.choice(self.children)
        return child_node
    
    def backpropagate(self, reward):
        self.num_visits += 1
        self.num_wins += reward
        if self.parent:
            self.parent.backpropagate(reward)
        
class MCTS():
    def __init__(self, root:MCTSNode) -> None:
        self.root = root
    
    def search(self, num_iterations=10) -> MCTSNode:
        # if only one action is available, return that action
        if len(self.root.state.get_available_actions()) == 1:
            return self.root.expand()
        
        result = 0
        for i in range(num_iterations):
            node = self.tree_policy()
            reward = self.rollout_policy(node.state)
            node.backpropagate(reward)
            
            result += reward
            # print(result, "/", i+1)
            
        return self.root.best_child(c_param=0)
    
    def tree_policy(self) -> MCTSNode:
        node = self.root
        while not node.state.is_terminal():
            # if not node.is_fully_expanded():
            #     print("Node not fully expanded")
            #     return node.expand()
            # else:
            #     print("Node fully expanded")
            #     node = node.best_child()
            if not node.children:
                return node.expand()
            else:
                node = node.best_child()
        return node
    
    def rollout_policy(self, state:BigTwoState):
        state_ = copy.deepcopy(state)
        while not state_.is_terminal():
            action = random.choice(state_.get_available_actions())
            # print("Player: ", state_.player.name, "Action: ", action, "Table cards: ", state_.table_cards)
            state_ = state_.move(action)
        return state_.get_reward()

# if __name__ == "__main__":
#     p1, p2, p3, p4 = "A", "B1", "B2", "B3"
#     t1, t2, t3, t4 = "Agent", "Bot", "Bot", "Bot"
#     p_t = zip([p1,p2,p3,p4], [t1,t2,t3,t4])
#     game = ModifyGame(p_t)
#     # print(game.cur_player)
    
#     state = BigTwoState(game)
#     root = MCTSNode(state)
#     mcts_ = MCTS(root)
#     best_action = mcts_.search()
#     print(best_action)            