import os
import time
import importlib
import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom

import advsearch.timer as timer

def player_name(player_dir:str) -> str:
    """
    Removes leading 'advsearch.' or 'advsearch/' from the player directory
    :param player_dir:
    :return:
    """
    if player_dir.startswith('advsearch'):
        return player_dir[len('advsearch')+1:]  # +1 to account for the / or .

class Server(object):
    """
    Othello server, implements a simple playing protocol based on function calls

    """

    def __init__(self, game_type, p1_agent, p2_agent, delay, history, output, pace=0):
        """
        Initializes the Game server
        :param game_type: type of game to play (othello, tttm for tic-tac-toe misere)
        :param p1_dir: directory where the 'agent.py' of the 1st player is located
        :param p2_dir: directory where the 'agent.py' of the 2nd player is located
        :param delay: time limit to make a move
        :param history: file that will contain the match history (plain text)
        :param output: file to save game details (includes history)
        :param pace: time to wait to display a move, if a player returns before timeout
        """

        if game_type not in {'othello', 'tttm'}:
            raise ValueError(f"Unknown game type '{game_type}'. Allowed types are othello' and 'tttm'")

        if game_type == 'othello':
            from advsearch.othello.board import Board 
            from advsearch.othello.gamestate import GameState
        else:
            from advsearch.tttm.board import Board
            from advsearch.tttm.gamestate import GameState


        # normalizes paths to avoid errors with trailing slashes
        p1_agent = os.path.normpath(p1_agent)
        p2_agent = os.path.normpath(p2_agent)

        # retrieves dir and file names for both players
        p1_dir = os.path.dirname(p1_agent)
        p2_dir = os.path.dirname(p2_agent)

        self.basedir = os.path.abspath('.')

        self.player_dirs = {'B': p1_dir, 'W': p2_dir}

        self.player_colors = ['B', 'W']
        self.color_names = ['black', 'white']
        self.state = GameState(Board(), 'B')
        self.last_player = None

        self.history = []  # a list of performed moves (tuple: ((x,y), color)
        self.history_file = open(history, 'w')
        self.output_file = output

        self.delay = delay
        self.pace = pace

        self.result = None

        # start and finish times of match
        self.start = None
        self.finish = None

        # replaces / or \ with . and removes .py extension for both agentes
        p1_agent, p2_agent = p1_agent.replace(os.sep, '.'), p2_agent.replace(os.sep, '.')
        p1_agent, p2_agent = os.path.splitext(p1_agent)[0], os.path.splitext(p2_agent)[0]
        
        self.player_modules = {
            'B': importlib.import_module(p1_agent),
            'W': importlib.import_module(p2_agent),
        }

    def __del__(self):
        self.history_file.close()

    def run(self):
        self.start = time.localtime()

        illegal_count = {'B': 0, 'W': 0}  # counts the number of illegal move attempts

        print(f'---- Current match: {self.player_dirs["B"]} (B) x (W) {self.player_dirs["W"]} ----')
        print('Initial board:')
        print(self.state.board.decorated_str(colors=False))

        while True:  # runs until endgame
            # creates auxiliary variables for better readability
            current_player = self.state.player
            opponent = 'W' if current_player == 'B' else 'B'

            # calculates scores
            if self.state.game_name == 'Othello':
                p1_score = self.state.board.num_pieces('B') 
                p2_score = self.state.board.num_pieces('W') 
            else:
                winner = self.state.winner()
                p1_score = 1 if winner == 'B' else -1 if winner == 'W' else 0
                p2_score = -1 if winner == 'B' else 1 if winner == 'W' else 0

            print(f'---- Current match: {self.player_dirs["B"]} (B) x (W) {self.player_dirs["W"]} ----')

            # checks whether both players don't have available moves (end of game)
            if self.state.is_terminal():

                print('End of game reached! Scores:')
                print(f'Player 1 (B - {self.player_dirs["B"]}): {p1_score}')
                print(f'Player 2 (W - {self.player_dirs["W"]}): {p2_score}')

                if p1_score > p2_score:
                    print(f'Player 1 (B - {self.player_dirs["B"]} wins!')
                elif p2_score > p1_score:
                    print(f'Player 2 (W - {self.player_dirs["W"]}) wins!')
                else:
                    print('Draw!')

                self.result = 0 if p1_score > p2_score else 1 if p2_score > p1_score else 2
                self.finish = time.localtime()
                return self.result
            
            # disqualify player if it attempts illegal moves 5 times in a row
            if illegal_count[current_player] >= 5:
                print(f'Player {current_player} ({self.player_dirs[current_player]}) DISQUALIFIED! Too many illegal move attempts.')
                print('End of game reached!')
                print('Player 1 (B): %d' % p1_score)
                print('Player 2 (W): %d' % p2_score)

                self.result = 0 if current_player == 'W' else 1
                self.finish = time.localtime()
                return self.result

            # if this player is moving twice, shows a message that the opponent has no legal moves
            if self.last_player == current_player:
                print(f'Player {opponent} ({self.player_dirs[opponent]}) has no legal moves. {self.player_dirs[current_player]} will play again')
                time.sleep(self.pace)

            # creates a copy of the state, so that player can do whathever it wants
            state_copy = self.state.copy()

            # calls current player's make_move function with the specified timeout
            start = time.time()
            function_call = timer.FunctionTimer(self.player_modules[current_player].make_move, (state_copy,))  # argument must be a 1-element tuple
            
            delay = 60 if player_name(self.player_dirs[current_player]) == "humanplayer" else self.delay
            move = function_call.run(delay)
                
            elapsed = time.time() - start

            if move is None:  # detects timeout
                print(f'Player {current_player} has not made a move and lost its turn. Illegal moves count incremented')
                illegal_count[current_player] += 1
                continue

            move_x, move_y = move

             # checks for move validity
            if not isinstance(move_x, int) or not isinstance(move_y, int):
                print(f'ILLEGAL MOVE! x, y are {type(move_x)}, {type(move_y)} but should be integer!')
                move_x = move_y = -1  # -1 is my code for type error
                #illegal_count[current_player] += 1


            # saves move in history
            self.history_file.write('%d,%d,%s\n' % (move_x, move_y, current_player))
            self.history.append(((move_x, move_y), current_player))

            if self.state.is_legal_move(move):   
                print('Player %s move %d,%d accepted.' % (current_player, move_x, move_y))
            
                self.last_player = current_player           # records the player that just moved
                self.state = self.state.next_state(move)  

            else:
                print(f'Player {current_player} move {move}_ILLEGAL!')
                illegal_count[current_player] += 1

            # waits the remaining time, if needed
            if self.pace - elapsed > 0:
                time.sleep(self.pace - elapsed)

            print('Current board:')
            print(self.state.board.decorated_str(
                colors=False, move=(move_y, move_x), highlight_flipped=True
            ))


    def write_output(self):
        """
        Writes a xml file with detailed match data
        :return:
        """
        os.chdir(self.basedir)

        root = ET.Element('othello-match')

        colors = ['B', 'W']
        self.player_dirs['None'] = '?'  # trick for writing a draw match

        timing = ET.SubElement(root, 'timing')
        timing.set('start', time.asctime(self.start))
        timing.set('finish', time.asctime(self.finish))

        if self.state.game_name == 'Othello':
            scores = {
                'B': self.state.board.piece_count['B'], 
                'W': self.state.board.piece_count['W']
            }
        else:
            winner = self.state.winner()
            scores = {
                'B': 1 if winner == 'B' else -1 if winner == 'W' else 0, 
                'W': -1 if winner == 'B' else 1 if winner == 'W' else 0, 
            }

        for color in colors:
            elem = ET.SubElement(root, 'player')
            elem.set('directory', self.player_dirs[color])
            elem.set('color', color)
            opp_color = 'W' if color == 'B' else 'B'
            result = 'win' if scores[color] > scores[opp_color] else 'loss' if scores[color] < scores[opp_color] else 'draw'
            elem.set('result', result)
            elem.set('score', str(scores[color]))

        moves = ET.SubElement(root, 'moves')

        for coords, color in self.history:
            move = ET.SubElement(moves, 'move')
            move.set('coord', '%d,%d' % coords)
            move.set('color', color)

        # preety xml thanks to: https://stackoverflow.com/a/1206856/1251716
        ugly_xml = ET.tostring(root).decode('utf-8')
        dom = xml.dom.minidom.parseString(ugly_xml)  # or xml.dom.minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml()
        f = open(self.output_file, 'w')
        f.write(pretty_xml)
        f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Game server.')

    parser.add_argument('game_type', type=str, choices=['tttm', 'othello'],
                        help='Choose the game type: "tttm" (tic-tac-toe misere) or "othello"')

    parser.add_argument('players', metavar='player', type=str, nargs=2,
                        help='Path to player directory')
    parser.add_argument('-d', '--delay', type=float, metavar='delay',
                        default=5.0,
                        help='Time allocated for players to make a move.')

    parser.add_argument('-p', '--pace', type=float,
                        default=0,
                        help='Pace of the match: time to wait to display a move '
                             '(if a player returns a move before the delay/timeout).')

    parser.add_argument('-l', '--log-history', type=str, dest='history',
                        default='history.txt', metavar='log-history',
                        help='File to save game log (history).')

    parser.add_argument('-o', '--output-file', type=str, dest='output',
                        default='results.xml', metavar='output-file',
                        help='File to save game details (includes history)')

    args = parser.parse_args()
    p1, p2 = args.players

    s = Server(args.game_type, p1, p2, args.delay, args.history, args.output, args.pace)
    s.run()
    s.write_output()
