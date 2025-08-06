import pygame

pygame.init()
screen = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()


class TictactoeFild():
    def __init__(self, pos, size_pixel, size):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.pos = pos
        self.size_pixel = size_pixel
        self.player = 1

    def restart(self):
        self.board = [[0] * self.size for _ in range(self.size)]
        self.player = 1

    def click(self, x, y):
        if self.pos[0] <= x <= self.pos[0] + self.size_pixel and self.pos[1] <= y <= self.pos[1] + self.size_pixel:
            x, y = x - self.pos[0], y - self.pos[1]
            x, y = x * self.size // self.size_pixel, y * self.size // self.size_pixel
            if self.board[x][y]!=0:
                return None
            self.board[x][y] = self.player
            self.player = (self.player % 2) + 1
            for x in range(self.size):
                for y in range(self.size):
                    if self.size-x>=3:
                        if self.board[x][y]==self.board[x+1][y]==self.board[x+2][y] and self.board[x][y]!=0:
                            return self.board[x][y]
                    if self.size-y>=3:
                        if self.board[x][y]==self.board[x][y+1]==self.board[x][y+2] and self.board[x][y]!=0:
                            return self.board[x][y]
                    if self.size-y>=3 and self.size-x>=3:
                        if self.board[x][y]==self.board[x+1][y+1]==self.board[x+2][y+2] and self.board[x][y]!=0:
                            return self.board[x][y]
                    if self.size-y>=3 and x>=2:
                        if self.board[x][y]==self.board[x-1][y+1]==self.board[x-2][y+2] and self.board[x][y]!=0:
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


field = TictactoeFild((50, 50), 600, 3)
while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                ans=field.click(mouse_pos[0], mouse_pos[1])
                if ans!=None:
                    field.restart()
    field.draw()
    pygame.display.update()
