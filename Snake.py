from tkinter import *
import random

# Paramètres de base du jeu
largeurjeu = 1400
hauteurjeu = 750
vitesse = 100
tailledelespace = 50
partieducorps = 3
couleurduserpent = "#05ffb3"
couleurdepomme = "#ff0505"
couleurdefond = "#000000"

# Configuration de la pomme
class Pomme:
    def __init__(self, canvas):
        self.canvas = canvas

        self.x = random.randint(0, int(largeurjeu / tailledelespace) - 1) * tailledelespace
        self.y = random.randint(0, int(hauteurjeu / tailledelespace) - 1) * tailledelespace

        self.coordinates = [self.x, self.y]
        self.objet = self.canvas.create_oval(self.x, self.y, self.x + tailledelespace, self.y + tailledelespace,
                                             fill=couleurdepomme, tag="pomme")


class Pomme:
    def __init__(self, canvas):
        self.canvas = canvas

        self.x = random.randint(0, int(largeurjeu / tailledelespace) - 1) * tailledelespace
        self.y = random.randint(0, int(hauteurjeu / tailledelespace) - 1) * tailledelespace

        self.coordinates = [self.x, self.y]
        self.objet = self.canvas.create_oval(self.x, self.y, self.x + tailledelespace, self.y + tailledelespace,
                                             fill=couleurdepomme, tag="pomme")

# Configuration du serpent
class Serpent:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body_size = partieducorps
        self.coordinates = [[0, 0] for _ in range(partieducorps)]
        self.squares = []
        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(x, y, x + tailledelespace, y + tailledelespace,
                                                  fill=couleurduserpent, tag="serpent")
            self.squares.append(square)

# Commande pour nouvelle direction du serpent
def next_turn(serpent, pomme):
    global direction
    x, y = serpent.coordinates[0]

    if direction == "up":
        y -= tailledelespace
    elif direction == "down":
        y += tailledelespace
    elif direction == "left":
        x -= tailledelespace
    elif direction == "right":
        x += tailledelespace

    serpent.coordinates.insert(0, [x, y])

# Plus grande taille lorsque le serpent mange la pomme
    if x == pomme.coordinates[0] and y == pomme.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("pomme")
        pomme = Pomme(canvas)
    else:

        del serpent.coordinates[-1]
        canvas.delete(serpent.squares[-1])
        del serpent.squares[-1]

    square = canvas.create_rectangle(x, y, x + tailledelespace, y + tailledelespace, fill=couleurduserpent)
    serpent.squares.insert(0, square)

    if check_collision(serpent):
        game_over()
    else:
        window.after(vitesse, next_turn, serpent, pomme)

# Changer de direction
def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

# Collision pour le game over
def check_collision(serpent):
    x, y = serpent.coordinates[0]

    if x < 0 or x >= largeurjeu or y < 0 or y >= hauteurjeu:
        print("GAME OVER")
        return True

    for partieducorps in serpent.coordinates[1:]:
        if x == partieducorps[0] and y == partieducorps[1]:
            print("GAME OVER")
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70), text="GAME OVER", fill="red")

window = Tk()
window.title("Snake de Maxou")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=couleurdefond, height=hauteurjeu, width=largeurjeu)
canvas.pack()

# Pour que la page ouvre au milieu de l'écran
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

serpent = Serpent(canvas)
pomme = Pomme(canvas)

next_turn(serpent, pomme)

window.mainloop()
