import pygame
import ML
import random

pygame.init()
screen = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()


class TictactoeField:
    def __init__(self, pos, size_pixel, size):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.board_line = [0] * (size ** 2)
        self.pos = pos
        self.size_pixel = size_pixel
        self.player = 1
        self.done = False

    def restart(self):
        self.board = [[0] * self.size for _ in range(self.size)]
        self.board_line = [0] * (self.size ** 2)
        self.player = 1
        self.done = False

    def generate_move(self, Ai):
        # if self.done:
        #     return
        if self.player == 1:
            for i in range(self.size ** 2):
                self.board_line[i] = -self.board_line[i]
            ans = Ai.play(self.board_line)
            for i in range(self.size ** 2):
                self.board_line[i] = -self.board_line[i]
        else:
            ans = Ai.play(self.board_line)
        if self.board_line[ans] != 0:
            self.done = True
            return (self.player % 2) + 1, ans
        self.board[ans // self.size][ans % self.size] = self.player
        self.board_line[ans] = (self.player - 1.5) * 2
        self.player = (self.player % 2) + 1

        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 0:
                    continue

                if self.size - x >= 3:
                    if self.board[x][y] == self.board[x + 1][y] == self.board[x + 2][y]:
                        self.done = True
                        return self.board[x][y], -1
                if self.size - y >= 3:
                    if self.board[x][y] == self.board[x][y + 1] == self.board[x][y + 2]:
                        self.done = True
                        return self.board[x][y], -1
                if self.size - y >= 3 and self.size - x >= 3:
                    if self.board[x][y] == self.board[x + 1][y + 1] == self.board[x + 2][y + 2]:
                        self.done = True
                        return self.board[x][y], -1
                if self.size - y >= 3 and x >= 2:
                    if self.board[x][y] == self.board[x - 1][y + 1] == self.board[x - 2][y + 2]:
                        self.done = True
                        return self.board[x][y], -1

    def click(self, x, y):
        if self.done:
            return
        if self.pos[0] <= x <= self.pos[0] + self.size_pixel and self.pos[1] <= y <= self.pos[1] + self.size_pixel:
            x, y = x - self.pos[0], y - self.pos[1]
            x, y = x * self.size // self.size_pixel, y * self.size // self.size_pixel
            if self.board[x][y] != 0:
                return None
            self.board[x][y] = self.player
            self.board_line[x * self.size + y] = (self.player - 1.5) * 2
            self.player = (self.player % 2) + 1
            for x in range(self.size):
                for y in range(self.size):
                    if self.size - x >= 3:
                        if self.board[x][y] == self.board[x + 1][y] == self.board[x + 2][y] and self.board[x][y] != 0:
                            self.done = True
                            return self.board[x][y]
                    if self.size - y >= 3:
                        if self.board[x][y] == self.board[x][y + 1] == self.board[x][y + 2] and self.board[x][y] != 0:
                            self.done = True
                            return self.board[x][y]
                    if self.size - y >= 3 and self.size - x >= 3:
                        if self.board[x][y] == self.board[x + 1][y + 1] == self.board[x + 2][y + 2] and self.board[x][
                            y] != 0:
                            self.done = True
                            return self.board[x][y]
                    if self.size - y >= 3 and x >= 2:
                        if self.board[x][y] == self.board[x - 1][y + 1] == self.board[x - 2][y + 2] and self.board[x][
                            y] != 0:
                            self.done = True
                            return self.board[x][y]

    def draw(self):
        for col in range(self.size):
            for row in range(self.size):
                if self.board[row][col] == 1:
                    pygame.draw.rect(screen, (255, 0, 0), (self.pos[0] + self.size_pixel / self.size * row,
                                                           self.pos[1] + self.size_pixel / self.size * col,
                                                           self.size_pixel / self.size, self.size_pixel / self.size))
                if self.board[row][col] == 2:
                    pygame.draw.rect(screen, (0, 0, 255), (self.pos[0] + self.size_pixel / self.size * row,
                                                           self.pos[1] + self.size_pixel / self.size * col,
                                                           self.size_pixel / self.size, self.size_pixel / self.size))
        for row in range(self.size + 1):
            pygame.draw.line(screen, (0, 0, 0), (self.pos[0], self.pos[1] + row * self.size_pixel / self.size),
                             (self.pos[0] + self.size_pixel, self.pos[1] + row * self.size_pixel / self.size))
            pygame.draw.line(screen, (0, 0, 0), (self.pos[0] + row * self.size_pixel / self.size, self.pos[1]),
                             (self.pos[0] + row * self.size_pixel / self.size, self.pos[1] + self.size_pixel))


readInit = True
evolve = False
field = TictactoeField((50, 50), 600, 3)
num_of_ai = 100
rounds = 1
learning_rate = 0.4
layers = 2
neurons = 54
num_best = 15


def new_generation(Ai, num_of_ai):
    ans = list(Ai)
    for i in range(len(Ai), num_of_ai):
        j = random.randint(0, len(Ai) - 1)
        k = random.randint(0, len(Ai) - 1)
        ans.append(Ai[j].mutate(learning_rate, Ai[k]))
    return ans


if readInit:
    Ai = []
    with open('ML_saves.txt', 'r') as f:
        for _ in range(4):
            ai = f.readline()
            net = ai.split(']]], [[[')
            for i in range(len(net)):
                net[i] = net[i].split(']], [[')
            for i in range(len(net)):
                for ii in range(len(net[i])):
                    net[i][ii] = net[i][ii].split("], [")
            for i in range(len(net)):
                for ii in range(len(net[i])):
                    for iii in range(len(net[i][ii])):
                        net[i][ii][iii] = list(map(float, net[i][ii][iii].split(", ")))
            Ai.append(ML.AI(9, neurons, layers, net))
    Ai = new_generation(Ai, num_of_ai)
else:
    Ai = [ML.AI(9, neurons, layers) for _ in range(num_of_ai)]

generation = 1
while True:
    with open('ML_saves.txt', 'w') as f:
        for ai in Ai[:4]:
            f.write(str(ai.net)[4:-4] + "\n")

    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                ans = field.click(mouse_pos[0], mouse_pos[1])
                # while ans == None:
                #     ans=field.click(1, 1)
                #     print(ans)
                #     if ans!=None:
                #         field.restart()
            if event.button == 3:
                field.generate_move(Ai[0])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                field.restart()
            if event.key == pygame.K_e:
                evolve = not evolve
    if evolve:
        winns = [[i, 0, 0, 0] for i in range(num_of_ai)]
        finished = 0
        draws = 0
        for i in range(num_of_ai):
            for j in range(num_of_ai):
                if i == j:
                    continue
                for _ in range(rounds):
                    ans = None
                    ai = [i, j]
                    index = 0
                    field.restart()
                    while ans is None:
                        ans = field.generate_move(Ai[ai[index % 2]])
                        index += 1
                    if index < 9:
                        winns[ai[index % 2]][1] += 1
                        if ans[1] != -1:
                            winns[ai[(index + 1) % 2]][1] -= 2
                            winns[ai[(index + 1) % 2]][3] -= 1
                        else:
                            winns[ai[(index + 1) % 2]][1] += 1
                            winns[ai[(index + 1) % 2]][2] += 1
                            finished += 1
                    else:
                        draws += 1

        winns.sort(key=lambda x: -x[1])

        best = winns[:num_best]
        bestAi = [Ai[best[i][0]] for i in range(len(best))]
        Ai = new_generation(bestAi, num_of_ai)
        print(generation, best)
        print("Finished:", finished, "Draws:", draws)
        generation += 1
    field.draw()
    pygame.display.update()
