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

def draw_horizontal_tree(tree_data, type = 'market', Strike = None):
    root = tk.Tk()
    root.title("Drzewo Rekombinujące (Poziomo)")

    outline_color = '#000000'
    base_color = '#7D6C69'
    base_color2 = '#697D6D'

    green = '#75FC91'
    red = '#FC8674'



    # Szerokie okno, bo drzewo rośnie w prawo
    canvas_width = 900
    canvas_height = 600
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)

    # --- PARAMETRY RYSOWANIA (ZMIENIONE NA PROSTOKĄTY) ---
    box_width = 50  # Szerokość prostokątnego węzła
    box_height = 24  # Wysokość prostokątnego węzła
    col_width = 80  # Odległość pozioma między środkami kolumn (zwiększona dla czytelności)
    row_height = 55  # Odległość pionowa między węzłami w tej samej warstwie
    line_padding = 2

    for col_idx, column in enumerate(tree_data):
        # Obliczamy pozycję X dla całej warstwy (rośnie w prawo)
        x = 60 + col_idx * col_width
        
        # Obliczamy pionowe wyśrodkowanie (start_y) dla tej konkretnej warstwy
        total_column_height = (len(column) - 1) * row_height
        start_y = (canvas_height - total_column_height) / 2

        for row_idx, value in enumerate(column):
            # Dokładna pozycja Y dla tego węzła
            y = start_y + row_idx * row_height

            # --- LOGIKA KOLOROWANIA ---
            # Tutaj możesz wpisać swoje warunki. Na przykład:
            if type == 'market':
                if col_idx % 2 == 0:
                    node_color = base_color
                else:
                    node_color = base_color2

            elif type == 'American Call':
                if Strike is None:
                    raise ValueError('to generate plot of this kind please provide Strike parameter')
                if value >= Strike:
                    node_color = green
                else:
                    node_color = red

            elif type == 'American Put':
                if Strike is None:
                    raise ValueError('to generate plot of this kind please provide Strike parameter')
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

            # Rysujemy linie łączące do NASTĘPNEJ warstwy (jeśli istnieje)
            if col_idx < len(tree_data) - 1:
                next_x = x + col_width
                next_column_elements = len(tree_data[col_idx + 1])
                next_total_height = (next_column_elements - 1) * row_height
                next_start_y = (canvas_height - next_total_height) / 2

                # Węzeł łączy się z dwoma kolejnymi na następnym poziomie
                y_child1 = next_start_y + row_idx * row_height
                y_child2 = next_start_y + (row_idx + 1) * row_height

                # Linie rysujemy przed kółkami, żeby schowały się pod nimi
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

            # Rysujemy koło (węzeł)
            canvas.create_rectangle(
                x - (box_width / 2), y - (box_height / 2),
                x + (box_width / 2), y + (box_height / 2),
                fill=node_color, outline=outline_color, width=1
            )

            # Wpisujemy wartość do środka
            if type == 'market':
                canvas.create_text(x, y, text=str(value), font=("Arial", 9, "bold"), fill="black")
            elif type in ('American Call', 'Euro Call'):
                canvas.create_text(x, y, text=str(round(max(0, value - Strike), 2)), font=("Arial", 9, "bold"), fill="black")
            elif type in ('American Put', 'Euro Put'):
                canvas.create_text(x, y, text=str(round(max(0, Strike-value),2)), font=("Arial", 9, "bold"), fill="black")


    root.mainloop()
