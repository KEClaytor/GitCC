# Main pygame visualizer for commits

import pygame, sys
from pygame.locals import *
from math import pi, cos, sin

blackColor = pygame.Color(0, 0, 0)
whiteColor = pygame.Color(255, 255, 255)
ltgryColor = pygame.Color(15, 15, 15)
resOrb = 'resources/circle.png'
resOctocat = 'resources/gitcat.png'

# TODO: send these into another module
# Some helper functions
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

# TODO: scrape this from github
def get_rgb_from_code(code_type):
    ct_python = 'python'
    cc_python = '#3581ba'
    if code_type == ct_python:
        rgb = hex_to_rgb(cc_python)
    else:
        rgb = whiteColor
    return rgb

class gloworb:

    def __init__(self, cx, cy, size):
        self.x, self.y = cx-size/2, cy-size/2
        self.size = size
        # Load up the default orb image
        # TODO: Put this out of the init function
        orbimg = pygame.image.load(resOrb).convert_alpha()
        orbimg = pygame.transform.scale(orbimg, (size, size))
        self.orbimg = orbimg

    #def set_color(self, code_type):
    #    (r, g, b) = get_rgb_from_code(code_type)
    #    # surfcopy = self.surf.copy()
    #    arr = pygame.surfarray.pixels3d(self.surf)
    #    arr[:,:,0] = r
    #    arr[:,:,1] = g
    #    arr[:,:,2] = b

    def blit(self, window):
        window.blit(self.orbimg, (self.x, self.y))

class orb_ring:
    def __init__(self, numorbs, radius, center_x, center_y, backgroundColor):
        self.n = numorbs
        self.r = radius
        self.cx, self.cy = center_x, center_y
        self.ox, self.oy = center_x-radius, center_y-radius
        self.screen = pygame.Surface((2*radius, 2*radius))
        self.screen.fill(backgroundColor)
        self.orbs = []
        orb_size = radius/2
        for ii in range(self.n):
            orbx = center_x + radius*sin(2*pi*ii/self.n)
            orby = center_y + radius*cos(2*pi*ii/self.n)
            self.orbs.append(gloworb(orbx, orby, orb_size))

    def blit(self, window):
        window.blit(self.screen, (self.ox, self.oy))
        for orb in self.orbs:
            orb.blit(window)

if __name__ == "__main__":
    pygame.init()
    fpsClock = pygame.time.Clock()

    # Get the screen size and make our window full screen
    scnInfo = pygame.display.Info()
    window = pygame.display.set_mode((scnInfo.current_w, scnInfo.current_h))
    pygame.display.set_caption('GitCC')

    # Assuming landscape screen
    sw = window.get_width()
    sh = window.get_height()

    oh = sh
    ox = (sw-sh)/2
    octocat = pygame.image.load(resOctocat).convert_alpha()
    octocat = pygame.transform.scale(octocat, (oh, oh))
    # Create the hued orbs
    orbs = orb_ring(32, oh*4/10, sw/2, sh/2, ltgryColor)
    print orbs
    octoorb = pygame.image.load(resOrb).convert_alpha()
    # Execute the moves
    while True:
        # Base window fill
        window.fill(blackColor)
        # Draw the orbs
        orbs.blit(window)
        # Draw octocat
        window.blit(octocat, (ox, 0))
        # Get user key presses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                print "Good Job, you pressed a key!"

        pygame.display.update()
        fpsClock.tick(30)

