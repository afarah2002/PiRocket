import pyglet
from pyglet.gl import *

window = pyglet.window.Window(width=1440, height=960)
window.projection = pyglet.window.Projection3D()
batch = pyglet.graphics.Batch()


@window.event
def on_draw():
    window.clear()
    batch.draw()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    glRotatef(1, dx, dy, 0)


def rotate(dt):
    glRotatef(.5, 0, 0, 1)


if __name__ == "__main__":
    glEnable(GL_MULTISAMPLE_ARB)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    model = pyglet.model.load("rocket.obj", batch=batch)
    glTranslatef(0, 0, -3)
    pyglet.clock.schedule_interval(rotate, 1/10)
    pyglet.app.run()
