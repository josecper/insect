import numpy
import argparse
import pyglet, pyglet.image, pyglet.gl, pyglet.clock


#constants and shit
delta = numpy.array(((0,1),
                     (1,0),
                     (0,-1),
                     (-1,0)))

grid_shape = (240, 240)
fps = 60
sps = 60
scale = 2
initial_iter = 2000000

class Ant:

    def __init__(self, grid_shape):

        self.grid = numpy.zeros(grid_shape, dtype=numpy.bool)
        
        start_x = numpy.random.randint(grid_shape[0])
        start_y = numpy.random.randint(grid_shape[1])
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

def go(ant):
    window = pyglet.window.Window(ant.grid.shape[0]*scale, ant.grid.shape[1]*scale)
    pyglet.gl.glScalef(scale, scale, scale)

    #doesn't work, pyglet limits scheduled functions to max fps
    pyglet.clock.schedule_interval(step_ant, 1/sps, ant)
    pyglet.clock.schedule_interval_soft(refresh, 1/fps, ant)
    pyglet.clock.schedule_interval_soft(info, 5, ant)
    pyglet.app.run()    
    
def refresh(dt, ant):
    grid8 = numpy.uint8(ant.grid)*255
    im = pyglet.image.ImageData(*ant.grid.shape, "L", bytes(grid8.data), -ant.grid.shape[1])
    tex = im.get_texture()
    pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, tex.id)
    pyglet.gl.glTexParameteri(tex.target, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
    tex.blit(0,0,0)

def step_ant(dt, ant):
    ant.step()

def info(dt, ant):
    print("dots: {0}, ant position: {1}, ant rotation: {2}".format(numpy.count_nonzero(ant.grid), ant.position, ant.rotation))
    
if __name__ == "__main__":
    ant = Ant(grid_shape)
    for i in range(initial_iter):
        ant.step()
        
    go(ant)

