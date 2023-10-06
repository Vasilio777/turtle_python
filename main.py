import turtle
import math
import helpers
import random
import time

t = turtle.Turtle()
screensize = (1280, 720)
paused = False
curr_task = 0
next_task = 0

def unpause(fun, btn):
    global paused
    paused = False

def turtle_setup():
    global t
    t.screen.setup(screensize[0], screensize[1])
    t.screen.onscreenclick(unpause)
    t.pen(speed=0, shown=False)
    t.screen.tracer(0, 0)

def draw_task_finished(func):
    def inner1(*args, **kwargs):

        func_to_return = func(*args, **kwargs)

        global paused, next_task, curr_task, drawing_tasks
        next_task += 1
        paused = True
        if next_task >= len(drawing_tasks):
            next_task = 0

        draw_task_after_keypress()

        # another var for UI (after a drawing call)
        if curr_task >= len(drawing_tasks):
            curr_task = 0
        curr_task += 1

        return func_to_return
    return inner1

def draw_task_after_keypress():
    global paused, next_task, t
    if paused:
        turtle.ontimer(draw_task_after_keypress, 100)
    else:
        t.clear()
        drawing_tasks[next_task]()
        draw_text()

def draw_text():
    global t, curr_task

    t.up()
    t.pen(pencolor='black')

    t.setpos(0, screensize[1]/2.3)
    t.down()
    t.write(curr_task, font=("Verdana", 18, "normal"), align="center")
    t.up()

    t.setpos(0, screensize[1]/2.5)
    t.down()
    t.write('Press LMB to see the next.', font=("Verdana", 15, "normal"), align="center")
    t.up()

# ---===---
@draw_task_finished
def draw_square():
    global t

    t.up()
    t.home()
    t.pen(pencolor='red', pensize=1)
    
    square_side = screensize[0] / 4 

    t.setpos(t.pos() + (-square_side / 2, -square_side / 2))
    t.down()
    for i in range(4):
        t.forward(square_side)
        t.left(90)
    t.up()

@draw_task_finished
def draw_axes():
    global t
    
    t.pen(pencolor='blue', pensize=1)
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

@draw_task_finished
def draw_cartoon():
    global t

    t.pen(speed=0)
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

@draw_task_finished
def draw_n_figure():
    global t

    t.up()
    t.pen(pensize=2)
    
    figures_amount = 5
    circle_distrib_r = 200
    for i in range(figures_amount):
        t.up()
        _color = (random.random(),random.random(), random.random())
        t.color(_color)
        angle = math.radians(i * 360 / figures_amount)
        x = circle_distrib_r*math.cos(angle)
        y = circle_distrib_r*math.sin(angle)

        t.setpos(x, y)
        t.down()

        n = random.choice(range(3, 10))
        for _ in range(n):
            t.forward(50)
            t.right(360 / n)

@draw_task_finished
def draw_random_walk():
    global t

    t.up()
    t.home()
    # t.screen.clearscreen()
    t.pen(speed=9)
    _color = (random.random(), random.random(), random.random())

    dist = 20
    edge_x = screensize[0] / 2 - dist*1.1
    edge_y = screensize[1] / 2 - dist*1.1

    t.down()
    for i in range(1000):
        _color = (random.random(), random.random(), random.random())
        t.pen(pencolor=_color, pensize=random.choice(range(1, 5)))
        if (-edge_x < t.xcor() < edge_x) and (-edge_y < t.ycor() < edge_y):
            t.right(random.choice([-90, 0, 90]))
            t.forward(dist)
        else:
            t.right(180)
            t.forward(dist)

@draw_task_finished
def draw_spirograph():
    global t 

    t.up()
    t.home()
    t.pen(pensize=1)
    rad = 100
    n = 50

    t.down()
    for i in range(n):
        t.right(360 / n)
        _color = (random.random(), random.random(), random.random())
        t.pen(pencolor=_color)
        t.circle(rad)

drawing_tasks = [draw_square, draw_axes, draw_cartoon, draw_n_figure, draw_random_walk, draw_spirograph]
# drawing_tasks = [draw_spirograph]

turtle_setup()
drawing_tasks[0]()
draw_text()
t.screen.mainloop()
