import pygame
import random, sys

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 720, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()
FPS = 60

pygame.mouse.set_visible(False)

degree_sign = u'\N{DEGREE SIGN}'


def draw_text(text = str, location = (0, 0), color = 'white', size = int):
    font = pygame.font.SysFont('Agency FB', size)
    blit_text = font.render(f'{text}', 1, color)
    screen.blit(blit_text, location)


def vec2_angle_of_vector(x, y):
    return pygame.math.Vector2(x, y).angle_to((0, 1))


def vec2_angle_btwn_vectors(x1, y1, x2, y2):
    angle = pygame.math.Vector2(x1, y1).angle_to((x2, y2))
    if abs(angle) > 180:
        angle = 360 - abs(angle)
    return format(abs(angle), '.2f')


def distance_to_point(x1, y1, x2, y2):
    return pygame.math.Vector2(x2 - x1, y2 - y1).length()


def gen_random_triangle():
    point1 = pygame.math.Vector2((random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))
    point2 = pygame.math.Vector2((random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))
    point3 = pygame.math.Vector2((random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))
    return point1, point2, point3


def gen_random_polygon():
    num_points = random.randint(4, 8)
    points = []
    for _ in range(num_points):
        point = pygame.math.Vector2((random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))
        points.append(point)
    return points


def center_point(points_list):
    num_sides, sum_x, sum_y = 0, 0, 0
    for vector in points_list:
        temp_x, temp_y = vector
        sum_x += temp_x
        sum_y += temp_y
        num_sides += 1
    x = sum_x / num_sides
    y = sum_y / num_sides
    return pygame.math.Vector2((x, y))


def draw_center_point(x, y):
    pygame.draw.circle(screen, 'blue', (x, y), 1)


class Triangle():
    def __init__(self, point1, point2, point3):
        self.points = [point1, point2, point3]
    
    def draw(self, color1='green', color2='red'):
        pygame.draw.polygon(screen, color1, self.points, width=1)
        point1, point2, point3 = self.points
        draw_text(f'{vec2_angle_btwn_vectors(*(point3 - point1), *(point2 - point1))}{degree_sign}', point1, color2, 20)
        draw_text(f'{vec2_angle_btwn_vectors(*(point1 - point2), *(point3 - point2))}{degree_sign}', point2, color2, 20)
        draw_text(f'{vec2_angle_btwn_vectors(*(point2 - point3), *(point1 - point3))}{degree_sign}', point3, color2, 20)
        

class Polygon():
    def __init__(self):
        self.points = []

    def draw(self, color1='green', color2='red'):
        pygame.draw.polygon(screen, color1, self.points, width=1)
        end = len(self.points) - 1
        for i, point in enumerate(self.points, start=0):
            if i == end:
                draw_text(f'{vec2_angle_btwn_vectors(*(self.points[i - 1] - self.points[i]), *(self.points[0] - self.points[i]))}{degree_sign}', self.points[i], color2, 20)
                break
            if i == 0:
                draw_text(f'{vec2_angle_btwn_vectors(*(self.points[end] - self.points[i]), *(self.points[1] - self.points[i]))}{degree_sign}', self.points[i], color2, 20)
            else:
                draw_text(f'{vec2_angle_btwn_vectors(*(self.points[i - 1] - self.points[i]), *(self.points[i + 1] - self.points[i]))}{degree_sign}', self.points[i], color2, 20)


def main():
    run = True
    triangles = []
    polygons = []

    while run:
        screen.fill('black')
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        draw_text('Press [t] to generate triangle', (0, 0), 'white', 25)
        draw_text('Press [p] to generate random polygon', (0, 25), 'white', 25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    triangles.clear()
                    polygons.clear()
                    point1, point2, point3 = gen_random_triangle()
                    triangle = Triangle(point1, point2, point3)
                    triangles.append(triangle)
                
                if event.key == pygame.K_p:
                    triangles.clear()
                    polygons.clear()
                    p_points = gen_random_polygon()
                    polygon = Polygon()
                    polygon.points = p_points
                    polygons.append(polygon)
                
        for triangle in triangles:
            triangle.draw()

        for polygon in polygons:
            polygon.draw()

        if len(triangles) > 0:
            dist = int(distance_to_point(*center_point(triangle.points), *mouse_pos))
            draw_center_point(*center_point(triangle.points))
        elif len(polygons) > 0:
            dist = int(distance_to_point(*center_point(polygon.points), *mouse_pos))
            draw_center_point(*center_point(polygon.points))
        else:
            dist = 0

        draw_text(f'{dist}', mouse_pos, 'blue', 20)

        pygame.display.flip()


if __name__ == '__main__':
    main()