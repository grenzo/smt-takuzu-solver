from z3 import *
import tkinter as tk
import sys

def read_takuzu_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        n = int(lines[0].strip())
        grille = [list(line.strip()) for line in lines[1:]]
        return n, grille

def solve_takuzu(grille):
    n = len(grille)
    # Créer le solver
    solver = Solver()

    # Créer la grille
    cells = [[Int("cell_%s_%s" % (i, j)) for j in range(n)] for i in range(n)]

    # La grille contient des 0 et des 1 uniquement
    for i in range(n):
        for j in range(n):
            if grille[i][j] == '0':
                solver.add(cells[i][j] == 0)
            elif grille[i][j] == '1':
                solver.add(cells[i][j] == 1)
            else:
                solver.add(Or(cells[i][j] == 0, cells[i][j] == 1))
    
    # Chaque ligne et colonne doit avoir un nombre égal de 0 et de 1
    for i in range(n):
        row = [cells[i][j] for j in range(n)]
        col = [cells[j][i] for j in range(n)]
        solver.add(sum(row) == n // 2)
        solver.add(sum(col) == n // 2)

    # Pas plus de deux chiffres identiques côte à côte en ligne ou en colonne
    for i in range(n):
        for j in range(n - 2):
            solver.add(cells[i][j] + cells[i][j+1] + cells[i][j+2] != 0)
            solver.add(cells[j][i] + cells[j+1][i] + cells[j+2][i] != 0)
            solver.add(cells[i][j] + cells[i][j+1] + cells[i][j+2] != 3)
            solver.add(cells[j][i] + cells[j+1][i] + cells[j+2][i] != 3)

    # Aucune ligne ou colonne ne doit être identique
    # Le plus dur a implémenté, nous avons traduit les 
    # lignes et colonnes en nombres binaires pour pouvoir les comparer plus facilement
    r_d = [0 for i in range(n)]
    c_d = [0 for i in range(n)]
    for i in range(n):
        r_d[i] = Sum([cells[i][j] * 2**(n-j-1) for j in range(n)])
        c_d[i] = Sum([cells[j][i] * 2**(n-j-1) for j in range(n)])

    solver.add(Distinct([r_d[i] for i in range(n)]))
    solver.add(Distinct([c_d[i] for i in range(n)]))


    # Vérifier si le problème est satisfaisable
    if solver.check() == sat:
        model = solver.model()
        solution = [[model.evaluate(cells[i][j]).as_long() for j in range(n)] for i in range(n)]
        return solution
    else:
        return None
    
class GrilleTakuzu:
    def __init__(self, master, grille, solution):
        self.master = master
        self.grille = grille
        self.solution = solution
        self.grille_size = len(grille)
        self.cell_size = 70
        self.current_row = 0
        self.current_col = 0

        self.canvas = tk.Canvas(master, width=self.grille_size*self.cell_size, height=self.grille_size*self.cell_size)
        self.canvas.pack()

        self.draw_grille()

    def draw_grille(self):
        for i in range(self.grille_size):
            for j in range(self.grille_size):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                value = self.grille[i][j]
                
                # Dessiner un carré
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")
                
                # Dessiner la valeur à l'intérieur du carré
                self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(value), fill="black")
                
        self.draw_next_cell()

    def draw_next_cell(self):
        self.canvas.config(bg="white")
        if self.current_row < self.grille_size:
            x0 = self.current_col * self.cell_size
            y0 = self.current_row * self.cell_size
            x1 = x0 + self.cell_size
            y1 = y0 + self.cell_size
            value = self.solution[self.current_row][self.current_col] if self.grille[self.current_row][self.current_col] == '.' else self.grille[self.current_row][self.current_col]
            
            # Mise a jour de la valeur dans la case
            self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(value), fill="black")
            
            # Move to the next cell
            self.current_col += 1
            if self.current_col >= self.grille_size:
                self.current_col = 0
                self.current_row += 1
            
            # Programmer le dessin de la prochaine cellule après un délai
            self.master.after(100, self.draw_next_cell)

    def afficher_solution_par_etapes(grille, solution):
        root = tk.Tk()
        root.title("Grille takuzu")

        app = GrilleTakuzu(root, grille, solution)

        root.mainloop()

def main():
    # Vérifier si un nom de fichier a été passé en argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <nom_fichier>")
        return
    
    # Récupérer le nom du fichier d'entrée à partir des arguments de la ligne de commande
    file_path = sys.argv[1]
    
    # Lire la grille Takuzu depuis le fichier d'entrée
    n, grille = read_takuzu_from_file(file_path)

    # Résolution
    solution = solve_takuzu(grille)

    # Construire le nom du fichier de sortie
    output_file_path = file_path.replace(".txt", "_sol.txt")

    # Écrire la solution dans le fichier de sortie
    if solution:
        with open(output_file_path, "w") as output_file:
            for row in solution:
                output_file.write("".join(map(str, row)) + "\n")
        print(f"Solution écrite dans '{output_file_path}'.")
        #GrilleTakuzu.afficher_solution_par_etapes(grille, solution)
    else:
        print("Pas de solution trouvée.")

if __name__ == "__main__":
    main()
