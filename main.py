import pygame, sys

pygame.init()

WIDTH, HEIGHT = 900, 900

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Trash Toe! By Brant Barton")
# sound effects
winner_sound = pygame.mixer.Sound("assets/like.mp3")
draw_sound = pygame.mixer.Sound("assets/dislike.mp3")

BOARDIMG = pygame.image.load("assets/Board.png")
# x and o images to play
original_x_img = pygame.image.load("assets/raccoon.png")
original_o_img = pygame.image.load("assets/opossum.png")

# fix aspect ratio of images resolution and resizing of images
new_width_x = int(original_x_img.get_width() * (200 / original_x_img.get_height()))
new_width_o = int(original_o_img.get_width() * (200 / original_o_img.get_height()))
X_IMG = pygame.transform.scale(original_x_img, (new_width_x, 200))
O_IMG = pygame.transform.scale(original_o_img, (new_width_o, 200))

BG_COLOR = (81,154,253)

board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
graphical_board = [[[None, None], [None, None], [None, None]], 
                   [[None, None], [None, None], [None, None]], 
                   [[None, None], [None, None], [None, None]]]
# when it is X turn
to_move = 'X'
# testing****** to draw a grid, went with image instead
# def draw_grid():
#     for i in range(1, 3):
#         pygame.draw.line(SCREEN, (0, 0, 0), (i * 300, 0), (i * 300, HEIGHT), 5)
#         pygame.draw.line(SCREEN, (0, 0, 0), (0, i * 300), (WIDTH, i * 300), 5)

def render_board(board, ximg, oimg):
    global graphical_board
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                graphical_board[i][j][0] = ximg
                graphical_board[i][j][1] = ximg.get_rect(center=(j*300+150, i*300+150))
            elif board[i][j] == 'O':
                graphical_board[i][j][0] = oimg
                graphical_board[i][j][1] = oimg.get_rect(center=(j*300+150, i*300+150))

def add_XO(board, graphical_board, to_move):
    current_pos = pygame.mouse.get_pos()
    converted_x = current_pos[0] // 300
    converted_y = current_pos[1] // 300
    if board[converted_y][converted_x] != 'O' and board[converted_y][converted_x] != 'X':
        board[converted_y][converted_x] = to_move
        to_move = 'O' if to_move == 'X' else 'X'
    
    render_board(board, X_IMG, O_IMG)

    for i in range(3):
        for j in range(3):
            if graphical_board[i][j][0] is not None:
                SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
    
    return board, to_move

game_finished = False

def determine_winner(symbol):
    return "raccoon" if symbol == 'X' else "opossum"

# clear cells function to start a new game 
def clear_cells(cells):
    for cell in cells:
        i, j = cell
        rect = pygame.Rect(j*300 + 50, i*300 + 50, 200, 200)
        pygame.draw.rect(SCREEN, BG_COLOR, rect)
        
# Logic for placing and a win
def check_win(board):
    winner = None
    winning_cells = []

    for row in range(0, 3):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            winner = determine_winner(board[row][0])
            winning_cells = [(row, 0), (row, 1), (row, 2)]
            break

    for col in range(0, 3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            winner = determine_winner(board[0][col])
            winning_cells = [(0, col), (1, col), (2, col)]
            break

    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        winner = determine_winner(board[0][0])
        winning_cells = [(0, 0), (1, 1), (2, 2)]

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        winner = determine_winner(board[0][2])
        winning_cells = [(0, 2), (1, 1), (2, 0)]

    if winner:
        image_filename = f"assets/win-{winner}.png"
        win_image = pygame.image.load(image_filename)
        win_image = pygame.transform.scale(win_image, (200, 200))

        clear_cells(winning_cells)

        for cell in winning_cells:
            i, j = cell
            graphical_board[i][j][0] = win_image
            graphical_board[i][j][1] = win_image.get_rect(center=(j*300+150, i*300+150))
            SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
        
        pygame.display.update()
        # test to get the winner
        # print("winner")
        winner_sound.play()
        return winner

    if winner is None:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    return None
        # test to get the draw
        # print("draw")
        draw_sound.play()
        return "DRAW"

# drawing my basic title screen with start button
def draw_title_screen():
    SCREEN.fill(BG_COLOR)
    font = pygame.font.Font(None, 74)
    title_text = font.render("Welcome to Tic Trash Toe!", True, (0, 0, 0))
    SCREEN.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4))
# button here
    button_font = pygame.font.Font(None, 50)
    button_text = button_font.render("Let it Begin", True, (255, 255, 255))
    button_rect = pygame.Rect(WIDTH//2 - button_text.get_width()//2 - 10, HEIGHT//2 - button_text.get_height()//2 - 10, button_text.get_width() + 20, button_text.get_height() + 20)
    pygame.draw.rect(SCREEN, (0, 0, 0), button_rect)
    SCREEN.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

    return button_rect

state = "title"
# start of game (while loop to keep window open until triggered to close)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if state == "title":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    state = "game"
                    SCREEN.fill(BG_COLOR)
                    SCREEN.blit(BOARDIMG, (64, 64))
                    # draw_grid()
                    pygame.display.update()
        elif state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN:
                board, to_move = add_XO(board, graphical_board, to_move)

                if game_finished:
                    board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
                    graphical_board = [[[None, None], [None, None], [None, None]], 
                                       [[None, None], [None, None], [None, None]], 
                                       [[None, None], [None, None], [None, None]]]

                    to_move = 'X'

                    SCREEN.fill(BG_COLOR)
                    SCREEN.blit(BOARDIMG, (64, 64))
                    # draw_grid()

                    game_finished = False

                    pygame.display.update()
                
                if check_win(board) is not None:
                    game_finished = True
                
                pygame.display.update()
# starting screen
    if state == "title":
        button_rect = draw_title_screen()
        pygame.display.update()
