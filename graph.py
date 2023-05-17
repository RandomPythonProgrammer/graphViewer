import os
import threading
import time

import pygame

import main


class App:
    def __init__(self):
        pygame.init()
        self.goblet = pygame.image.load('goblet.jpg')
        self.window = pygame.display.set_mode((self.goblet.get_width(), self.goblet.get_height()))
        self.xmin, self.xmax = -5.5, 12
        self.ymin, self.ymax = -4.15, 4.15
        self.graph_points = []
        if os.path.exists('data.csv'):
            with open('data.csv', 'r') as file:
                data = file.readlines()
                for line in data:
                    x, y = line.split(', ')
                    x, y = float(x), float(y)
                    tx = abs(self.xmax - self.xmin)
                    ty = abs(self.ymax - self.ymin)
                    rx = ((x - self.xmin) / tx) * self.window.get_width()
                    ry = ((y - self.ymin) / ty) * self.window.get_height()
                    ry = self.window.get_height() - ry
                    self.graph_points.append((rx, ry))
                    print(rx, ry)

    def draw(self):
        while True:
            pygame.display.flip()
            self.window.blit(self.goblet, (0, 0))
            for point in self.graph_points:
                pygame.draw.circle(self.window, center=point, radius=2, color=(255, 0, 255, 255))
            pygame.display.update()

    def start(self):
        last = time.time()
        while True:
            if pygame.mouse.get_pressed()[0] and time.time() - last > 1 / 1000:
                self.graph_points.append(pygame.mouse.get_pos())
                last = time.time()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.graph_points.clear()
                    if event.key == pygame.K_RETURN:
                        points = []
                        for point in self.graph_points:
                            x, y = point
                            y = self.window.get_height() - y
                            tx = abs(self.xmax - self.xmin)
                            ty = abs(self.ymax - self.ymin)
                            rx = self.xmin + (x / self.window.get_width()) * tx
                            ry = self.ymin + (y / self.window.get_height()) * ty
                            points.append((rx, ry))

                        print(points)
                        with open('data.csv', 'w') as file:
                            for point in points:
                                x, y = point
                                file.write(f'{x}, {y}\n')
                        main.make_stuff(points)
                    if event.key == pygame.K_z:
                        self.graph_points = self.graph_points[:-250]
                if event.type == pygame.QUIT:
                    os._exit(0)


if __name__ == '__main__':
    app = App()
    draw_thread = threading.Thread(target=app.draw)
    draw_thread.start()
    app.start()
