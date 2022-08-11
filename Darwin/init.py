import pygame, sys, time, pyautogui, random, math
from sprites import Nub, Node
from pygame.constants import K_SPACE, K_ESCAPE, K_w, K_a, K_s, K_d
pygame.init()
pygame.font.init


#-----SETTINGS-----#

#--MAIN--#
screen_scale_factor = 0.9
cycle_time = 0.0001

#--ORGANISMS--#

##NUBS##
nub_starting_points = 100

num_nubs = 40
nub_starting_speed = 1
nub_starting_stamina = 1
nub_starting_size = 50
nub_stamina_drain_factor = 10 #value is used to determain stamina drain: self.stamina_drain = self.speed/VALUE

nub_fatigue_threshold_fixed = True #if true all nubs will slow down after the set threshold as been crossed
nub_fatigue_threshold = 0.10 #the percentage of stamina depletions which triggers the slowing of speed by half

##NODES##
num_nodes = 4
node_size_range = [10, 20] #also range of value for nodes

#--VISUALS--#
colors = {
    "background": (200, 200, 200),
    "nub": (100, 100, 100),
    "food": (100, 155, 100),
    "water": (0, 0, 255)
}

font = pygame.font.SysFont("monospace", 50)

#-----SETUP-----#

#--SCREEN SETUP--#
width, height = pyautogui.size()
width, height = screen_scale_factor*width, screen_scale_factor*height
size= width, height 
screen = pygame.display.set_mode(size)

#--SIMULATION SETUP--#
def setup():
    ## ORGANISMS ##
    nubs = [Nub(random.randint(50, width-50), random.randint(50, height-50), nub_starting_points, nub_starting_size, nub_starting_speed, nub_starting_stamina, nub_stamina_drain_factor, nub_fatigue_threshold_fixed, nub_fatigue_threshold, 0, colors, True)  for i in range(num_nubs)]
    food_nodes = {}
    for i in range(num_nodes): food_nodes[i] = Node(random.randint(50, width-50), random.randint(50, height-50), "food", random.randint(node_size_range[0], node_size_range[1]), colors)
    water_nodes = [Node(random.randint(50, width-50), random.randint(50, height-50), "water", random.randint(node_size_range[0], node_size_range[1]), colors) for i in range(num_nodes)]
    return nubs, food_nodes, water_nodes

def analyze(nubs):
    ordered = {}
    for nub in nubs:
        if nub.food_eaten not in ordered:
            ordered[nub.food_eaten] = [nub]
        else:
            ordered[nub.food_eaten].append(nub)
    #print(ordered)
    
    keys = sorted(ordered, reverse=True)
    #print(keys)
    ordered_list = []
    for key in keys:
        for nub in ordered[key]:
            ordered_list.append(nub)
            #print(key, nub)
    

    
    return ordered_list

def get_averages(nubs):
    sum = 0
    for nub in nubs: sum += nub.speed_points
    average = round(sum/len(nubs), 3)

    average_speed_txt = font.render(str(average), 1, (0, 0, 0))

    return average_speed_txt, average

def get_gen_average(generation_averages):
    sum = 0
    for ave in generation_averages:
        sum += ave
    
    average = round(sum/len(generation_averages), 3)
    ave_text = font.render(str(average), 1, (0, 0, 0))
    return(ave_text)

def next_generation(nubs):
    next_gen = []
    for i in range(math.floor(len(nubs)/4)):
        nubs[i].speed = nubs[i].base_speed
        nubs[i].stamina= nubs[i].base_stamina
        nubs[i].food_eaten = 0
        next_gen.append(nubs[i])
        for i in range(3):
            next_gen.append(Nub(random.randint(50, width-50), random.randint(50, height-50), nub_starting_points, nub_starting_size, nubs[i].speed_points, nub_starting_stamina,nub_stamina_drain_factor,nub_fatigue_threshold_fixed, nub_fatigue_threshold, 0, colors, False))
    return(next_gen)

#-----MAIN-----#
def main():

    nubs, food_nodes, water_nodes = setup()
    node_index = num_nodes # a running counter of the next index for a new node
    round_active = True
    generation_averages = []
    generation = 0

    while 1:
        now = time.time()
        screen.fill(colors["background"])
        keys=pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        if round_active == True:
            round_active = False
            for nub in nubs: 
                if nub.stamina > nub.stamina_drain: round_active = True
                if len(food_nodes) == 0: 
                    round_active = False
                    break
                nub.move(food_nodes)

            for nub in nubs: nub.draw(screen)
            for key in food_nodes: food_nodes[key].draw(screen)
            
            average_speed_txt, average = get_averages(nubs)
        
        else:
            generation_averages.append(average)
            gen_average_text = get_gen_average(generation_averages)
            generation +=1
            #print("round over")
            nubs_ordered = analyze(nubs)
            #print("analyzed", len(nubs_ordered))
            #quit
            nubs, food_nodes, water_nodes = setup()
            nubs = next_generation(nubs_ordered)
            round_active = True

        if generation > 1: screen.blit(gen_average_text, (width-200, 10))
        screen.blit(average_speed_txt, (10, 10))
        pygame.display.flip()
        elapsed = time.time()-now
        if elapsed < cycle_time:
            time.sleep(cycle_time-elapsed)


main()