import pygame
import sys
import time

import logic.Yoshis_Zones as yz

GREEN = (0, 255, 0)
RED = (254, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

size = width, height = 800, 800

yz_game = yz

# colors
black = (0, 0, 0)
white = (255, 255, 255)
tile_size = 80

# fonts
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

screen = pygame.display.set_mode(size)

board = yz_game.initial_state()

user = None

depth = 2

ai_turn = True


def load_image(path):
    try:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (tile_size, tile_size))
        return image
    except Exception as e:
        print(f"could not load image, error: {e}")
        return None


def draw_button(text, left, top, width, height):
    button = pygame.Rect(left, top, width, height)
    playX = mediumFont.render(text, True, white)
    playXRect = playX.get_rect()
    playXRect.center = button.center
    pygame.draw.rect(screen, black, button)
    screen.blit(playX, playXRect)

    return button


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(white)

    if user is None:

        # Draw title
        title = largeFont.render("Play Yoshi's Zones", True, black)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw title
        title = largeFont.render(
            "Please choose the dificult level to start:", True, black
        )
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), (height / 2) - 100)
        screen.blit(title, titleRect)

        begginer_button = draw_button(
            "Begginer",
            ((width / 2) - (width / 4) / 2),
            ((height / 2) - 50 / 2),
            width / 4,
            50,
        )

        medium_button = draw_button(
            "Medium",
            ((width / 2) - (width / 4) / 2),
            ((height / 2) - 50 / 2) + 100,
            width / 4,
            50,
        )

        hard_button = draw_button(
            "Hard",
            ((width / 2) - (width / 4) / 2),
            ((height / 2) - 50 / 2) + 200,
            width / 4,
            50,
        )

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if begginer_button.collidepoint(mouse):
                time.sleep(0.2)
                user = "ym"
                depth = 2
            elif medium_button.collidepoint(mouse):
                time.sleep(0.2)
                user = "ym"
                depth = 3
            elif hard_button.collidepoint(mouse):
                time.sleep(0.2)
                user = "ym"
                depth = 4

    else:

        # load images

        yoshi_green = load_image("images/yoshi_green.png")
        yoshi_red = load_image("images/yoshi_red.jpg")

        # Draw game board

        tile_origin = (
            width / 2 - (8 * tile_size) / 2,
            height / 2 - (8 * tile_size) / 2,
        )

        tiles = []
        for i in range(8):
            row = []
            for j in range(8):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size,
                    tile_size,
                )

                color = WHITE
                if board[i][j] != yz.EMPTY:
                    if board[i][j] == "G":
                        color = GREEN
                    elif board[i][j] == "R":
                        color = RED

                pygame.draw.rect(
                    screen,
                    color,
                    (
                        tile_origin[0] + j * tile_size,
                        tile_origin[1] + i * tile_size,
                        tile_size,
                        tile_size,
                    ),
                )

                if board[i][j] == "ym" and yoshi_green is not None:
                    screen.blit(
                        yoshi_green,
                        (
                            tile_origin[0] + j * tile_size,
                            tile_origin[1] + i * tile_size,
                            tile_size,
                            tile_size,
                        ),
                    )
                if board[i][j] == "yh" and yoshi_red is not None:
                    screen.blit(
                        yoshi_red,
                        (
                            tile_origin[0] + j * tile_size,
                            tile_origin[1] + i * tile_size,
                            tile_size,
                            tile_size,
                        ),
                    )

                if (i, j) in [cell for zone in yz.special_positions for cell in zone]:
                    pygame.draw.rect(screen, black, rect, 6)
                else:
                    pygame.draw.rect(screen, black, rect, 3)

                row.append(rect)
            tiles.append(row)

        game_over = yz_game.terminal(board)

        # show title
        if game_over:
            winner = yz_game.winner(board)

            if winner is None:
                title = f"Game Over: Tie"
            elif winner == "ym":
                title = f"Game Over: Green Yoshi Wins."
            else:
                title = f"Game Over: Red Yoshi Wins."

            # draw again button
            again_button = draw_button(
                "Play Again",
                ((width / 2) - (width / 4) / 2),
                ((height / 2) - 50 / 2),
                width / 4,
                50,
            )

            # chek button again click
            click, _, _ = pygame.mouse.get_pressed()

            if click == 1:
                mouse = pygame.mouse.get_pos()
                if again_button.collidepoint(mouse):
                    time.sleep(0.2)

                    board = yz_game.initial_state()

                    user = None

                    depth = 2

                    ai_turn = True

        elif user == "yh":
            title = f"Play as Red Yoshi."
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, black)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        score = f"Green Yoshi:{yz.WIN_ZONES[0]},Red Yoshi:{yz.WIN_ZONES[1]}"
        score = largeFont.render(score, True, black)
        scoreRect = score.get_rect()
        scoreRect.center = ((width / 2), height - 40)
        screen.blit(score, scoreRect)

        pygame.display.flip()

        # check for user move
        click, _, _ = pygame.mouse.get_pressed()

        if click == 1 and user == "yh" and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(8):
                for j in range(8):
                    if board[i][j] == yz.EMPTY and tiles[i][j].collidepoint(mouse):
                        result = yz_game.result((i, j), board, user)
                        if result is not None:
                            board = result
                            yz.winner(board)
                        user = yz_game.change_player(user)

        # check for AI move
        if user != "yh" and not game_over:

            if ai_turn:
                time.sleep(0.5)
                move = yz_game.minimax(board, depth=depth)
                print(move)
                board = yz_game.result(move, board, "ym")
                ai_turn = False
                user = yz_game.change_player(user)
                yz.winner(board)

            else:
                ai_turn = True

    pygame.display.flip()
