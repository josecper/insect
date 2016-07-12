import numpy
import argparse
import pyglet, pyglet.image, pyglet.gl, pyglet.clock

parser = argparse.ArgumentParser(description="do a nice insect")
parser.add_argument("--shape", type=str, default="240x240")
parser.add_argument("--fps", type=float, default=60.0)
parser.add_argument("--sps", type=float, default=60.0)
parser.add_argument("--scale", type=int, default=4)
parser.add_argument("--ants", type=int, default=1)
parser.add_argument("--trons", type=int, default=0)
parser.add_argument("--start", type=int, default=0)

namespace = parser.parse_args()

#nice parameter wow
grid_shape = tuple(int(x) for x in namespace.shape.split("x")) #doesn't render correctly for non-square grids for some reason
fps = namespace.fps #frames per second, limited by vsync
sps = namespace.sps #simulation steps per second (currently does nothing if above fps)
scale = namespace.scale #resolution scaling (integers work best)
ants = namespace.ants #number of ants
trons = namespace.trons #number of trons
initial_iter = namespace.start #precalculate this many simulation steps

#constants and shit
delta = numpy.array(((0,1),
                     (1,0),
                     (0,-1),
                     (-1,0)))

class Colony:

    def __init__(self, grid_shape):
        self.grid = numpy.zeros(grid_shape, dtype=numpy.bool)
        self.ants = []

    def add_ant(self, ant_class):
        self.ants.append(ant_class(self.grid))

    def step(self):
        for ant in self.ants:
            ant.step()

class Ant:

    def __init__(self, grid):

        self.grid = grid
        
        start_x = numpy.random.randint(grid.shape[0])
        start_y = numpy.random.randint(grid.shape[1])
        self.position = numpy.array((start_x, start_y))
        self.rotation = numpy.random.randint(0, 4)

        def step(self):

        coords = tuple(self.position)
        
        if self.grid[coords]:
            self.rotation = (self.rotation - 1) % 4
        else:
            self.rotation = (self.rotation + 1) % 4
            
        self.grid[coords] = -self.grid[coords]
        self.position = (self.position + delta[self.rotation]) % self.grid.shape

class Tron(Ant):

    def step(self):

        coords = tuple(self.position)

        if self.grid[coords]:
            self.rotation = (self.rotation + 1) % 4

        self.grid[coords] = -self.grid[coords]
        self.position = (self.position + delta[self.rotation]) % self.grid.shape
        
def go(colony):
    window = pyglet.window.Window(colony.grid.shape[1]*scale, colony.grid.shape[0]*scale)
    pyglet.gl.glScalef(scale, scale, scale)

    #doesn't work, pyglet limits scheduled functions to max fps
    pyglet.clock.schedule_interval(step_colony, 1/sps, colony)
    pyglet.clock.schedule_interval_soft(refresh, 1/fps, colony)
    pyglet.clock.schedule_interval_soft(info, 5, colony)
    pyglet.app.run()    
    
def refresh(dt, colony):
    grid8 = (numpy.uint8(colony.grid)*255)
    im = pyglet.image.ImageData(colony.grid.shape[1],
                                colony.grid.shape[0],
                                "L", bytes(grid8.data),
                                -colony.grid.shape[1]) #wow it's trick wow
    tex = im.get_texture()
    pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, tex.id)
    pyglet.gl.glTexParameteri(tex.target, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
    tex.blit(0,0,0)

def step_colony(dt, colony):
    colony.step()

def info(dt, colony):
    print("dots: {0}, ant positions: {1}, ant rotations: {2}".format(numpy.count_nonzero(colony.grid),
                                                                     [ant.position for ant in colony.ants],
                                                                     [ant.rotation for ant in colony.ants]))
    
if __name__ == "__main__":
    colony = Colony(grid_shape)
    for i in range(ants):
        colony.add_ant(Ant)

    for i in range(trons):
        colony.add_ant(Tron)
        
    for i in range(initial_iter):
        colony.step()
        
    go(colony)

