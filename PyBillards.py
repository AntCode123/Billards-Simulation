import pygame, sys, math

pygame.init()
wn = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()

class Vector:
    def __init__(self):
        pass

    def add(self, vec1, vec2):
        vec = [vec1[0] + vec2[0], vec1[1] + vec2[1]]
        return vec

    def sub(self, vec1, vec2):
        vec = [vec1[0] - vec2[0], vec1[1] - vec2[1]]
        return vec

    def normalise(self, vec):
        mag = self.magnitude(vec)
        vec = self.scalar_divide(mag, vec)
        return vec

    def magnitude(self, vec):
        mag = math.sqrt(vec[0]**2 + vec[1]**2)
        return mag

    def scalar_multiply(self, scl, vec):
        vec = [vec[0] * scl, vec[1] * scl]
        return vec

    def scalar_divide(self, scl, vec):
        vec = [vec[0] / scl, vec[1] / scl]
        return vec

    def dot_product(self, vec1, vec2):
        scl = vec1[0] * vec2[0] + vec1[1] * vec2[1]
        return scl

    
class Game:
    def __init__(self):
        self.FPS = 400
        self.pocket_locations = [(205, 205), (995, 205), (205, 595), (600, 190), (600, 610), (995, 595)]

    def events(self):
        mouse = pygame.mouse.get_pos()
        mx = mouse[0]
        my = mouse[1]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.select_cue_ball(mx, my)
                    print(mx, my)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and cue_ball.ready:
                    self.release_cue_ball(mx, my)

        for i in range(len(balls)-1):
            for j in range(i+1, len(balls)):
                balls[i].collide_with(balls[j])

        for ball in balls:
            if ball.location[0] + 16 > 235 and ball.location[0] - 16 < 570 and ball.location[1] - 16 < 200 and ball.location[1] - 16 > 195:
                ball.velocity = [ball.velocity[0], -ball.velocity[1]]
            elif ball.location[0] + 16 > 630 and ball.location[0] - 16 < 965 and ball.location[1] - 16 < 200 and ball.location[1] - 16 > 195:
                ball.velocity = [ball.velocity[0], -ball.velocity[1]]
            elif ball.location[0] + 16 > 235 and ball.location[0] - 16 < 570 and ball.location[1] + 16 > 600 and ball.location[1] + 16 < 605:
                ball.velocity = [ball.velocity[0], -ball.velocity[1]]
            elif ball.location[0] + 16 > 630 and ball.location[0] - 16 < 965 and ball.location[1] + 16 > 600 and ball.location[1] + 16 < 605:
                ball.velocity = [ball.velocity[0], -ball.velocity[1]]
            elif ball.location[1] + 16 > 245 and ball.location[1] - 16 < 555 and ball.location[0] - 16 < 200 and ball.location[0] - 16 > 195: 
                ball.velocity = [-ball.velocity[0], ball.velocity[1]]
            elif ball.location[1] + 16 > 245 and ball.location[1] - 16 < 555 and ball.location[0] + 16 > 1000 and ball.location[0] + 16 < 1005: 
                ball.velocity = [-ball.velocity[0], ball.velocity[1]]

        self.check_if_pot()
                
    def create_balls(self, r):
        x, y = 450, 400
        k = 6
        for i in range(5):
            for j in range(5-i):
                balls.append(Ball(x, y, (255, 0, 0)))
                x -= r*(3**0.5)
                y += r
            y -= r * k
            x += (k-2)*(r*(3**0.5))
            k -= 1

    def check_if_pot(self):
        for pocket in self.pocket_locations:
            for ball in balls:
                a = ball.location[0] - pocket[0]
                b = ball.location[1] - pocket[1]
                distance = math.sqrt(a**2 + b**2)
                if distance + 16 <= 30 or ball.location[0] - 16 < 190 or ball.location[0] + 16 > 1010 or ball.location[1] - 16 < 190 or ball.location[1] + 16 > 620:
                    if ball != cue_ball:
                        balls.remove(ball)
                    else:
                        cue_ball.location = [800, 400]
                        cue_ball.velocity = [0, 0]
                    

    def select_cue_ball(self, mx, my):
        a = mx - cue_ball.location[0]
        b = my - cue_ball.location[1]
        distance = math.sqrt(a**2 + b**2)

        if distance <= 16:
            cue_ball.ready = True

    def release_cue_ball(self, mx, my):
        normal = vector.sub(cue_ball.location, [mx, my])
        normalised = vector.normalise(normal)
        mag = vector.magnitude(normal)
        cue_ball.velocity = vector.scalar_multiply(mag/50, normalised)
        cue_ball.ready = False

    def animate(self):
        for ball in balls:
            ball.location = vector.add(ball.location, ball.velocity)
            ball.velocity = vector.scalar_multiply(0.995, ball.velocity)

    def render(self):
        pygame.draw.rect(wn, (50, 50, 50), (150 , 150, 900, 500))
        pygame.draw.rect(wn, (9, 134, 43), (200, 200, 800, 400))
        pygame.draw.rect(wn, (149, 69, 21), (240, 150, 720, 50))
        pygame.draw.rect(wn, (149, 69, 21), (240, 600, 720, 50))
        pygame.draw.rect(wn, (149, 69, 21), (150, 240, 50, 320))
        pygame.draw.rect(wn, (149, 69, 21), (1000, 240, 50, 320))
        pygame.draw.rect(wn, (200, 200, 200), (800, 200, 3, 400))
        pygame.draw.arc(wn, (200, 200, 200), (700, 300, 200, 200), -math.pi/2, math.pi/2, 3)

        pygame.draw.circle(wn, (0, 0, 0), (205, 205), 30)
        pygame.draw.circle(wn, (0, 0, 0), (995, 205), 30)
        pygame.draw.circle(wn, (0, 0, 0), (205, 595), 30)
        pygame.draw.circle(wn, (0, 0, 0), (995, 595), 30)
        pygame.draw.circle(wn, (0, 0, 0), (600, 190), 30)
        pygame.draw.circle(wn, (0, 0, 0), (600, 610), 30)

        for ball in balls:
            pygame.draw.circle(wn, ball.color, (ball.location[0], ball.location[1]), 16)

        mouse = pygame.mouse.get_pos()
        mx = mouse[0]
        my = mouse[1]
        
        if cue_ball.ready:
            pygame.draw.line(wn, (255, 255, 255), (cue_ball.location[0], cue_ball.location[1]), (mx, my), 5)

    def update(self):
        pygame.display.update()
        wn.fill((0, 0, 0))
        clock.tick(self.FPS)
        

class Ball:
    def __init__(self, x, y, color):
        self.location = [x, y]
        self.velocity = [0, 0]
        self.color = color
        self.ready = False

    def distance_from(self, other):
        a = self.location[0] - other.location[0]
        b = self.location[1] - other.location[1]
        distance = math.sqrt(a**2 + b**2)
        return distance

    def collide_with(self, other):
        radii = 32
        if self.distance_from(other) < radii:
            normal = vector.sub(self.location, other.location)
            normal = vector.normalise(normal)

            depth = radii - self.distance_from(other)

            self.collision_resolve(other, normal, depth)
            self.collision_response(other, normal)

    def collision_resolve(self, other, normal, depth):
        self.location = vector.add(self.location, vector.scalar_multiply(depth/2, normal))
        other.location = vector.add(other.location, vector.scalar_multiply(-depth/2, normal))

        
    def collision_response(self, other, normal):
        relative_velocity = vector.sub(self.velocity, other.velocity)
        separating_velocity = vector.dot_product(relative_velocity, normal)
        separating_velocity_vector = vector.scalar_multiply(separating_velocity, normal)
        self.velocity = vector.sub(self.velocity, separating_velocity_vector)
        other.velocity = vector.add(other.velocity, separating_velocity_vector)
        
            

vector = Vector()
game = Game()
cue_ball = Ball(800, 400, (255, 255, 255))
balls = [cue_ball]
game.create_balls(16)


while True:
    game.events()
    game.animate()
    game.render()
    game.update()
