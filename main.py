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

def draw_task_finished(func):
    def inner1(*args, **kwargs):

        func_to_return = func(*args, **kwargs)

        global paused, current_task, drawing_tasks
        current_task += 1
        paused = True
        if current_task < len(drawing_tasks):
            draw_task_after_keypress()

        return func_to_return
    return inner1

def draw_task_after_keypress():
    global paused, current_task, t
    if paused:
        turtle.ontimer(draw_task_after_keypress, 100)
    else:
        t.clear()
        drawing_tasks[current_task]()
        draw_text()

def draw_text():
    global t

    t.up()
    t.pen(pencolor='black')
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

        

drawing_tasks = [draw_square, draw_axes, draw_cartoon, draw_n_figure]
# drawing_tasks = [draw_n_figure]

turtle_setup()
drawing_tasks[0]()
draw_text()
t.screen.mainloop()
