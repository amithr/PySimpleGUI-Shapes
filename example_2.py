import PySimpleGUI as sg

options_layout = [
        [sg.T('Choose what clicking a figure does', enable_events=True)],
        [sg.R('Draw Rectangles', 1, key='-RECT-', enable_events=True)],
        [sg.R('Erase item', 1, key='-ERASE-', enable_events=True)],
        [sg.R('Move Stuff', 1, True, key='-MOVE-', enable_events=True)]
    ]

layout = [[sg.Graph(
    canvas_size=(400, 400),
    graph_bottom_left=(0, 0),
    graph_top_right=(400, 400),
    key="-GRAPH-",
    enable_events=True,  # mouse click events
    background_color='lightblue',
    drag_submits=True), sg.Col(options_layout)]]

window = sg.Window("Simple Square Movement", layout, finalize=True, margins=(0,0))

is_being_dragged = False
figures_being_dragged = None
mouse_down_point = None
end_of_drag_point = None
most_recently_clicked_point = None
temporary_rect = None
graph = window['-GRAPH-']

while True:
    event, values = window.read()

    if event is None:
        break

    if event == '-MOVE-':
        graph.set_cursor(cursor='fleur')
    elif not event.startswith('-GRAPH-'):
        graph.set_cursor(cursor='left_ptr')

    if event == "-GRAPH-":
        x, y = values["-GRAPH-"]

        if not is_being_dragged:
            mouse_down_point = (x, y)
            most_recently_clicked_point = (x, y)
            is_being_dragged = True
            figures_being_dragged = graph.get_figures_at_location((x,y))
        else:
            end_of_drag_point = (x, y)

        if temporary_rect:
            graph.delete_figure(temporary_rect)
        
        x_diff, y_diff = x - most_recently_clicked_point[0], y - most_recently_clicked_point[1]
        most_recently_clicked_point = (x, y)

        if mouse_down_point and end_of_drag_point:
            if values['-MOVE-']:
                for figure in figures_being_dragged:
                    graph.move_figure(figure, x_diff, y_diff)
                    graph.update()
            elif values['-RECT-']:
                print(mouse_down_point)
                print(end_of_drag_point)
                temporary_rect = graph.draw_rectangle(mouse_down_point, end_of_drag_point,fill_color='green', line_color='red')
            elif values['-ERASE-']:
                 for figure in figures_being_dragged:
                    graph.delete_figure(figure)
    elif event.endswith('+UP'):
        mouse_down_point = None
        end_of_drag_point = None
        is_being_dragged = False
        temporary_rect = None



