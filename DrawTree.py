import tkinter as tk
import numpy as np

def array_to_tree(market_model):
    tree_data = []
    for layer in range(1,market_model.number_of_layers + 1):
        tree_data.append(
            np.round(
                market_model.tree[market_model.getTreeId(layer, 1) : market_model.getTreeId(layer+1, 1)],
                2))   
    return tree_data

def array_to_exercise_tree(exercise_tree_array, market_model):
    """Konwertuje flat exercise tree array na listę list (tak jak array_to_tree)"""
    exercise_data = []
    for layer in range(1, market_model.number_of_layers + 1):
        exercise_data.append(
            exercise_tree_array[market_model.getTreeId(layer, 1) : market_model.getTreeId(layer+1, 1)]
        )
    return exercise_data

def draw_horizontal_tree(tree_data, type = 'market', Strike = None, exercise_tree_data = None):
    root = tk.Tk()
    root.title("Drzewo Rekombinujące (Poziomo)")
    root.geometry("1200x700")

    outline_color = '#000000'
    base_color = '#7D6C69'
    base_color2 = '#697D6D'

    green = '#75FC91'
    red = '#FC8674'
    
    early_exercise_color = '#FFD700'
    continuation_color = '#87CEEB'

    box_width = 50
    box_height = 24
    col_width = 80
    row_height = 55
    line_padding = 2
    
    num_layers = len(tree_data)
    max_elements = max(len(layer) for layer in tree_data)
    
    required_width = 60 + num_layers * col_width + 60
    required_height = 60 + (max_elements - 1) * row_height + 60
    
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    canvas = tk.Canvas(main_frame, bg="white")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    h_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=canvas.xview)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    v_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
    canvas.configure(scrollregion=(0, 0, required_width, required_height))
    
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_shift_mousewheel(event):
        canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind("<MouseWheel>", _on_mousewheel)
    canvas.bind("<Shift-MouseWheel>", _on_shift_mousewheel)

    for col_idx, column in enumerate(tree_data):
        x = 60 + col_idx * col_width
        
        total_column_height = (len(column) - 1) * row_height
        start_y = 60 + (required_height - 120 - total_column_height) / 2

        for row_idx, value in enumerate(column):
            y = start_y + row_idx * row_height

            if type == 'market':
                if col_idx % 2 == 0:
                    node_color = base_color
                else:
                    node_color = base_color2

            elif type == 'American Call':
                if Strike is None:
                    raise ValueError('to generate plot of this kind please provide Strike parameter')
                
                if exercise_tree_data is not None and col_idx < len(exercise_tree_data) and row_idx < len(exercise_tree_data[col_idx]):
                    is_early_exercise = exercise_tree_data[col_idx][row_idx] == 1
                    if is_early_exercise:
                        node_color = early_exercise_color
                    else:
                        node_color = continuation_color
                else:
                    if value >= Strike:
                        node_color = green
                    else:
                        node_color = red

            elif type == 'American Put':
                if Strike is None:
                    raise ValueError('to generate plot of this kind please provide Strike parameter')
                
                if exercise_tree_data is not None and col_idx < len(exercise_tree_data) and row_idx < len(exercise_tree_data[col_idx]):
                    is_early_exercise = exercise_tree_data[col_idx][row_idx] == 1
                    if is_early_exercise:
                        node_color = early_exercise_color
                    else:
                        node_color = continuation_color
                else:
                    if value <= Strike:
                        node_color = green
                    else:
                        node_color = red

            elif type == 'Euro Call':
                if Strike is None:
                    raise ValueError('to generate plot of this kind please provide Strike parameter')
                if col_idx == len(tree_data) - 1:
                    if value >= Strike:
                        node_color = green
                    else:
                        node_color = red
                else:
                    if col_idx % 2 == 0:
                        node_color = base_color
                    else:
                        node_color = base_color2

            elif type == 'Euro Put':
                if Strike is None:
                    raise ValueError('to generate plot of this kind please provide Strike parameter')
                if col_idx == len(tree_data) - 1:
                    if value <= Strike:
                        node_color = '#24D691'
                    else:
                        node_color = '#814C41'
                else:
                    node_color = "#B5B5B5"

            if col_idx < len(tree_data) - 1:
                next_x = x + col_width
                next_column_elements = len(tree_data[col_idx + 1])
                next_total_height = (next_column_elements - 1) * row_height
                next_start_y = 60 + (required_height - 120 - next_total_height) / 2

                y_child1 = next_start_y + row_idx * row_height
                y_child2 = next_start_y + (row_idx + 1) * row_height

                canvas.create_line(
                    x + (box_width / 2) - line_padding, y,
                    next_x - (box_width / 2) + line_padding, y_child1,
                    fill=outline_color, width=1, smooth=True
                )
                canvas.create_line(
                    x + (box_width / 2) - line_padding, y,
                    next_x - (box_width / 2) + line_padding, y_child2,
                    fill=outline_color, width=1, smooth=True
                )

            canvas.create_rectangle(
                x - (box_width / 2), y - (box_height / 2),
                x + (box_width / 2), y + (box_height / 2),
                fill=node_color, outline=outline_color, width=1
            )

            if type == 'market':
                canvas.create_text(x, y, text=str(value), font=("Arial", 9, "bold"), fill="black")
            elif type in ('American Call', 'Euro Call'):
                canvas.create_text(x, y, text=str(round(max(0, value - Strike), 2)), font=("Arial", 9, "bold"), fill="black")
            elif type in ('American Put', 'Euro Put'):
                canvas.create_text(x, y, text=str(round(max(0, Strike-value),2)), font=("Arial", 9, "bold"), fill="black")

    root.mainloop()
