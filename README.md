
# Visualiseur d'Images avec Suppression de Métadonnées

Cette application est un outil permettant de visualiser, sélectionner et supprimer des métadonnées d'images. Les images peuvent être sélectionnées individuellement ou par dossier. Une fois les métadonnées sélectionnées, elles sont supprimées et les images sont sauvegardées dans un dossier avec un nom modifié pour indiquer que les métadonnées ont été supprimées.

## Fonctionnalités

- **Affichage des images** : Visualisez une ou plusieurs images avec un carrousel.
- **Affichage des métadonnées** : Affichez les métadonnées disponibles pour chaque image.
- **Sélection de métadonnées à supprimer** : Utilisez des cases à cocher pour choisir les métadonnées que vous souhaitez supprimer.
- **Suppression de métadonnées** : Supprimez les métadonnées sélectionnées de toutes les images.
- **Sauvegarde en lot** : Sauvegardez toutes les images modifiées dans un dossier sélectionné, avec un nouveau nom au format `nom_image_nometadata.extension`.
- **Barre de progression** : Suivez l'avancement de la suppression et de la sauvegarde des images.

## Installation

1. Clonez ce dépôt ou téléchargez le code source :
   ```bash
   git clone https://github.com/ton-utilisateur/nom-du-repo.git
   cd nom-du-repo
   ```

2. Installez les dépendances nécessaires via `requirements.txt` :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. Lancez l'application en exécutant le fichier Python principal :
   ```bash
   python main.py
   ```

2. **Sélection des images** : 
   - Cliquez sur le bouton "Sélectionner des images" pour choisir une ou plusieurs images depuis votre système de fichiers.
   - Vous pouvez aussi sélectionner un dossier entier contenant des images en cliquant sur "Sélectionner un dossier".

3. **Affichage des métadonnées** : 
   - Une fois l'image chargée, ses métadonnées sont affichées sur la droite, accompagnées de cases à cocher pour chaque métadonnée.

4. **Suppression des métadonnées** :
   - Cochez les métadonnées que vous souhaitez supprimer.
   - Cliquez sur "Supprimer et sauvegarder toutes les images" pour supprimer les métadonnées sélectionnées.
   - L'application vous demandera de choisir un dossier où sauvegarder les images modifiées.

5. **Sauvegarde des images** :
   - Les images sont sauvegardées avec le suffixe `_nometadata` dans le nom du fichier.

6. **Nouvelle sélection** : Après la sauvegarde des images, l'application vous proposera de sélectionner un nouveau dossier ou de nouvelles images à traiter.

## Capture d'écran

_Ajoutez ici des captures d'écran de l'application pour aider les utilisateurs à visualiser le fonctionnement._

## Technologies utilisées

- **Python 3** : Langage de programmation.
- **Tkinter** : Bibliothèque pour la création de l'interface graphique.
- **Pillow (PIL)** : Bibliothèque pour manipuler les images et les métadonnées.

## Améliorations futures

- Support des formats d'image supplémentaires.
- Possibilité de modifier les métadonnées avant la sauvegarde.
- Ajout de raccourcis clavier pour naviguer plus rapidement dans l'interface.

## Contribuer

Les contributions sont les bienvenues ! Pour soumettre une modification :
1. Forkez le projet.
2. Créez une nouvelle branche (ex: `feature/nouvelle-fonctionnalité`).
3. Faites un commit avec vos modifications (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`).
4. Poussez vos modifications (`git push origin feature/nouvelle-fonctionnalité`).
5. Ouvrez une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
