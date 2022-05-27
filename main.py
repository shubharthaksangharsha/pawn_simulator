#By Shubharthak Sangharasha,
from typing import List, Tuple
import sys

class Board:
    '''Board class that contains board-blueprint'''
    def __init__(self, row = 8, col = 8) -> None:
        '''
        initialize the board by 8x8 square matrix using list
        input: row: int, col: int
        output: None
        '''      
        self.board = []
        for i in range(row):
            temp = []
            for j in range(col):
                temp.append(0)
            self.board.append(temp)
        self.place_counter, self.counter, self.cur_pos, self.pawn_pos, self.prev_pos = 0, 0, (-1, -1, ""), (-1, -1, "", ""), (-1, -1, "")
        
    def place_translate(self, x, y, f) -> Tuple:
        '''
        return a tuple (X,Y, f) if move is valid else return (-1, -1, f)
        input: x: int, y: int
        output: Tuple
        '''
        if x > 7 or y > 7 or x < 0 and y < 0:
            return -1, -1, f
        X, Y = 7 - y, x
        return X,Y,f,


        
    def place(self, X: int, Y: int, F: str, C: str) -> None:
        '''
        place the pawn in the board if valid move else do nothing
        input: X: int, Y: int, F: str, C: str
        '''
        if self.place_counter > 0:
            return
        self.pawn_pos, self.cur_pos = (X, Y, F, C), self.place_translate(X,Y,F)
        self.prev_pos = self.cur_pos
        if self.cur_pos !=  (-1, -1, F):
            self.board[self.cur_pos[0]][self.cur_pos[1]] = self.pawn_pos
            
    def move_translate(self, X: int, pawn_pos: Tuple) -> Tuple:
        '''
        Return a tuple with pawn x,y pos if valid move else return (-1, -1, pawn_pos)
        input: X: int, pawn_pos: Tuple
        output: Tuple
        '''
        x, y = pawn_pos[0], pawn_pos[1]
#        print(x, y, pawn_pos[2])
        if pawn_pos[2] == "East":
            x = x + X
        if pawn_pos[2] == "South":
            y = y - X
        if pawn_pos[2] == "North":
            y = y + X
        if pawn_pos[2] == "West":
            x = x - X
#        print(x, y)
        if x > 7 or y > 7 or x < 0 or y < 0:
            return -1, -1, pawn_pos[2]
        X, Y = 7 - y, x
#        print(X, Y)
        self.counter += 1
        return X,Y,pawn_pos[2], x, y,


    def move(self, x: int) -> None:
        '''
        move the pawn if it's a valid move
        input: x: int
        output: None
        '''
        if x > 2 or x <= 0:
            print("Invalid Move")
        elif self.counter != 0 and x > 1:
            print("Invalid Move")
        else:
#            print(x)
            temp = self.move_translate(x, self.pawn_pos)
            self.prev_pos, self.cur_pos = self.cur_pos, temp[0:3]
 #           print(self.cur_pos)
            if self.cur_pos != (-1, -1, self.cur_pos[2]):
                self.temp_pawn = (temp[3], temp[4], self.pawn_pos[2], self.pawn_pos[3])
                self.board[self.prev_pos[0]][self.prev_pos[1]] = 0
                self.pawn_pos = self.temp_pawn
                self.board[self.cur_pos[0]][self.cur_pos[1]] = self.pawn_pos
            
            
    def left(self) -> None:
        '''
        rotate the pawn to 90 degree left of current face
        input: None
        output: None
        '''
        x, y, f, c = self.pawn_pos
        if f == "East":
            f = "North"
        elif f == "North":
            f = "West"
        elif f == "South":
            f = "East"
        else:
            f = "South"
        self.pawn_pos = (x, y, f, c)
        
    def right(self):
        '''
        rotate the pawn to 90 degree right of current face
        input: None
        output: None
        '''
        x, y, f, c = self.pawn_pos
        if f == "East":
            f = "South"
        elif f == "North":
            f = "East"
        elif f == "South":
            f = "West"
        else:
            f = "North"
        self.pawn_pos = (x, y, f, c)
   
    def report(self) -> Tuple:
        '''
        return the tuple of current pawn position, state, color 
        '''
        return self.pawn_pos    
        
def take_input(filename: str) -> List[tuple]:
    '''
    read input from the file of the pawn simulator and return the input list
    input: filename: str
    output: input_list: List[tuple]
    '''
    input_list = []
    with open (filename, "r") as f:
        for line in f.readlines():
            input_list.append(tuple(line.split()))
#    print(input_list)
    return input_list

def execute_input(input_list: List[str], myboard: Board) -> None:
    '''
    execute the input_file provided for the pawn simulator
    input: input_list: List[str], myboard: Board
    output: None
    '''
    for input in input_list:
        if 'place' in  input[0] or 'Place' in input[0] or 'PLACE' in input[0]:
            _, X, Y, F, C  = input
            myboard.place(int(X), int(Y), F, C)
        if 'move' in input[0] or 'MOVE' in input[0]:
            if len(input) == 1:
                input = ('MOVE', 1)
            _, x = input
            myboard.move(int(x))
        if 'left' in input or 'LEFT' in input:
            myboard.left()
        if 'right' in input or 'RIGHT' in input:
            myboard.right()
        if 'report' in input or 'REPORT' in input:
            print(myboard.report())      
  

#Driver Code
if __name__ == '__main__':
    myboard = Board()
    if len(sys.argv[1:]) != 0:
        input_list = take_input(sys.argv[1])
    else:
        file_input = input("Enter the name of the input file [file should be present in current working directory]: ")
        input_list = take_input(file_input)
    execute_input(input_list, myboard)
