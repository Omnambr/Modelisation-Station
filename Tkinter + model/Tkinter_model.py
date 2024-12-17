import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk  # Pour gérer les images
import pandas as pd
import matplotlib.pyplot as plt
import model_calcul

def start_simulation():
    
    t, P_buffer, P_stockage, Puissance_comp = model_calcul.simulation(float(entry1.get()), float(entry2.get()), float(entry3.get()), float(entry4.get())*1e5, float(entry5.get())*1e5, float(entry6.get()), float(entry7.get()), 0.85, 0.79, 0.95, float(entry9.get()), float(entry10.get())*1e5, float(entry11.get())*1e5, float(entry12.get()))

    plt.figure(1) 
    plt.plot(t,P_buffer/1e5, label="Buffer (lim. " + entry5.get() + " bar)")
    plt.plot(t,P_stockage/1e5, label="Stockage (lim. " + entry11.get() + " bar)")
    plt.axhline(float(entry5.get()),linestyle="--",color='r')
    plt.axvline(x=44700,linestyle="--",color='r')
    plt.text(500,78,f"{max(P_buffer/1e5):.2f}"+" bar",color='r')
    plt.xlabel("Temps (s)")
    plt.ylabel("Pression (bar)")
    plt.title("Pression P en bar dans le buffer et le stockage")
    plt.xlim([0,max(t)])
    plt.legend()
    plt.grid()
    
    plt.figure(2) 
    plt.plot(t,Puissance_comp/1000)
    plt.xlabel("Temps (s)")
    plt.ylabel("Puissance (kW)")
    plt.title("Puissance élec du compresseur")
    plt.grid()
    
    plt.show()


# Fonction pour importer un fichier CSV
def import_data():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:  # Vérifie si un fichier a été sélectionné
        try:
            data = pd.read_csv(file_path)
            messagebox.showinfo("Importation réussie", f"Fichier chargé avec succès :\n{file_path}")
            print("Données importées :\n", data.head())  # Affiche les premières lignes dans la console
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier :\n{e}")

# Création de la fenêtre principale
main = tk.Tk()
main.title("Hydrogen refuelling station – V1")
main.geometry("1000x600")
main.configure(bg="white")

#label1 = tk.Label(main, bg = 'White',text="Station hydrogène EIFHYTEC",font=('Times New Roman', 30))
#label1.place(x=10, y=20)

# --------- Logo EIFHYTEC --------- #
try:
    logo_img = Image.open("eifhytec logo.jpg")  # Remplacez par le chemin de votre logo
    logo_img = logo_img.resize((171, 65))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(main, image=logo_photo)
    logo_label.place(x=700, y=20)  # Positionner le logo en haut à droite

except:
    print("Erreur de chargement du logo")
# --------- Logo EIFHYTEC --------- #

# Canvas pour les images
canvas = tk.Canvas(main, bg="white", width=800, height=400, bd=0, highlightthickness=0)
canvas.place(x=50, y=100)

# Chargement des images (remplacez les chemins par vos propres fichiers d'image)
try:
    img_electrolyser = ImageTk.PhotoImage(Image.open("electrolyser.png").resize((100, 100)))
    img_buffer = ImageTk.PhotoImage(Image.open("buffer.png").resize((100, 100)))
    img_compressor = ImageTk.PhotoImage(Image.open("compressor.png").resize((100, 100)))
    img_storage = ImageTk.PhotoImage(Image.open("storage.png").resize((100, 100)))

    # Placement des images sur le Canvas
    canvas.create_image(100, 120, image=img_electrolyser, anchor=tk.CENTER)
    canvas.create_text(100, 180, text="Electrolyser", font=("Arial", 9, "bold"))

    canvas.create_image(300, 140, image=img_buffer, anchor=tk.CENTER)
    canvas.create_text(300, 180, text="Buffer", font=("Arial", 9, "bold"))

    canvas.create_image(500, 120, image=img_compressor, anchor=tk.CENTER)
    canvas.create_text(500, 180, text="Compressor", font=("Arial", 9, "bold"))

    canvas.create_image(700, 140, image=img_storage, anchor=tk.CENTER)
    canvas.create_text(700, 180, text="Storage", font=("Arial", 9, "bold"))

    # Flèches entre les composants
    canvas.create_line(180, 140, 220, 140, arrow=tk.LAST, width=2)  # Electrolyser -> Buffer
    canvas.create_line(380, 140, 420, 140, arrow=tk.LAST, width=2)  # Buffer -> Compressor
    canvas.create_line(580, 140, 620, 140, arrow=tk.LAST, width=2)  # Compressor -> Storage

except Exception as e:
    messagebox.showerror("Erreur", f"Impossible de charger les images :\n{e}")

# Boutons en bas à droite
buttons = [("Import data", 450), ("Start simulation", 490), ("View graphs", 530), ("QUIT", 570)]

for text, y in buttons:
    if text == "QUIT":
        button = ttk.Button(main, text=text, width=15, command=main.destroy)  # Ferme la fenêtre
    elif text == "Start simulation":
        button = ttk.Button(main, text=text, width=15, command=start_simulation)  # Démarre la simulation
    elif text == "Import data":
        button = ttk.Button(main, text=text, width=15, command=import_data)  # Import de fichier CSV
    else:
        button = ttk.Button(main, text=text, width=15)
    button.place(x=900, y=y)

# ------- Electrolyseur ------- #
label1 = ttk.Label(main,text='Débit (kg/s)')
label1.place(x=115, y=300)
entry1 = ttk.Entry(main, width=10)
entry1.place(x=115, y=320)

label1 = ttk.Label(main,text='Température (K)')
label1.place(x=105, y=350)
entry2 = ttk.Entry(main, width=10)
entry2.place(x=115, y=370)
# ------- Electrolyseur ------- #

# ------- Buffer ------- #
label1 = ttk.Label(main,text='Volume (m3)')
label1.place(x=310, y=300)
entry3 = ttk.Entry(main, width=10)
entry3.place(x=318, y=320)

label1 = ttk.Label(main,text='Pression initiale (bar)')
label1.place(x=300, y=350)
entry4 = ttk.Entry(main, width=10)
entry4.place(x=318, y=370)

label1 = ttk.Label(main,text='Pression maximale (bar)')
label1.place(x=290, y=400)
entry5 = ttk.Entry(main, width=10)
entry5.place(x=318, y=420)  

label1 = ttk.Label(main,text='Température (K)')
label1.place(x=310, y=450)
entry6 = ttk.Entry(main, width=10)
entry6.place(x=318, y=470)
# ------- Buffer ------- #

# ------- Compresseur ------- #
label1 = ttk.Label(main,text='Taux de compression')
label1.place(x=490, y=300)
entry7 = ttk.Entry(main, width=10)
entry7.place(x=515, y=320)

label1 = ttk.Label(main,text='Rendement global')
label1.place(x=500, y=350)
entry8 = ttk.Entry(main, width=10)
entry8.place(x=515, y=370)
# ------- Compresseur ------- #

# ------- Stockage ------- #
label1 = ttk.Label(main,text='Volume (m3)')
label1.place(x=710, y=300)
entry9 = ttk.Entry(main, width=10)
entry9.place(x=715, y=320)

label1 = ttk.Label(main,text='Pression initiale (bar)')
label1.place(x=695, y=350)
entry10 = ttk.Entry(main, width=10)
entry10.place(x=715, y=370)

label1 = ttk.Label(main,text='Pression maximale (bar)')
label1.place(x=690, y=400)
entry11 = ttk.Entry(main, width=10)
entry11.place(x=715, y=420)  

label1 = ttk.Label(main,text='Température (K)')
label1.place(x=705, y=450)
entry12 = ttk.Entry(main, width=10)
entry12.place(x=715, y=470)
# ------- Stockage ------- #

main.mainloop()
