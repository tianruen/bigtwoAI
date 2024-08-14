from big_two_AI_draft import Card
from collections import defaultdict
import itertools

class Combo:
    
    ############ DOUBLE or TRIPLE ############
    def filter_cards_combinations_23(player_hand, card_length):
        
        grouped_cards_rank = defaultdict(list)
        
        ## Group all cards with same rank 
        for card in player_hand:
            r = card.rank
            grouped_cards_rank[r].append(card)
        
        ## Filter away group with quantity lower than current card_length
        ## They can't be played
        temp_filtered_groups = [group for group in grouped_cards_rank.values() if len(group) >= card_length]
        filtered_groups = []

        # Find all possible combinations following card_length
        # Using itertools.combinations
        for group in temp_filtered_groups:
            
            filtered_groups.extend(itertools.combinations(group, card_length))

        # change filtered_groups from iterables to list
        filtered_groups = [list(item) for item in filtered_groups]
        
        return filtered_groups

    
    ############ FIVE CARDS ############
    def filter_cards_combinations_5(player_hand):
        
        grouped_cards_rank = defaultdict(list)
        grouped_cards_suit = defaultdict(list)
        five_card_combo = []
        
        ## Group all cards with same rank 
        for card in player_hand:
            r = card.rank
            grouped_cards_rank[r].append(card)

        for card in player_hand:
            s = card.suit
            grouped_cards_suit[s].append(card)
        
        add_FourOfAKindCombo(grouped_cards_rank, five_card_combo)
        add_ThreeOfAKindCombo(grouped_cards_rank, five_card_combo)
        add_Flush(grouped_cards_suit, five_card_combo)
        add_Straight(grouped_cards_rank, five_card_combo)

        # There might be repetition of combinations:
        # Royal flush might be included twice from add_Flush and add_Straight
        # We remove duplicates!
        five_card_combo = list(dict.fromkeys(tuple(item) for item in five_card_combo))
        five_card_combo = [list(item) for item in five_card_combo]    # Is this necessary? (Changing all elements from tuple(?) to list)

        return five_card_combo



#################################################################
######### METHODS ASSISTING FILTER_CARDS_COMBINATIONS_5 #########
#################################################################
#####
    # Those are:
    #   add_FourOfAKindCombo
    #   add_ThreeOfAKindCombo
    #   add_Flush
    #   add_Straight
#####

def add_FourOfAKindCombo(grouped_cards_rank, five_card_combo):
    # 4 of a kind , LETS GO
    
    # grouped_cards_rank is a dictionary with ranks as key and the value are all the cards with the rank
    # find groups that has at least four cards
    # Name these groups DISH
    dish = [group for group in grouped_cards_rank.values() if len(group) == 4]

    for food in dish:
        sauce = grouped_cards_rank.copy()

        # Exclude group of the chosen rank
        # Then sauce.remove(food)
        # But dict doesn't allow it to be easy, so we do following
        # Shit
        for key, value in sauce.items():
            if value == food:
                del sauce[key]
                break

        # Now we transform sauce from dict to list
        # Without key(rank)
        # SAUCE is now single cards to be paired with DISH
        sauce = [item for value_list in sauce.values() for item in value_list]

        # PAIR THE SHIT OUT OF THEM, AND MAKE A FKING MEAL
        for liao in sauce:
            meal = food.copy()
            meal.append(liao)                   # Can't do extend because liao is single Card object, not iterable list of Card object(?)
            five_card_combo.append(meal)        # five_card_combo is not returned because the five_card_combo passed in is a list
                                                # It is iterable, thus it is original
                                                # Meaning changing five_card_combo here also directly modify original five_card_combo

def add_ThreeOfAKindCombo(grouped_cards_rank, five_card_combo):
    # 3 of a kind , LETS GO

    # grouped_cards_rank is a dictionary with ranks as key and the value are all the cards with the rank
    # find groups that has at least three cards
    # Name these groups TEMP_DISH, because we are going to do some combo
    temp_dish = [group for group in grouped_cards_rank.values() if len(group) >= 3]
    dish = []

    # TEMP_DISH goes through combo
    # and we have fucking dishes
    # group DISH contains all possible 3 card combinations
    for plate in temp_dish:
        dish.extend(itertools.combinations(plate, 3))
    dish = [list(item) for item in dish]
    
    for food in dish:
        temp_sauce = grouped_cards_rank.copy()

        # Exclude group of the chosen rank
        # Concept is like temp_sauce.remove(food)
        for key, value in temp_sauce.items():
            if all(item in value for item in food):
                del temp_sauce[key]
                break
        # TEMP_SAUCE group now contains all the group except chosen rank group

        # Find groups that has at least two cards
        # At the same time we transform TEMP_SAUCE from dict to list
        temp_sauce = [group for group in temp_sauce.values() if len(group) >= 2]
        
        sauce = []

        # TEMP_SAUCE goes through combo
        # and we have fucking sauces
        # group SAUCE contains all possible 2 card combinations
        for bowl in temp_sauce:
            sauce.extend(itertools.combinations(bowl, 2))
        sauce = [list(item) for item in sauce]
        
        # PAIR THE SHIT OUT OF THEM, AND MAKE A FKING MEAL
        for liao in sauce:
            meal = food.copy()
            meal.extend(liao)                   # Can't do append because it creates list within list
            five_card_combo.append(meal)        # five_card_combo is not returned because the five_card_combo passed in is a list
                                                # It is iterable, thus it is original
                                                # Meaning changing five_card_combo here also directly modify original five_card_combo

def add_Flush(grouped_cards_suit, five_card_combo):
    temp_meal = [group for group in grouped_cards_suit.values() if len(group) >= 5]
    meal = []

    for course in temp_meal:
        meal.extend(itertools.combinations(course, 5))
    meal = [list(item) for item in meal]
    
    five_card_combo.extend(meal)                # five_card_combo is not returned because the five_card_combo passed in is a list
                                                # It is iterable, thus it is original
                                                # Meaning changing five_card_combo here also directly modify original five_card_combo

def add_Straight(grouped_cards_rank, five_card_combo):
    # Straights, LETS GO

    # Create ranks that would be used as reference later
    ranks = Card.ranks
    meal = []

    # From 3-7 until J-2
    for i in range(len(ranks) - 4):
        
        # This is the reference
        possible_straight_ranks = ranks[i:i+5]
        possible_meal = []

        for rank in possible_straight_ranks:
            
            # If we found the rank contains card
            # we include it into POSSIBLE_MEAL
            if grouped_cards_rank[rank]:
                possible_meal.append(grouped_cards_rank[rank])
            # AND we gg if it didn't find
            else:
                break
    
        # POSSIBLE_MEAL will contain five cards
        # if there is five cards
        if len(possible_meal) == 5:

            # And we find all combinations to form the straight
            # E.g. 3-7 but we have 3 diamonds and 3 clubs
            # And we have a MEAL!
            meal.extend(itertools.product(*possible_meal))
            
    # Transform all collected MEALs from iterable to list!
    meal = [list(item) for item in meal]

    # AND SERVE THOSE FKING MEALS
    five_card_combo.extend(meal)                # five_card_combo is not returned because the five_card_combo passed in is a list
                                                # It is iterable, thus it is original
                                                # Meaning changing five_card_combo here also directly modify original five_card_combo


#################################################################
######### METHODS ASSISTING FILTER_CARDS_COMBINATIONS_5 #########
#################################################################