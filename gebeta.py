
import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Define colors to use in the code
BLACK = (0, 0, 0)
WOODEN = (50, 20, 0, 128)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BROWN = (160, 82, 45)
LIGHT_BROWN = (205, 133, 63)
STONE_COLOR = (255, 255, 255)

# Set the window size, W and H
WINDOW_SIZE = (1000, 640)

# Create the game window
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set the title of the window
pygame.display.set_caption("GEBETA_GAME")

# Set the font
font = pygame.font.Font(None, 30)

# Define the board dimensions and position
BOARD_WIDTH = 840
BOARD_HEIGHT = 380


PADDING_X = (WINDOW_SIZE[0] - BOARD_WIDTH) // 2
BOARD_X = PADDING_X if PADDING_X > 0 else 0

BOARD_Y = (WINDOW_SIZE[1] - BOARD_HEIGHT) // 2

# Define the pit dimensions
PIT_WIDTH = BOARD_WIDTH // 7
PIT_HEIGHT = BOARD_HEIGHT // 2

# Define the board layout as array
board = np.array([[4, 4, 4, 4, 4, 4, 0],
                  [4, 4, 4, 4, 4, 4, 0]])

# Define the current player and player's turn
current_player = 0
current_turn = 0

PADDING_X = (WINDOW_SIZE[0] - BOARD_WIDTH) // 4  # Adjust the padding value
# Define the colors for player indicators
PLAYER1_COLOR = (255, 0, 0)  # Red
PLAYER2_COLOR = (0, 0, 255)  # Blue


def draw_board():
    # Draw the board background with wooden texture
    pygame.draw.rect(screen, BROWN, (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), border_radius=30)
    pygame.draw.rect(screen, LIGHT_BROWN, (BOARD_X + 10, BOARD_Y + 10, BOARD_WIDTH - 20, BOARD_HEIGHT - 20),
                     border_radius=20)

    # Draw the player indicator
    player_indicator_x = BOARD_X - 30  # Adjust the position of the player indicator
    player_indicator_y = BOARD_Y + BOARD_HEIGHT // 2 - 10

    if current_player == 0:
        # Draw player 1 indicator as an upward arrow
        pygame.draw.polygon(screen, PLAYER1_COLOR, [(player_indicator_x, player_indicator_y + 20),
                                                    (player_indicator_x + 10, player_indicator_y),
                                                    (player_indicator_x + 20, player_indicator_y + 20)])
    else:
        # Draw player 2 indicator as a downward arrow
        pygame.draw.polygon(screen, PLAYER2_COLOR, [(player_indicator_x, player_indicator_y),
                                                    (player_indicator_x + 10, player_indicator_y + 20),
                                                    (player_indicator_x + 20, player_indicator_y)])

    for i in range(2):
        for j in range(7):
            # Calculate the coordinates for pits and stone stores
            pit_x = BOARD_X + j * PIT_WIDTH
            pit_y = BOARD_Y + i * PIT_HEIGHT
            store_x = BOARD_X + j * PIT_WIDTH  # Calculate the x-coordinate for stone stores

            # Draw the pits as circles
            pygame.draw.circle(screen, BROWN, (int(pit_x + PIT_WIDTH / 2), int(pit_y + PIT_HEIGHT / 2)),
                               int(PIT_WIDTH / 2), 0)
            pygame.draw.circle(screen, WOODEN, (int(pit_x + PIT_WIDTH / 2), int(pit_y + PIT_HEIGHT / 2)),
                               int(PIT_WIDTH / 2) - 10, 0)
            # Draw the stones in the pit as circles
            num_stones = board[i][j]
            if num_stones > 0:
                for k in range(num_stones):
                    stone_x = pit_x + PIT_WIDTH // 2.9 + int((k % 7) - 1) * (PIT_WIDTH // 12)
                    stone_y = pit_y + PIT_HEIGHT // 2.5 + int((k // 7) - 1) * (PIT_HEIGHT // 16)
                    pygame.draw.circle(screen, WHITE, (stone_x, stone_y), PIT_WIDTH // 30)
                    pit_stones = font.render(str(num_stones), True, WHITE)
                pit_rect = pit_stones.get_rect(center=(pit_x + PIT_WIDTH // 2, pit_y + PIT_HEIGHT // 1.1))
                screen.blit(pit_stones, pit_rect)

                # Draw the stone stores
                if j == 7:
                    store_stones = board[i][j]
                    store_text = font.render(str(store_stones), True, WHITE)
                    store_rect = store_text.get_rect(center=(store_x + PIT_WIDTH // 2, pit_y + PIT_HEIGHT // 4))
                    screen.blit(store_text, store_rect)

                # Draw the current player's turn
                player_turn_text = font.render(f"Player {current_player + 1}'s Turn", True, WHITE)
                player_turn_rect = player_turn_text.get_rect(midtop=(WINDOW_SIZE[0] // 2, BOARD_Y - 65))
                screen.blit(player_turn_text, player_turn_rect)

                # Check if the game is over and display the winner message
                if is_game_over():
                    # Get the scores
                    score1 = board[0][6]
                    score2 = board[1][6]

                    # Capture remaining seeds
                    for j in range(6):
                        score1 += board[0][j]
                        board[0][j] = 0
                        score2 += board[1][j]
                        board[1][j] = 0

                    # Display the winner
                    if score1 > score2:
                        text = font.render("Player 1 wins!", True, GREEN)
                    elif score2 > score1:
                        text = font.render("Player 2 wins!", True, GREEN)
                    else:
                        text = font.render("It's a tie!", True, WHITE)

                    # Draw the winner text
                    text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, BOARD_Y - 90))
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                    pygame.time.wait(5000)
                    pygame.quit()
                    exit()





def update_board(selected_pit):
    global board, current_player, current_turn

    # Check if the selected pit is a stone store
    if selected_pit == 6:
        return

    # Get the number of stones in the selected pit
    num_stones = board[current_player][selected_pit]

    # Set the number of stones in the selected pit to zero
    board[current_player][selected_pit] = 0

    # Distribute the stones to the other pits
    i = current_player
    j = selected_pit + 1
    while num_stones > 0:
        if i == current_player and j == 7:
            i = 1 - current_player
            j = 0

        # Check if the stone distribution is within the board boundaries
        if i == current_player:
            if j < 7:
                board[i][j] += 1
                num_stones -= 1
            elif j == 7:
                board[i][j % 7] += 1
                num_stones -= 1
        else:
            board[i][j % 7] += 1
            num_stones -= 1

        j += 1
        if j == 7:
            i = 1 - i
            j = 0

    # Check if the last stone lands in the player's store
    if i == current_player and j - 1 == 6:
        current_turn += 1
    # Check if the last stone lands in an empty pit on the player's side
    elif i == current_player and j - 1 != 6 and board[i][j - 1] == 1:
        opposite_pit = 1 - current_player
        captured_stones = board[opposite_pit][5 - (j - 1)]
        board[current_player][j - 1] = 0
        board[current_player][6] += captured_stones + 1
        board[opposite_pit][5 - (j - 1)] = 0
        current_turn += 1
    else:
        current_turn += 1

    # Check if the game is over
    if is_game_over():
        draw_board()  # Display the final board state
        pygame.display.flip()
        pygame.time.wait(6000)
        pygame.quit()
        exit()

    # Switch to the next player
    if i != current_player:
        current_player = 1 - current_player


def is_game_over():
    if np.sum(board[0, :6]) == 0 or np.sum(board[1, :6]) == 0:
        return True
    return False


# Define the main game loop
running = True
selected_pit = None


while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Get the position of the mouse click
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]

            # Check if the mouse click is within the board area
            if BOARD_X <= x <= BOARD_X + BOARD_WIDTH and BOARD_Y <= y <= BOARD_Y + BOARD_HEIGHT:
                # Calculate the selected pit
                selected_pit = (x - BOARD_X) // PIT_WIDTH

                # Check if it is the current player's pit
                if current_player == 0 and y <= BOARD_Y + PIT_HEIGHT or current_player == 1 and y >= BOARD_Y + PIT_HEIGHT:
                    if selected_pit == 6:
                        continue  # Skip if stone store is clicked
                    update_board(selected_pit)

        elif event.type == pygame.MOUSEMOTION:
            pass

    # Clear the screen
    screen.fill(BLACK)

    # Draw the board
    draw_board()

    # Update the display
    pygame.display.flip()
# Quit the game
pygame.quit()
