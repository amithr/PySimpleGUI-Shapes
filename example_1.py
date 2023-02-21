import PySimpleGUI as sg


GRAPH_SIZE = (400, 400)
START = (200, 200)       # We'll assume X and Y are both this value
SQ_SIZE = 40                # Both width and height will be this value

layout = [[sg.Graph(
            canvas_size=GRAPH_SIZE, graph_bottom_left=(0, 0), 
            graph_top_right=GRAPH_SIZE,   # Define the graph area
            enable_events=True,    # mouse click events
            drag_submits=True,      # mouse move events
            background_color='lightblue',
            key="-GRAPH-",
            pad=0)]]

window = sg.Window("Simple Square Movement", layout, finalize=True, margins=(0,0))

# draw the square we'll move around
square = window["-GRAPH-"].draw_rectangle(START, (START[0]+SQ_SIZE, START[1]+SQ_SIZE), fill_color='black')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "-GRAPH-":  # if there's a "Graph" event, then it's a mouse movement. Move the square
        x, y = values["-GRAPH-"]        # get mouse position
        window["-GRAPH-"].relocate_figure(square, x - SQ_SIZE // 2, y + SQ_SIZE // 2)   # Move using center of square to mouse pos

window.close()