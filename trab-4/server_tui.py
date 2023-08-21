import os
import sys
import time
import importlib
import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom
from pytermgui import tim, ansi_interface  # for TUI (text user interface) - install with 'pip install pytermgui'

from advsearch.othello.board import Board
from advsearch.othello.gamestate import GameState
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

    SCREEN_BOARD_POSITION = (0, 2)  # col, row of board position on screen

    def __init__(self, p1_dir, p2_dir, delay, history, output, pace=0):
        """
        Initializes the Othello game server
        :param p1_dir: directory where the 'agent.py' of the 1st player is located
        :param p2_dir: directory where the 'agent.py' of the 2nd player is located
        :param delay: time limit to make a move
        :param history: file that will contain the match history (plain text)
        :param output: file to save game details (includes history)
        :param pace: time to wait to display a move, if a player returns before timeout
        """
        # normalizes paths to avoid errors with trailing slashes
        p1_dir = os.path.normpath(p1_dir)
        p2_dir = os.path.normpath(p2_dir)

        self.basedir = os.path.abspath('.')

        self.player_dirs = {Board.BLACK: p1_dir, Board.WHITE: p2_dir}

        self.player_colors = [Board.BLACK, Board.WHITE]
        self.color_names = ['black', 'white']
        self.state = GameState(Board(), Board.BLACK)    # initial state, where black begins playing
        self.last_player = None  # player that made the last move

        self.history = []  # a list of performed moves (tuple: ((x,y), color)
        self.history_file = open(history, 'w')
        self.output_file = output

        self.delay = delay
        self.pace = pace

        self.result = None

        # start and finish times of match
        self.start = None
        self.finish = None

        # imports 'agent.py' from both players
        p1_module = p1_dir.replace(os.sep, '.')
        p2_module = p2_dir.replace(os.sep, '.')
        self.player_modules = {
            Board.BLACK: importlib.import_module(f"{p1_module}.agent"),
            Board.WHITE: importlib.import_module(f"{p2_module}.agent"),
        }

    def __del__(self):
        self.history_file.close()

    def print_header(self):
        board = self.state.board
        tim.print(
            f'[@green]{player_name(self.player_dirs[Board.BLACK])} ({board.num_pieces(Board.BLACK):02d} [black]⬤[/fg]) '
            f'x ([ffffff]⬤[/fg] {board.num_pieces(Board.WHITE):02d}) [@green]{player_name(self.player_dirs[Board.WHITE])} [/bg]'
        )

    def display_board(self, move=None, flipped=False) -> None:
        """
        Displays the board on screen
        :param move: move position to highlight or None
        :param flipped: whether to highlight latest flipped pieces
        :return:
        """
        ansi_interface.move_cursor(self.SCREEN_BOARD_POSITION)
        tim.print(self.state.board.decorated_str(move=move, highlight_flipped=flipped))
        sys.stdout.flush()

    def run(self) -> int:
        """
        Runs the game and returns the winner (0 or 1)
        :return: game winner (0 for 1st player, 1 for 2nd)
        """
        self.start = time.localtime()
        #player_num = 0
        move_xy = None
        illegal_count = {Board.BLACK: 0, Board.WHITE:0}  # counts the number of illegal move attempts

        ansi_interface.clear()
        sys.stdout.flush()

        while True:  # runs until endgame
            start = time.time()

            current_player = self.state.player
            opponent = Board.WHITE if current_player == Board.BLACK else Board.BLACK

            # calculates scores
            p1_score = self.state.board.num_pieces(Board.BLACK) #sum([1 for char in str(self.board) if char == self.board.BLACK])
            p2_score = self.state.board.num_pieces(Board.WHITE) #sum([1 for char in str(self.board) if char == self.board.WHITE])

            ansi_interface.cursor_home()
            self.print_header()
            self.display_board()
            #time.sleep(.5)  # waits a time for board visualization

            ansi_interface.clear('eos')

            # checks whether both players don't have available moves (end of game)
            if self.state.is_terminal():

                print('Game finished!')
                if p1_score > p2_score:
                    print(f'Player 1 (B - {self.player_dirs[Board.BLACK]}) wins!')
                    self.result = 0
                elif p2_score > p1_score:
                    print(f'Player 2 (W - {self.player_dirs[Board.WHITE]}) wins!')
                    self.result = 1
                else:
                    print('Draw!')
                    self.result = 2

                self.finish = time.localtime()
                return self.result
            
            # disqualify player if it attempts illegal moves 5 times in a row
            if illegal_count[current_player] >= 5:
                print(f'Player {current_player} ({self.player_dirs[current_player]}) DISQUALIFIED! Too many illegal move attempts or timeouts.')
                print('Game finished!')

                # black (player 0) wins if white was disqualified and vice versa
                self.result = 0 if current_player == Board.WHITE else 1
                self.finish = time.localtime()
                self.display_board()
                time.sleep(1)  # waits a time for board visualization
                return self.result

            # if this player is moving twice, shows a message that the opponent has no legal moves
            if self.last_player == current_player:
                print(f'Player {opponent} ({self.player_dirs[opponent]}) has no legal moves. {self.player_dirs[current_player]} will play again')
                time.sleep(self.pace)

            # creates a copy of the state, so that player can do whathever it wants
            state_copy = self.state.copy()

            # calls current player's make_move function with the specified timeout
            function_call = timer.FunctionTimer(self.player_modules[current_player].make_move, (state_copy,))  # argument must be a 1-element tuple
            
            delay = 60 if player_name(self.player_dirs[current_player]) == "humanplayer" else self.delay
            move_xy = function_call.run(delay)      # move in x,y coordinates (human convention)

            # checks for timeout
            if move_xy is None:  # detects timeout
                print(f'Player {current_player} TIMED OUT. Illegal moves count incremented')
                illegal_count[current_player] += 1
                #player = 1 - player
                #continue
                move_xy = -2, -2  # -2 is my code for timeout

            move_x, move_y = move_xy
            move_yx = (move_y, move_x)    # move in y,x coordinates (for display and matrix indexing)

            # checks for move validity
            if not isinstance(move_x, int) or not isinstance(move_y, int):
                print(f'ILLEGAL MOVE! x, y are {type(move_x)}, {type(move_y)} but should be integer!')
                move_x = move_y = -1  # -1 is my code for type error
                #illegal_count[current_player] += 1

            
            if self.state.is_legal_move(move_xy):   
                print('Player %s move %d,%d accepted.' % (current_player, move_x, move_y))

                # prints the board with a highlight on the move before flipping the pieces
                self.display_board(move=move_yx)

                time.sleep(.5)  # waits a time for board visualization

                # saves move in history
                self.history_file.write('%d,%d,%s\n' % (move_x, move_y, current_player))
                self.history.append((move_xy, current_player))
            
                self.last_player = current_player           # records the player that just moved
                self.state = self.state.next_state(move_xy)    # processes the move
                
                self.display_board(move=move_yx, flipped=True)  #TODO highlight flipped positions before flipping
            
            else:  # illegal move
                print(f'Player {current_player} move {move_xy}_ILLEGAL!')
                illegal_count[current_player] += 1

            elapsed = time.time() - start  # calculates time spend to process this move
            if self.pace - elapsed > 0:
                time.sleep(self.pace - elapsed)

            ansi_interface.clear("eos")  # clears the remainder of the screen
            ansi_interface.cursor_home()  # resets cursor to print all over

    def write_output(self):
        """
        Writes a xml file with detailed match data
        :return:
        """
        os.chdir(self.basedir)

        root = ET.Element('othello-match')

        colors = [Board.BLACK, Board.WHITE]
        self.player_dirs['None'] = '?'  # trick for writing a draw match

        timing = ET.SubElement(root, 'timing')
        timing.set('start', time.asctime(self.start))
        timing.set('finish', time.asctime(self.finish))

        scores = {
            Board.BLACK: self.state.board.piece_count[Board.BLACK], 
            Board.WHITE: self.state.board.piece_count[Board.WHITE]
        }

        for color in colors:
            elem = ET.SubElement(root, 'player')
            elem.set('directory', self.player_dirs[color])
            elem.set('color', color)
            opp_color = Board.WHITE if color == Board.BLACK else Board.BLACK
            result = 'win' if scores[color] > scores[opp_color] else 'loss' if scores[color] < scores[opp_color] else 'draw'
            elem.set('result', result)
            elem.set('score', str(scores[color]))

        moves = ET.SubElement(root, 'moves')

        for coords, color in self.history:
            move = ET.SubElement(moves, 'move')
            move.set('coord', '%d,%d' % coords)
            move.set('color', color)

        # pretty xml thanks to: https://stackoverflow.com/a/1206856/1251716
        ugly_xml = ET.tostring(root).decode('utf-8')
        dom = xml.dom.minidom.parseString(ugly_xml)  # or xml.dom.minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml()
        f = open(self.output_file, 'w')
        f.write(pretty_xml)
        f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Othello server.')
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

    s = Server(p1, p2, args.delay, args.history, args.output, args.pace)
    s.run()
    s.write_output()
