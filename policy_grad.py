import torch
import torch.nn as nn
import torch.optim as optim

import big_two_AI as bt
import mcts
import preprocess

class deepPG(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dim) -> None:
        super().__init__()
        self.net = nn.Sequential(nn.Linear(input_dim, hidden_dim),
                                 nn.ReLU(),
                                 nn.Linear(hidden_dim, output_dim))
        self.optimizer = optim.Adam(self.net.parameters())
        
    def forward(self, x, avail_actions):
        raw_prob = self.net(x) + (avail_actions - 1) * 1e9
        return nn.Softmax(dim=0)(raw_prob)
    
all_actions = preprocess.all_actions
input_dim, output_dim, hidden_dim = 143, 18879, 256
dpg = deepPG(input_dim, output_dim, hidden_dim)
# dpg.load_state_dict(torch.load("against_random.pt"))
opt = optim.Adam(dpg.parameters())

win_rate = [0 for _ in range(4)]
for i in range(30000):
    p1, p2, p3, p4 = "A", "B1", "B2", "B3"
    t1, t2, t3, t4 = "Agent", "Bot", "Bot", "Bot"
    p_t = zip([p1,p2,p3,p4], [t1,t2,t3,t4])
    game = bt.BigTwoGame(p_t)

    opt.zero_grad()
    while not game.game_over():
        cur_player = game.cur_player
        table_card = next((p_c[1] for p_c in game.game_hist[-3:][::-1] if p_c[1] is not None), None)
        
        p = preprocess.Preprocess(game)
        # create features
        features = torch.tensor(p.create_features(), dtype=torch.float)
        # get available actions
        avail_act = cur_player.get_available_actions(table_card)
        none_bin = [0] if [bt.Card("Diamonds", "3")] in avail_act or table_card is None else [1] 
        avail_act_binary = [1 if list(act) in avail_act else 0 for act in all_actions] + none_bin
        avail_act_binary = torch.tensor(avail_act_binary, dtype=torch.float)
        # calculate probability distribution
        prob_dist = dpg(features, avail_act_binary)
        # select action based on probability distribution
        selected_index = torch.multinomial(prob_dist, num_samples=1).item()
        if selected_index in preprocess.num_to_act:
            action = list(preprocess.num_to_act[selected_index])
        else:
            action = None
        # calculate gradient        
        if cur_player.type in ["Agent", "AI"]:    # only focus on updating the actions of 1 agent although all players' actions are selected based on the same policy
            prob_dist[selected_index].backward()
        
        if i % 50 == 0:
            print(cur_player.name)
            print(f"Available action: {avail_act}")
            print(f"Played: {action}")
            
        game.play_turn(action)
    game.display_winner()

    reward = 1 if game.winner.type in ["Agent", "AI"] else -1

    for param in dpg.parameters():
        if param.grad is not None:
            param.grad *= -reward

    opt.step()
    
    winner_idx = [len(player.hand) == 0 for player in game.players].index(True)
    win_rate[winner_idx] += 1
    print(f"Game: {i+1}; Win rate: {[wr/(i+1) for wr in win_rate]}")
    
    if (i+1) % 1000 == 0:
        torch.save(dpg.state_dict(), "self_play_from0_more_feats_list.pt")