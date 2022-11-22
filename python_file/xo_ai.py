

from dis import dis
from subprocess import call


board = ['-']*9
# print(board)


def check_win(board,player):
    pattern = [
        [0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]
    ]
    for item in pattern:
        #print(item,board)
        if board[item[0]] == player and board[item[1]] == player and board[item[2]] == player:
            return True
    return False

def display(board):
    n = 0
    for row in range(3):
        for col in range(3):
            print(board[n], end=' ')
            n+=1
        print()

def user_input(board,player):
    index = int(input('please your turn:'))
    board[index-1] = player

if __name__ == '__main__':
    player_name = ['X','O']
    turn = 0
    while(True):
        display(board)
        user_input(board,player_name[turn])
        if(check_win(board,player_name[0])):
            display(board)
            print('player x win ')
            break
        elif(check_win(board,player_name[1])):
            display(board)
            print('player O win ')
            break
        elif not '-' in board:
            display(board)
            print('tie')
            break
        turn = 1 if turn == 0 else 0