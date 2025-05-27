from browser import document, window
from browser import timer
import math
import random

# Debug: Confirm script is loaded
print("animation.py loaded")

# Constants
xmlns = "http://www.w3.org/2000/svg"
xlinkns = "http://www.w3.org/1999/xlink"
N = 40

# Access SVG element
screen = document["screen"]
if screen is None:
    print("Error: SVG element with id='screen' not found")
else:
    print("SVG element found:", screen)

# Global variables
width = window.innerWidth
height = window.innerHeight
elems = [{"use": None, "x": width / 2, "y": 0} for _ in range(N)]
pointer = {"x": width / 2, "y": height / 2}
radm = min(pointer["x"], pointer["y"]) - 20
frm = random.random()
rad = 0

# Event handlers
def on_pointermove(evt):
    global rad
    pointer["x"] = evt.clientX
    pointer["y"] = evt.clientY
    rad = 0
    print("Pointer moved:", pointer["x"], pointer["y"])  # Debug

def on_resize(evt):
    global width, height
    width = window.innerWidth
    height = window.innerHeight
    print("Window resized:", width, height)  # Debug

# Bind events
try:
    window.bind("pointermove", on_pointermove)
    window.bind("resize", on_resize)
    print("Event handlers bound")
except Exception as e:
    print("Error binding events:", str(e))

# Helper function to prepend SVG elements
def prepend(use_id, i):
    try:
        if screen is None:
            print(f"Error: Cannot prepend {use_id} at index {i}, screen is None")
            return
        elem = document.createElementNS(xmlns, "use")
        href = "#" + use_id
        elem.setAttributeNS(xlinkns, "xlink:href", href)
        screen <= elem  # Brython's append to DOM
        elems[i]["use"] = elem
        print(f"Prepended element {i}: {use_id}")
    except Exception as e:
        print(f"Error in prepend for {use_id} at index {i}:", str(e))

# Initialize SVG elements
try:
    for i in range(1, N):
        if i == 1:
            prepend("Cabeza", i)
        elif i in (8, 14):
            prepend("Aletas", i)
        else:
            prepend("Espina", i)
except Exception as e:
    print("Error initializing SVG elements:", str(e))

# Animation loop
def run(timestamp=None):
    try:
        print("Animation loop running")  # Debug
        global frm, rad
        e = elems[0]
        ax = (math.cos(3 * frm) * rad * width) / height
        ay = (math.sin(4 * frm) * rad * height) / width
        e["x"] += (ax + pointer["x"] - e["x"]) / 10
        e["y"] += (ay + pointer["y"] - e["y"]) / 10

        for i in range(1, N):
            e = elems[i]
            ep = elems[i - 1]
            a = math.atan2(e["y"] - ep["y"], e["x"] - ep["x"])
            e["x"] += (ep["x"] - e["x"] + (math.cos(a) * (100 - i)) / 5) / 4
            e["y"] += (ep["y"] - e["y"] + (math.sin(a) * (100 - i)) / 5) / 4
            s = (162 + 4 * (1 - i)) / 50
            transform = (
                f"translate({(ep['x'] + e['x']) / 2},{(ep['y'] + e['y']) / 2}) "
                f"rotate({(180 / math.pi) * a}) "
                f"translate(0,0) "
                f"scale({s},{s})"
            )
            if e["use"] is not None:
                e["use"].setAttribute("transform", transform)
            else:
                print(f"Warning: use element is None at index {i}")

        if rad < radm:
            rad += 1
        frm += 0.003
        if rad > 60:
            pointer["x"] += (width / 2 - pointer["x"]) * 0.05
            pointer["y"] += (height / 2 - pointer["y"]) * 0.05

        timer.request_animation_frame(run)
    except Exception as e:
        print("Error in animation loop:", str(e))

# Start animation
try:
    run()
except Exception as e:
    print("Error starting animation:", str(e))
