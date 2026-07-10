"""
### Paint tool for TkEasyGUI

Using original event model
"""
import TkEasyGUI as eg

# canvas
canvas = eg.Canvas(
    size=(100, 100),
    key="-canvas-",
    background_color="black",
    enable_events=True # enable mouse events
)

# window create
window = eg.Window("Paint tool", layout=[
    [eg.Button("Exit"), eg.Button("Clear")],
    [canvas]])
flag_on = False

# event loop
for event, values in window.event_iter():
    x = 0
    y = 0
    #print("#", event, values)
    if event in (None, "Exit"):
        break
    if event == "Clear":
        canvas.clear()
    if event == "-canvas-":
        # check event type
        event = values["event"]
        event_type = values["event_type"]
        if event_type == "mousedown":
            flag_on = True
        elif event_type == "mouseup":
            flag_on = False
        elif event_type == "mousemove":
            canvas.set_cursor("hand2")
            if not flag_on:
                continue
            # get mouse cursor position
            x, y = event.x, event.y
            #最大最小の設定
            # draw white circle
            canvas.create_oval(x, y, x+10, y+10, fill="white", outline="white")
            print("x:",x - 50)
            print("y:",y - 50)
            canvas.clear()
