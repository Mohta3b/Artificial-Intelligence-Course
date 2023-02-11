from select import select
from symbol import dotted_as_name
import turtle
import math
import random
import time
from sys import argv
from colorama import Fore , Back , Style

class Sim:
    # Set true for graphical interface
    GUI = False
    screen = None
    selection = []
    turn = ''
    dots = []
    red = []
    blue = []
    available_moves = []
    minimax_depth = 0
    prune = False

    def __init__(self, minimax_depth, prune, gui):
        self.GUI = gui
        self.prune = prune
        self.minimax_depth = minimax_depth
        if self.GUI:
            self.setup_screen()

    def setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 800)
        self.screen.title("Game of SIM")
        self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
        self.screen.tracer(0, 0)
        turtle.hideturtle()

    def draw_dot(self, x, y, color):
        turtle.up()
        turtle.goto(x, y)
        turtle.color(color)
        turtle.dot(15)

    def gen_dots(self):
        r = []
        for angle in range(0, 360, 60):
            r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
        return r

    def initialize(self):
        self.selection = []
        self.available_moves = []
        for i in range(0, 6):
            for j in range(i, 6):
                if i != j:
                    self.available_moves.append((i, j))
        if random.randint(0, 2) == 1:
            self.turn = 'red'
        else:
            self.turn = 'blue'
        self.dots = self.gen_dots()
        self.red = []
        self.blue = []
        if self.GUI: turtle.clear()
        self.draw()

    def draw_line(self, p1, p2, color):
        turtle.up()
        turtle.pensize(3)
        turtle.goto(p1)
        turtle.down()
        turtle.color(color)
        turtle.goto(p2)

    def draw_board(self):
        for i in range(len(self.dots)):
            if i in self.selection:
                self.draw_dot(self.dots[i][0], self.dots[i][1], self.turn)
            else:
                self.draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

    def draw(self):
        if not self.GUI: return 0
        self.draw_board()
        for i in range(len(self.red)):
            self.draw_line((math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
                           (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
                           'red')
        for i in range(len(self.blue)):
            self.draw_line((math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
                           (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
                           'blue')
        self.screen.update()
        time.sleep(1)
    
    def count_almost_triangle_lines(self,red,blue):
        red_degree=[0 for _ in range(6)]
        for reds in red:
            red_degree[reds[0]]+=1
            red_degree[reds[1]]+=1
        blue_degress=[0 for _ in range(6)]
        for blues in blue:
            blue_degress[blues[0]]+=1
            blue_degress[blues[1]]+=1

        return sum(red_degree),sum(blue_degress)

    def _evaluate(self,red,blue):
        #TODO
        almost_red_triangle,almost_blue_triangle = self.count_almost_triangle_lines(red,blue)
        return almost_blue_triangle-almost_red_triangle

    def minimax(self, depth, player_turn):
        #TODO

        def max_value(depth:int,red_moves:list,blue_moves:list,available_moves:list,alpha=float('-inf'),beta=float('inf')):
            if self.gameover(red_moves, blue_moves) == 'blue':
                return [float('-inf'), None]

            elif self.gameover(red_moves, blue_moves) == 'red':
                return [float('inf'), None]

            if depth == 0:
                return [self._evaluate(red_moves,blue_moves), None]

            v= [float('-inf'), None]

            for move in available_moves:
                available_moves.remove(move)
                red_moves.append(move)
                new_path = min_value(depth-1,red_moves,blue_moves,available_moves,alpha=alpha,beta=beta)
                available_moves.append(move)
                red_moves.remove(move)
                
                if new_path[0]>= v[0]:
                    v[0]=new_path[0]
                    v[1]=move
                    alpha = max(alpha, v[0])
                    if self.prune:
                        if v[0] >= beta:
                            break
            return v

        
        def min_value(depth:int,red_moves:list,blue_moves:list,available_moves:list,alpha=float('-inf'),beta=float('inf')):
            if self.gameover(red_moves, blue_moves) == 'blue':
                return [float('-inf'), None]

            elif self.gameover(red_moves, blue_moves) == 'red':
                return [float('inf'), None]

            if depth == 0 or not available_moves:
                return [self._evaluate(red_moves,blue_moves), None]

            v= [float('inf'), None]

            for move in available_moves:
                available_moves.remove(move)
                blue_moves.append(move)
                new_path = max_value(depth-1,red_moves,blue_moves,available_moves,alpha=alpha,beta=beta)
                available_moves.append(move)
                blue_moves.remove(move)
                
                if new_path[0]<= v[0]:
                    v[0]=new_path[0]
                    v[1]=move
                    beta = min(beta, v[0])
                    if self.prune:
                        if v[0] <= alpha:
                            break
            return v

        if player_turn=='red':
            return(max_value(depth=depth,red_moves=self.red,blue_moves=self.blue,available_moves=self.available_moves)[1])
        else:
            return(min_value(depth=depth,red_moves=self.red,blue_moves=self.blue,available_moves=self.available_moves)[1])

        
    def enemy(self):
        return random.choice(self.available_moves)


    def _swap_turn(self,turn):
        if turn == 'red':
            return 'blue'
        else:
            return 'red'


    def play(self):
        self.initialize()
        while True:
            if self.turn == 'red':
                selection = self.minimax(depth=self.minimax_depth, player_turn=self.turn)
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            else:
                selection = self.enemy()
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            if selection in self.red or selection in self.blue:
                raise Exception("Duplicate Move!!!")
            if self.turn == 'red':
                self.red.append(selection)
            else:
                self.blue.append(selection)

            self.available_moves.remove(selection)
            self.turn = self._swap_turn(self.turn)
            selection = []
            self.draw()
            r = self.gameover(self.red, self.blue)
            if r != 0:
                return r

    def gameover(self, r, b):
        if len(r) < 3:
            return 0
        r.sort()
        for i in range(len(r) - 2):
            for j in range(i + 1, len(r) - 1):
                for k in range(j + 1, len(r)):
                    if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                        return 'blue'
        if len(b) < 3: return 0
        b.sort()
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                        return 'red'
        return 0


if __name__=="__main__":

    game = Sim(minimax_depth=int(argv[1]), prune=True, gui=bool(int(argv[2])))

    results = [0, 0]
    start_time=time.time()
    n=100
    for i in range(n):
        print(i)
        if game.play()=='red':
            results[0] += 1
        else:
            results[1]+=1
    end_time=time.time()
    average_time = (end_time - start_time)/n
    print(Fore.CYAN+ "depth=",argv[1])
    print(Fore.RED+"red:",results[0],Fore.BLUE + "blue:",results[1])
    print(Fore.GREEN+"average time=",average_time)
    print(Style.RESET_ALL)
    