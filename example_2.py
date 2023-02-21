import PySimpleGUI as sg

def main():

    sg.theme('Dark Blue 3')

    col = [[sg.T('Choose what clicking a figure does', enable_events=True)],
           [sg.R('Draw Rectangles', 1, key='-RECT-', enable_events=True)],
           [sg.R('Draw Circle', 1, key='-CIRCLE-', enable_events=True)],
           [sg.R('Draw Line', 1, key='-LINE-', enable_events=True)],
           [sg.R('Draw point', 1,  key='-POINT-', enable_events=True)],
           [sg.R('Erase item', 1, key='-ERASE-', enable_events=True)],
           [sg.R('Erase all', 1, key='-CLEAR-', enable_events=True)],
           [sg.R('Send to back', 1, key='-BACK-', enable_events=True)],
           [sg.R('Bring to front', 1, key='-FRONT-', enable_events=True)],
           [sg.R('Move Everything', 1, key='-MOVEALL-', enable_events=True)],
           [sg.R('Move Stuff', 1, True, key='-MOVE-', enable_events=True)],
           ]

    layout = [[sg.Graph(
        canvas_size=(400, 400),
        graph_bottom_left=(0, 0),
        graph_top_right=(400, 400),
        key="-GRAPH-",
        enable_events=True,  # mouse click events
        background_color='lightblue',
        drag_submits=True), sg.Col(col) ],
        [sg.Text(key='info', size=(60, 1))]]

    window = sg.Window("Drawing and Moving Stuff Around", layout, finalize=True)

    # get the graph element for ease of use later
    graph = window["-GRAPH-"]  # type: sg.Graph
    START = (200, 200)       # We'll assume X and Y are both this value
    SQ_SIZE = 40
    graph.draw_rectangle(START, (START[0]+SQ_SIZE, START[1]+SQ_SIZE), fill_color='black')

    dragging = False
    start_point = end_point = prior_rect = None
    # Right mouse button
    while True:
        event, values = window.read()
        if event is None:
            break  # exit
        if event in ('-MOVE-', '-MOVEALL-'):
            # Shows 4 arrow cursor
            graph.Widget.config(cursor='fleur')
            # graph.set_cursor(cursor='fleur')          # not yet released method... coming soon!
        elif not event.startswith('-GRAPH-'): 
            # Once MOVE event is done, switches cursor back
            # Doesn't apply when mouse is down on GRAPH
            graph.set_cursor(cursor='left_ptr')       # not yet released method... coming soon!
            graph.Widget.config(cursor='left_ptr')
        if event == "-GRAPH-":  # Mouse clicks on Graph Elememt 
            x, y = values["-GRAPH-"]
            if not dragging: # On mouse down (which selects the shape)
                start_point = (x, y)
                dragging = True
                drag_figures = graph.get_figures_at_location((x,y)) # Stores shapes at current mouse location
                lastxy = x, y # current mouse coordinates
            else:
                end_point = (x, y)
            if prior_rect:
                # Clears prior drawing event
                graph.delete_figure(prior_rect)
            delta_x, delta_y = x - lastxy[0], y - lastxy[1] # x and y difference between intended and current coordinates
            lastxy = x,y # intended, soon to be current coordinates
            if None not in (start_point, end_point): # If movement has been initiated on Graph, but not finished
                if values['-MOVE-']:
                    for fig in drag_figures:
                        # Move figure at current location to location indicated by deltas
                        graph.move_figure(fig, delta_x, delta_y)
                        graph.update()
                elif values['-RECT-']:
                    prior_rect = graph.draw_rectangle(start_point, end_point,fill_color='green', line_color='red')
                elif values['-CIRCLE-']:
                    prior_rect = graph.draw_circle(start_point, end_point[0]-start_point[0], fill_color='red', line_color='green')
                elif values['-LINE-']:
                    prior_rect = graph.draw_line(start_point, end_point, width=4)
                elif values['-POINT-']:
                    prior_rect = graph.draw_point(start_point, size=1)
                elif values['-ERASE-']:
                    for figure in drag_figures:
                        graph.delete_figure(figure)
                elif values['-CLEAR-']:
                    graph.erase()
                elif values['-MOVEALL-']:
                    # Move all graph contents by amount of delta
                    graph.move(delta_x, delta_y)
                elif values['-FRONT-']:
                    for fig in drag_figures:
                        graph.bring_figure_to_front(fig)
                elif values['-BACK-']:
                    for fig in drag_figures:
                        graph.send_figure_to_back(fig)
        elif event.endswith('+UP'): # This is what happens on mouse up
            info = window["info"]
            info.update(value=f"grabbed rectangle from {start_point} to {end_point}")
            start_point, end_point = None, None  # enable grabbing a new rect
            dragging = False
            prior_rect = None


    window.close()

main()