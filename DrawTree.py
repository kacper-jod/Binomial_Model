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

def draw_horizontal_tree(tree_data):
    root = tk.Tk()
    root.title("Drzewo Rekombinujące (Poziomo)")

    # Szerokie okno, bo drzewo rośnie w prawo
    canvas_width = 900
    canvas_height = 600
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Parametry rysowania
    radius = 18        # promień węzła
    col_width = 50     # odległość pozioma między warstwami (krokami)
    row_height = 55    # odległość pionowa między węzłami w tej samej warstwie

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
            if col_idx % 2 == 0:
                node_color = "#E6E6FA"  # Lawendowy dla parzystych kroków
            else:
                node_color = "#FFE4E1"  # Różany dla nieparzystych kroków
            
            # Wyróżnienie konkretnej wartości (np. 12)
            if value == 12:
                node_color = "#FFD700"  # Złoty
            # ---------------------------

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
                canvas.create_line(x + radius, y, next_x - radius, y_child1, fill="#CBCBCB", width=1.5)
                canvas.create_line(x + radius, y, next_x - radius, y_child2, fill="#CBCBCB", width=1.5)

            # Rysujemy koło (węzeł)
            canvas.create_oval(
                x - radius, y - radius, 
                x + radius, y + radius, 
                fill=node_color, outline="#8B8B8B", width=1.5
            )

            # Wpisujemy wartość do środka
            canvas.create_text(x, y, text=str(value), font=("Arial", 9, "bold"), fill="black")

    root.mainloop()
