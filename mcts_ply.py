import time
import copy
import big_two_AI as bt
import mcts

# s = time.time()

# win_rate = [0 for _ in range(4)]
# n = 50
# for i in range(n):
#     p1, p2, p3, p4 = "A", "B1", "B2", "B3"
#     t1, t2, t3, t4 = "Agent", "Bot", "Bot", "Bot"
#     p_t = zip([p1,p2,p3,p4], [t1,t2,t3,t4])
#     game = bt.BigTwoGame(p_t)

#     while not game.game_over():
#         cur_player = game.cur_player
#         table_card = next((p_c[1] for p_c in game.game_hist[-3:][::-1] if p_c[1] is not None), None)
        
#         if cur_player.type in ["Agent", "AI"]:
#             # modify game for mcts (combine all bots to become a single player)
#             p1_, p2_, p3_, p4_ = "A", "B1", "B2", "B3"
#             t1_, t2_, t3_, t4_ = "Agent", "Bot", "Bot", "Bot"
#             p_t = zip([p1_,p2_,p3_,p4_], [t1_,t2_,t3_,t4_])
#             mod_game = mcts.ModifyGame(p_t)
#             mod_game.players = copy.deepcopy(game.players)
#             mod_game.combine_bot()
#             mod_game.cur_player = mod_game.players[0]   # since AI agent is the first player
#             mod_game.game_hist = copy.deepcopy(game.game_hist)
#             avail_act = mod_game.cur_player.get_available_actions(table_card)
            
#             state = mcts.BigTwoState(mod_game)
#             root = mcts.MCTSNode(state)
#             mcts_ = mcts.MCTS(root)
#             best_action = mcts_.search(num_iterations=500)
#             action = best_action.state.game.game_hist[-1][1]
#         else:
#             avail_act = cur_player.get_available_actions(table_card)
#             action = cur_player.get_action(avail_act)

#         print(cur_player.name)
#         print(f"Available action: {avail_act}")
#         print(f"Played: {action}")
            
#         game.play_turn(action)
#     game.display_winner()
    
#     winner_idx = [len(player.hand) == 0 for player in game.players].index(True)
#     win_rate[winner_idx] += 1
#     print(i+1)
#     print([wr/(i+1) for wr in win_rate])
#     print("-----------------------------")
    
# e = time.time()
# print((e-s)/60)

p1_, p2_, p3_, p4_ = "A", "B1", "B2", "B3"
t1_, t2_, t3_, t4_ = "Agent", "Bot", "Bot", "Bot"
p_t = zip([p1_,p2_,p3_,p4_], [t1_,t2_,t3_,t4_])
mod_game = mcts.ModifyGame(p_t)

print(mod_game.cur_player)

state = mcts.BigTwoState(mod_game)
root = mcts.MCTSNode(state)
mcts_ = mcts.MCTS(root)
best_action = mcts_.search(num_iterations=500)

for item in root.children:
    print(item)


    #WORKS.. Now how to retrieve them..?
