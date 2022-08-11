import pygame, math, time, random


class Nub:
    def __init__(self, init_x, init_y, starting_points, size, speed, stamina,stamina_drain_factor,nub_fatigue_threshold_fixed, nub_fatigue_threshold,direction, colors, first_gen):

        if first_gen == True:
            self.attribute_points = starting_points
            self.speed_points = speed + random.randint(0, starting_points)
            self.stamina = stamina + starting_points - self.speed_points + speed
        else:
            self.speed_points = speed + random.randint(-math.ceil(starting_points/50), math.ceil(starting_points/50))
            self.stamina = stamina + starting_points - self.speed_points
        
        self.x, self.y, self.color, self.direction = init_x, init_y, colors["nub"], direction

        self.size = size * (1-(self.speed_points/starting_points))
        self.speed = self.speed_points/10

        self.fatigue_threshold_fixed = nub_fatigue_threshold_fixed
        if self.fatigue_threshold_fixed == False:
            self.fatigue_threshold = self.speed_points/starting_points
        else: self.fatigue_threshold = nub_fatigue_threshold

        self.objective_index = None
        self.objective = None
        
        
        self.stamina_drain = self.speed/stamina_drain_factor

        self.base_speed = self.speed
        self.base_stamina = self.stamina

        self.food_eaten = 0

    def move(self, food_nodes):
        if self.objective == None or self.objective_index not in food_nodes:
            self.objective_index = self.look_for_nodes(food_nodes)
            self.objective = food_nodes[self.objective_index]
            self.angle = self.get_angle()

        else:
            if self.stamina > self.stamina_drain:
                if self.stamina < (self.fatigue_threshold*self.base_stamina)+self.stamina_drain/2 and self.stamina > (self.fatigue_threshold*self.base_stamina)-self.stamina_drain/2: self.speed *= 0.5
                self.x += math.cos(math.radians(self.angle)) * self.speed
                self.y += math.sin(math.radians(self.angle)) * self.speed
                self.stamina -= self.stamina_drain

                


                if math.sqrt( abs(self.x-self.objective.x)**2 + abs(self.y-self.objective.y)**2) <= self.objective.size/2 + self.size/2 + self.speed:
                    self.food_eaten += self.objective.value
                    food_nodes.pop(self.objective_index)

    
    def get_angle(self):
        xdis = self.objective.x - self.x
        ydis = self.objective.y - self.y
       # 
        if xdis != 0:
            angle =math.degrees(math.atan(ydis/xdis))
        else: angle =math.degrees(math.atan(0))

        if xdis <0: angle += 180

        angle = angle %360
        if angle <0: angle = 360 + angle
        return angle

        ##could u use pythag? if you know a side and hypoteneuse cant u use sin/cos to solve for the angle??
    
    def look_for_nodes(self, food_nodes):
        nodes = {}
        for node in food_nodes:
            distance = math.sqrt( abs(self.x-food_nodes[node].x)**2 + abs(self.y-food_nodes[node].y)**2 )
            nodes[distance] = node #distance points to the node's index
        
        distances = list(nodes.keys())
        distances = sorted(distances)
        return nodes[distances[0]]
        

    
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, pygame.Rect(self.x-self.size/2, self.y-self.size/2, self.size, self.size))
    


class Node:
    def __init__(self, x, y, type, value, colors):
        self.x, self.y = x, y
        self.type = type
        self.value, self.size = value, value
        self.color = colors[self.type]
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, pygame.Rect(self.x-self.size/2, self.y-self.size/2, self.size, self.size))
    


