import turtle
import math
import helpers
import random
import time

t = turtle.Turtle()
screensize = (1280, 720)
paused = False
current_task = 0

def unpause(fun, btn):
    global paused
    paused = False

def turtle_setup():
    global t
    t.screen.setup(screensize[0], screensize[1])
    t.screen.onscreenclick(unpause)
    t.pen(speed=0, shown=False)
    t.screen.tracer(0, 0)

def draw_task_finished():
    global paused, current_task, drawing_tasks
    current_task += 1
    paused = True
    if current_task < len(drawing_tasks):
        draw_task_after_keypress()

def draw_task_after_keypress():
    global paused, current_task
    if paused:
        turtle.ontimer(draw_task_after_keypress, 100)
    else:
        drawing_tasks[current_task]()

# ---===---
def draw_square():
    global t
    t.clear()

    t.pen(pencolor='red', pensize=1, speed=5, shown=False)
    t.up()
    square_side = screensize[0] / 4 

    t.setpos(t.pos() + (-square_side / 2, -square_side / 2))
    t.down()
    for i in range(4):
        t.forward(square_side)
        t.left(90)
    t.up()
    draw_task_finished()

def draw_axes():
    global t
    t.clear()
    
    t.pen(pencolor='blue', pensize=1, speed=0, shown=False)
    t.up()
    dot_width = 50
    dotline_size = screensize[0] / 3
    offset = dotline_size*2 / dot_width

    t.setpos(-dotline_size - offset/2, 0)
    for i in range(dot_width):
        t.up() if i % 2 == 0 else t.down()
        t.forward(offset)
        t.pensize(helpers.lerp(1, 4, (math.sin(i/dot_width) * 5) % 1))
    t.up()

    dotline_size = screensize[1] / 3
    offset = dotline_size*2 / dot_width
    t.setpos(0, -dotline_size - offset/2)
    t.left(90)

    for i in range(dot_width):
        t.up() if i % 2 == 0 else t.down()
        t.forward(offset)
        t.pensize(helpers.lerp(1, 4, (math.sin(i/dot_width) * 5) % 1))
    t.up()
    draw_task_finished()

def draw_cartoon():
    global t
    t.clear()

    t.pen(speed=0, shown=False)
    t.up()

    radius = 50
    grid = (5, 5)
    uv = (-screensize[0] / 2, -screensize[1] / 2)
    offset = radius + 30

    for i in range(grid[0]):
        for j in range(grid[1]):
            t.up()
            x = (uv[0] + (screensize[0] - offset*2) / (grid[0]-1) * i) + radius + offset
            y = (uv[1] + (screensize[1] - offset*2) / (grid[1]-1) * j) + offset
            t.setpos(x, y)
            _color = (random.random(),random.random(), random.random())
            t.color(_color)
            t.down()
            t.begin_fill()
            t.circle(radius)
            t.end_fill()


drawing_tasks = [draw_square, draw_axes, draw_cartoon]

turtle_setup()
drawing_tasks[0]()
t.screen.mainloop()
