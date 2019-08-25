###############################################################################
# FILE : ai.py
# WRITER : Ori Becher, orib_222 ,Bar Schwartz, bar4411
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION: contains class AI with sophisticated ai algorithm.
###############################################################################

import random


class AI:

    def find_legal_move(self, game, func, timeout=None):
        """finds ai's legal next move"""
        beta = 2
        alpha = -2
        max_depth = 4
        # In the choise of max_depth there's
        # trade of between runtime and events anticipation
        non_valid_col = -1

        start_depth = 0
        cols = random.sample(range(len(game.board[0])), len(game.board[0]))

        alpha_beta_pruning(func, game, start_depth, max_depth, alpha, beta, True,
                           cols, {})
        return func(non_valid_col)


def alpha_beta_pruning(func, game, depth, max_depth, a, b, player, cols, dict_opt):
    """performs alpha beta pruning algortihm to find
        the best next move. See more details in the README file """

    heuristic_scores = [-1, 0, 1]
    num_players = 2
    start_depth = 0
    # base cases

    if game.get_winner()[0] == game.PLAYER_ONE:

        return heuristic_scores[2]
    elif game.get_winner()[0] == game.PLAYER_TWO:
        return heuristic_scores[0]
    if depth == max_depth + 1:
        return heuristic_scores[1]
    for each_player in (True, False):
        if each_player != player:
            continue
        else:
            for col in cols:
                try:
                    game.set_turn(player)
                    game.make_move(col)
                except:
                    continue
                if player:
                    a = max(a, alpha_beta_pruning(func, game, depth + 1,
                                                  max_depth, a, b, False, cols, dict_opt))
                else:
                    b = min(b, alpha_beta_pruning(func, game, depth + 1,
                                                  max_depth, a, b, True, cols, dict_opt))
                if depth == start_depth:
                    dict_opt[col] = a
                    best_col = max(dict_opt, key=lambda k: dict_opt[k])
                    func(best_col)
                game.set_turn(player)
                game.remove_move(col)
                if a >= b:
                    break

    return a if player else b

