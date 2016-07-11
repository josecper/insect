import numpy
import argparse
import pyglet, pyglet.image, pyglet.gl, pyglet.clock


#constants and shit
delta = numpy.array(((0,1),
                     (1,0),
                     (0,-1),
                     (-1,0)))

grid_shape = (100, 100)
fps = 60
scale = 4

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

def go():
    window = pyglet.window.Window(grid_shape[0]*scale, grid_shape[1]*scale)
    pyglet.gl.glScalef(scale, scale, scale)
    ant = Ant(grid_shape)
    
    pyglet.clock.schedule_interval(refresh, 1/fps, ant)
    pyglet.app.run()    
    
def refresh(dt, ant):
    grid8 = numpy.uint8(ant.grid)*255
    im = pyglet.image.ImageData(*grid_shape, "L", bytes(grid8.data), -grid_shape[0])
    tex = im.get_texture()
    pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, tex.id)
    pyglet.gl.glTexParameteri(tex.target, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
    #print(numpy.count_nonzero(ant.grid), ant.position, ant.rotation, delta[ant.rotation])
    
    tex.blit(0,0,0)
    ant.step()

if __name__ == "__main__":
    go()

