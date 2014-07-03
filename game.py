from pyglet import gl
from pyglet import window
from pyglet import app
from pyglet import clock
from pyglet.window import key
from pyglet.window import mouse
import time
from state import *
from random import randrange

update_period = 1
last_update = time.time()
pause = 0 

SPEED_MODIFIER_STEP = 0.75
speed_IO = 1
pause_IO = pause
point_buffer_IO = []

w = 800 #window.width
h = 800 #window.height
# Direct OpenGL commands to this window.
window = window.Window(w, h)

w = window.width
h = window.height

state = create_empty_state()
state = set(state, [[1, 1], [1, 2], [1, 3]], 1)

start_x, end_x = ((w - h) / 2), ((w + h) / 2)
start_y, end_y = 0, h
step = h / Y

def draw_camera():
    gl.glViewport(0, 0, w, h)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0, w, 0, h, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glLoadIdentity()

def draw_grid():
    gl.glColor3f(0.2, 0.2, 0.2) 
    gl.glBegin(gl.GL_LINES)
    for i in range(1, X):
        x = start_x + step * i
        y = start_y + step * i
        
        gl.glVertex2f(start_x, start_y + i * step)
        gl.glVertex2f(end_x, start_y + i * step)

        gl.glVertex2f(start_x + i * step, start_y)
        gl.glVertex2f(start_x + i * step, end_y)
    gl.glEnd()

def draw_state(state):
    gl.glColor3f(1, 1, 1)
    gl.glBegin(gl.GL_TRIANGLES)
    for i in range(Y):
        for j in range(X):
            if get(state, i, j) == 1:
                x = start_x + step * j
                y = start_y + step * i

                nb = count_neighbours(state, i, j)
                if nb < 2 or nb > 3:
                    gl.glColor3f(1, 0, 0)
                else:
                    gl.glColor3f(0, 1, 0)

                gl.glVertex2f(x, y)
                gl.glVertex2f(x + step, y)
                gl.glVertex2f(x, y + step)
                gl.glVertex2f(x + step, y)
                gl.glVertex2f(x + step, y + step)
                gl.glVertex2f(x, y + step)
    gl.glEnd()

def draw(state):
    draw_camera()
    draw_grid()
    draw_state(state)

def updateIO(state, last_update, update_period):
    global speed_IO, pause_IO, point_buffer_IO

    update_period = update_period * speed_IO
    speed_IO = 1

    pause = pause_IO

    for point in point_buffer_IO:
        x = (point[0] - start_x) / step
        y = (point[1] - start_y) / step
        state = set(state, [[y, x]], 1 - get(state, y, x)) 
    point_buffer_IO = []

    if (time.time() > last_update + update_period) and not(pause):
        state = get_next_state(state)
        last_update = time.time()
    return (state, last_update, update_period)

@window.event
def on_key_press(symbol, modifiers):
    global speed_IO, pause_IO
    if symbol == key.SPACE:
        pause_IO = 1 - pause_IO
    elif symbol == key.MINUS:
        speed_IO = speed_IO / SPEED_MODIFIER_STEP
    elif symbol == key.EQUAL:
        speed_IO = speed_IO * SPEED_MODIFIER_STEP

@window.event
def on_mouse_press(x, y, button, modifiers):
    global point_buffer_IO
    if button == mouse.LEFT:
        point_buffer_IO.append([x, y])

while not window.has_exit:
    dt = clock.tick()
    (state, last_update, update_period) = updateIO(state, last_update, update_period)

    window.dispatch_events()
    window.clear()
    draw(state)
    window.flip()


