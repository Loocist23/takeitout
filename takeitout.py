import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from tkinter import ttk  # Pour la barre de progression

# Variables globales pour stocker l'état du carrousel et des métadonnées
current_image_index = 0
image_paths = []
checkbox_vars = {}  # Dictionnaire pour stocker les états des cases à cocher

# Fonction pour mettre à jour l'affichage de l'image dans le carrousel et ses métadonnées
def update_image_display():
    global current_image_index, image_paths
    if image_paths:
        image_path = image_paths[current_image_index]
        img = Image.open(image_path)
        img.thumbnail((400, 400))  # Redimensionner pour un aperçu
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Prévenir le garbage collector
        image_name_label.config(text=os.path.basename(image_path))
        
        # Afficher les métadonnées avec des cases à cocher
        display_image_metadata(image_path)
        update_buttons()

# Fonction pour afficher les métadonnées d'une image avec des cases à cocher et une barre de défilement
def display_image_metadata(image_path):
    global checkbox_vars
    try:
        img = Image.open(image_path)
        
        # Vider la zone d'affichage des métadonnées
        for widget in metadata_frame.winfo_children():
            widget.destroy()

        checkbox_vars.clear()  # Réinitialiser les variables des cases à cocher

        # Cadre pour les métadonnées avec barre de défilement
        canvas = tk.Canvas(metadata_frame)
        scrollbar = tk.Scrollbar(metadata_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Afficher les métadonnées avec des cases à cocher
        metadata = img.info
        if metadata:
            for key, value in metadata.items():
                var = tk.BooleanVar()  # Créer une variable pour chaque case à cocher
                checkbox_vars[key] = var

                frame = tk.Frame(scrollable_frame)
                frame.pack(anchor='w', pady=2)

                checkbox = tk.Checkbutton(frame, text=key, variable=var)
                checkbox.pack(side=tk.LEFT)

                metadata_value_label = tk.Label(frame, text=str(value), wraplength=300)
                metadata_value_label.pack(side=tk.LEFT, padx=5)
        else:
            label_no_metadata = tk.Label(scrollable_frame, text="Aucune métadonnée PIL trouvée.")
            label_no_metadata.pack()

    except Exception as e:
        for widget in metadata_frame.winfo_children():
            widget.destroy()
        error_label = tk.Label(metadata_frame, text=f"Erreur lors de l'affichage des métadonnées : {e}")
        error_label.pack()

# Fonction pour supprimer les métadonnées sélectionnées et sauvegarder toutes les images
def delete_selected_metadata():
    global image_paths, current_image_index
    if image_paths:
        # Demander un dossier unique pour sauvegarder les images modifiées
        output_folder = filedialog.askdirectory(title="Sélectionner un dossier pour sauvegarder les images modifiées")
        if not output_folder:
            messagebox.showwarning("Annulation", "Aucun dossier sélectionné.")
            return
        
        # Initialiser la barre de progression
        progress_bar["maximum"] = len(image_paths)
        progress_bar["value"] = 0
        app.update_idletasks()  # Rafraîchir l'interface

        # Parcourir toutes les images et supprimer les métadonnées sélectionnées
        for i, image_path in enumerate(image_paths):
            img = Image.open(image_path)
            img_metadata = img.info.copy()  # Copie des métadonnées pour traitement

            # Supprimer les métadonnées sélectionnées
            for key, var in checkbox_vars.items():
                if var.get() and key in img_metadata:
                    del img_metadata[key]

            # Créer un nouveau nom pour l'image
            base_name, ext = os.path.splitext(os.path.basename(image_path))
            new_image_name = f"{base_name}_nometadata{ext}"
            new_image_path = os.path.join(output_folder, new_image_name)

            # Sauvegarder l'image avec les métadonnées modifiées
            img.save(new_image_path, **img_metadata)

            # Mettre à jour la barre de progression
            progress_bar["value"] = i + 1
            app.update_idletasks()  # Rafraîchir l'interface

        messagebox.showinfo("Succès", f"Toutes les images ont été sauvegardées dans {output_folder}.")
        progress_bar["value"] = 0  # Réinitialiser la barre de progression
        
        # Réinitialiser la liste des images et l'interface après la sauvegarde
        reset_application()

# Fonction pour réinitialiser l'application après la sauvegarde
def reset_application():
    global image_paths, current_image_index
    image_paths = []
    current_image_index = 0

    # Vider l'interface des métadonnées et de l'image affichée
    image_label.config(image='')
    image_name_label.config(text="Sélectionnez une image")
    for widget in metadata_frame.winfo_children():
        widget.destroy()

    # Proposer de sélectionner un nouveau dossier ou de nouvelles images
    new_selection = messagebox.askyesno("Nouvelle sélection", "Voulez-vous sélectionner un nouveau dossier ou des images ?")
    if new_selection:
        open_images()

# Fonction pour aller à l'image suivante
def next_image():
    global current_image_index
    if current_image_index < len(image_paths) - 1:
        current_image_index += 1
        update_image_display()

# Fonction pour revenir à l'image précédente
def previous_image():
    global current_image_index
    if current_image_index > 0:
        current_image_index -= 1
        update_image_display()

# Fonction pour mettre à jour l'état des boutons Précédent/Suivant
def update_buttons():
    previous_button.config(state=tk.NORMAL if current_image_index > 0 else tk.DISABLED)
    next_button.config(state=tk.NORMAL if current_image_index < len(image_paths) - 1 else tk.DISABLED)

# Fonction pour ouvrir un fichier ou plusieurs fichiers et mettre à jour le carrousel
def open_images():
    global image_paths, current_image_index
    file_paths = filedialog.askopenfilenames(
        title="Sélectionner une ou plusieurs images",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
    )
    if file_paths:
        image_paths = list(file_paths)
        current_image_index = 0
        update_image_display()

# Fonction pour ouvrir un dossier entier et ajouter toutes les images dans le carrousel
def open_folder():
    global image_paths, current_image_index
    folder_path = filedialog.askdirectory(title="Sélectionner un dossier contenant des images")
    if folder_path:
        image_extensions = (".png", ".jpg", ".jpeg")
        folder_images = []
        
        # Parcourir le dossier pour trouver toutes les images
        for file in os.listdir(folder_path):
            if file.lower().endswith(image_extensions):
                folder_images.append(os.path.join(folder_path, file))
        
        if folder_images:
            image_paths = folder_images
            current_image_index = 0
            update_image_display()
        else:
            messagebox.showwarning("Pas d'images", "Aucune image trouvée dans le dossier sélectionné.")

# Interface graphique principale
app = tk.Tk()
app.title("Visualiseur d'Images avec Suppression de Métadonnées")

# Configuration de la grille
app.geometry("800x600")

# Frame principale pour contenir le carrousel et les métadonnées
main_frame = tk.Frame(app)
main_frame.pack(fill=tk.BOTH, expand=True)

# Section pour afficher l'image
image_frame = tk.Frame(main_frame)
image_frame.pack(side=tk.LEFT, padx=10)

# Label pour afficher l'image
image_label = tk.Label(image_frame)
image_label.pack(pady=20)

# Label pour afficher le nom de l'image
image_name_label = tk.Label(image_frame, text="Sélectionnez une image", font=("Arial", 14))
image_name_label.pack(pady=10)

# Boutons Précédent/Suivant pour naviguer dans le carrousel
previous_button = tk.Button(image_frame, text="Précédent", command=previous_image, state=tk.DISABLED)
previous_button.pack(side=tk.LEFT, padx=10)

next_button = tk.Button(image_frame, text="Suivant", command=next_image, state=tk.DISABLED)
next_button.pack(side=tk.RIGHT, padx=10)

# Section pour afficher les métadonnées avec une barre de défilement
metadata_frame = tk.Frame(main_frame)
metadata_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

# Barre de progression pour afficher l'avancement
progress_bar = ttk.Progressbar(app, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# Bouton pour supprimer les métadonnées sélectionnées et sauvegarder toutes les images
delete_button = tk.Button(app, text="Supprimer et sauvegarder toutes les images", command=delete_selected_metadata)
delete_button.pack(pady=10)

# Bouton pour ouvrir les images
open_file_button = tk.Button(app, text="Sélectionner des images", command=open_images)
open_file_button.pack(pady=10)

# Bouton pour ouvrir un dossier
open_folder_button = tk.Button(app, text="Sélectionner un dossier", command=open_folder)
open_folder_button.pack(pady=10)

# Lancer l'application
app.mainloop()
