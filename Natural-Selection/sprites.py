import pygame, math, time, random


class Nub:
    #def __init__(self, init_x, init_y, starting_points, size, speed, stamina,stamina_drain_factor,nub_fatigue_threshold_fixed, nub_fatigue_threshold,direction, colors, first_gen):
    def __init__(self, init_x, init_y,nub_info, colors, first_gen, screen_width, screen_height):
        self.screen_width, self.screen_height = screen_width, screen_height

        starting_points = nub_info["starting_points"]
        starting_speed = nub_info["starting_speed"]
        starting_size = nub_info["starting_size"]

        starting_stamina = nub_info["starting_stamina"]
        stamina_drain_factor = nub_info["stamina_drain_factor"]
        
        fatigue_threshold_is_fixed = nub_info["fatigue_threshold_is_fixed"]
        fatigue_threshold = nub_info["fatigue_threshold"]

        self.detection_radius_is_active = nub_info["detection_radius_is_active"]
        self.detection_radius = nub_info["detection_radius"]



        if first_gen == True:
            self.attribute_points = starting_points
            self.speed_points = starting_speed + random.randint(0, starting_points)
            self.stamina = starting_stamina + starting_points - self.speed_points + starting_speed
        else:
            self.speed_points = starting_speed + random.randint(-math.ceil(starting_points/50), math.ceil(starting_points/50))
            if self.speed_points<0: self.speed_points = 0
            self.stamina = starting_stamina + starting_points - self.speed_points
        
        self.x, self.y, self.color = init_x, init_y, colors["nub"]

        self.size = starting_size * (1-(self.speed_points/starting_points))
        self.speed = self.speed_points/10

        self.fatigue_threshold_fixed = fatigue_threshold_is_fixed
        if self.fatigue_threshold_fixed == False:
            self.fatigue_threshold = self.speed_points/starting_points
        else: self.fatigue_threshold = fatigue_threshold

        self.objective_index = None
        self.objective = None
        
        
        self.stamina_drain = self.speed/stamina_drain_factor

        self.base_speed = self.speed
        self.base_stamina = self.stamina

        self.food_eaten = 0

        self.wandering = False

    def move(self, food_nodes):
        if self.wandering == False:
            if self.objective == None or self.objective_index not in food_nodes:
                self.objective_index = self.look_for_nodes(food_nodes)
                if self.objective_index != None: 
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
        else:
            if self.look_for_nodes(food_nodes) != None:
                self.wandering = False
                self.move(food_nodes)
            else:
                self.angle += random.randint(-1, 3)
                if self.stamina > self.stamina_drain/2:
                    #if self.stamina < (self.fatigue_threshold*self.base_stamina)+self.stamina_drain/2 and self.stamina > (self.fatigue_threshold*self.base_stamina)-self.stamina_drain/2: self.speed *= 0.5
                    self.x += math.cos(math.radians(self.angle)) * self.speed/2
                    self.y += math.sin(math.radians(self.angle)) * self.speed/2
                    self.stamina -= self.stamina_drain/2


    
    def get_angle(self):
        xdis = self.objective.x - self.x
        ydis = self.objective.y - self.y

        angle = math.degrees(math.atan2((ydis),(xdis)))


       # 
        # if xdis != 0:
        #     angle =math.degrees(math.atan(ydis/xdis))
        # else: angle =math.degrees(math.atan(1))

        # if xdis <0: angle += 180

        angle = angle %360
        if angle <0: angle = 360 + angle
        return angle

        ##could u use pythag? if you know a side and hypoteneuse cant u use sin/cos to solve for the angle??
    
    def look_for_nodes(self, food_nodes):
        nodes = {}
        for node in food_nodes:
            distance = math.sqrt( abs(self.x-food_nodes[node].x)**2 + abs(self.y-food_nodes[node].y)**2 )
            if self.detection_radius_is_active == False: nodes[distance] = node #distance points to the node's index
            else:
                if distance <= self.detection_radius: nodes[distance] = node #distance points to the node's index
        if len(nodes) != 0:
            distances = list(nodes.keys())
            distances = sorted(distances)
            return nodes[distances[0]]
        else:
            self.wandering = True
            if self.x < self.screen_width/2:
                if self.y < self.screen_width/2:self.angle = 45
                else:self.angle = 315
            else:
                if self.y < self.screen_width/2:self.angle = 215
                else:self.angle = 135

            return None
        

    
    def draw(self, screen):
        if self.detection_radius_is_active == True:
            pygame.draw.ellipse(screen, self.color, pygame.Rect(self.x-self.detection_radius/2, self.y-self.detection_radius/2, self.detection_radius, self.detection_radius), 10)
        pygame.draw.ellipse(screen, self.color, pygame.Rect(self.x-self.size/2, self.y-self.size/2, self.size, self.size))
    


class Node:
    def __init__(self, x, y, type, value, colors):
        self.x, self.y = x, y
        self.type = type
        self.value, self.size = value, value
        self.color = colors[self.type]
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, pygame.Rect(self.x-self.size/2, self.y-self.size/2, self.size, self.size))
    


