import pygame
import sys
import random
import heapq

class PacmanGame:
    def __init__(self, field):
        pygame.init()

        self.colors = {
            '#': (0, 0, 255),      # Blue for walls
            '$': (255, 255, 255),  # White for coins
            'G': (255, 0, 0),      # Red for ghosts
            'P': (255, 255, 0),    # Yellow for Pacman
            '.': (0, 0, 0)         # Black for empty cells
        }

        self.field = [list(row) for row in field]
        self.width = len(self.field[0])
        self.height = len(self.field)
        self.pacman = None
        self.ghosts = []
        self.coins = 0
        self.total_coins = 0
        self.moves = {'W': (0, -1), 'A': (-1, 0), 'S': (0, 1), 'D': (1, 0)}  # Up, Left, Down, Right

        self.initialize_game()

        self.tile_size = 30
        self.screen = pygame.display.set_mode((self.width * self.tile_size, self.height * self.tile_size))
        pygame.display.set_caption("Pacman Game")

        self.pacman_turn = True  # True if it's Pacman's turn, False if it's the ghosts' turn

    def initialize_game(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.field[y][x] == 'P':
                    self.pacman = (x, y)
                elif self.field[y][x] == 'G':
                    self.ghosts.append((x, y))
                elif self.field[y][x] == '$':
                    self.coins += 1
                    self.total_coins += 1
                
    def print_game(self):
        for y in range(self.height):
            for x in range(self.width):
                color = self.colors.get(self.field[y][x], (0, 0, 0))
                pygame.draw.rect(self.screen, color, (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))

        pygame.display.flip()

    def move_entity(self, entity, direction):
        dx, dy = self.moves[direction]
        new_x, new_y = entity[0] + dx, entity[1] + dy

        if 0 <= new_x < self.width and 0 <= new_y < self.height and self.field[new_y][new_x] != '#':
            return new_x, new_y
        else:
            return entity

    def move_pacman(self, direction):
        if self.pacman_turn and direction in self.moves:
            new_pacman = self.move_entity(self.pacman, direction)
            if new_pacman != self.pacman:
                self.field[self.pacman[1]][self.pacman[0]] = '.'
                self.pacman = new_pacman
                self.field[self.pacman[1]][self.pacman[0]] = 'P'
                self.pacman_turn = False  # Switch to the ghosts' turn

    def move_ghosts(self, algorithm='AStar'):
        if not self.pacman_turn:
            for i, ghost in enumerate(self.ghosts):
                if algorithm == 'AStar':
                    next_move = self.astar(ghost, self.pacman)
                elif algorithm == 'DFS':
                    next_move = self.dfs(ghost, self.pacman)
                if next_move:
                    self.field[ghost[1]][ghost[0]] = '.'
                    self.ghosts[i] = next_move
                    self.field[next_move[1]][next_move[0]] = 'G'
            self.check_collision()
            self.pacman_turn = True  # Switch back to Pacman's turn

    def dfs(self, start, target):
        stack = [(start, [])]
        visited = set()

        while stack:
            current, path = stack.pop()
            if current == target:
                return path[0] if path else start

            visited.add(current)
            for move in self.moves.values():
                neighbor = (current[0] + move[0], current[1] + move[1])
                if (
                    0 <= neighbor[0] < self.width
                    and 0 <= neighbor[1] < self.height
                    and neighbor not in visited
                    and self.field[neighbor[1]][neighbor[0]] != '#'
                ):
                    stack.append((neighbor, path + [neighbor]))

        return start

    def astar(self, start, target):
        heap = [(0, start, [])]
        visited = set()

        while heap:
            cost, current, path = heapq.heappop(heap)
            if current == target:
                return path[0] if path else start

            visited.add(current)
            for move in self.moves.values():
                neighbor = (current[0] + move[0], current[1] + move[1])
                if (
                    0 <= neighbor[0] < self.width
                    and 0 <= neighbor[1] < self.height
                    and neighbor not in visited
                    and self.field[neighbor[1]][neighbor[0]] != '#'
                ):
                    heapq.heappush(heap, (self.manhattan_distance(neighbor, target), neighbor, path + [neighbor]))

        return start

    def manhattan_distance(self, point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def check_collision(self):
        if self.pacman in self.ghosts:
            print("Game Over! Pacman was caught by a ghost.")
            pygame.quit()
            sys.exit()
        elif self.field[self.pacman[1]][self.pacman[0]] == '$':
            print("Pacman collected a coin!")
            self.coins -= 1
            if self.coins <= 0:
                print("You Win! Pacman collected all coins and won!")
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    pacman_game = PacmanGame([
        "####################################################",
        "#  #$                        #     #         G#   $#",
        "#  #                    ######     #   ########    #",
        "#              P                                   #",
        "#                                                  #",
        "#                                                  #",
        "#                                    #             #",
        "# #  # #  G                          #             #",
        "# #  # #                             #             #",
        "#$#### #                             #             #",
        "#      #                             ####          #",
        "# ####                                             #",
        "# #  # #                         G                 #",
        "####################################################"
    ])
    pacman_game.initialize_game()

    clock = pygame.time.Clock()  # Create a clock object to control the frame rate

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pacman_game.print_game()
        move_input = pygame.key.get_pressed()
        if move_input[pygame.K_w]:
            pacman_game.move_pacman('W')
        elif move_input[pygame.K_a]:
            pacman_game.move_pacman('A')
        elif move_input[pygame.K_s]:
            pacman_game.move_pacman('S')
        elif move_input[pygame.K_d]:
            pacman_game.move_pacman('D')

        pacman_game.move_ghosts(algorithm='AStar')

        clock.tick(5)  # Set the frame rate to 1 move per second (adjust as needed)
