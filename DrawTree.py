import tkinter as tk
import numpy as np

def array_to_layers(array, market_model):
    option_value_layers = []
    for layer in range(1,market_model.number_of_layers+1):
        option_value_layers.append(
            np.round(
                array[market_model.getTreeId(layer, 1) : market_model.getTreeId(layer+1, 1)],
                2))   
    return option_value_layers

def draw_horizontal_tree(option_value_layers, exercise_layers, price_layers):
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
    box_height = 40
    col_width = 80
    row_height = 55
    line_padding = 2
    
    num_layers = len(option_value_layers)
    max_elements = max(len(layer) for layer in option_value_layers)
    
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

    for col_idx, column in enumerate(option_value_layers):
        x = 60 + col_idx * col_width
        
        total_column_height = (len(column) - 1) * row_height
        start_y = 60 + (required_height - 120 - total_column_height) / 2

        for row_idx, value in enumerate(column):
            y = start_y + row_idx * row_height

            is_early_exercise = exercise_layers[col_idx][row_idx] == 1
            if is_early_exercise:
                node_color = early_exercise_color
            else:
                node_color = continuation_color
           
            if col_idx < len(option_value_layers) - 1:
                next_x = x + col_width
                next_column_elements = len(option_value_layers[col_idx + 1])
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

            canvas.create_text(x, y, text=str(value) + '\n' + str(price_layers[col_idx][row_idx]), font=("Arial", 9, "bold"), fill="black")
            
    root.mainloop()
