# Projet 1
## Introduction
L'objectif de ce projet est d'étudier les rendements de l'ETF Amundi PEA MSCI Europe, qui réplique un indice d'actions européen.
A partir de données de prix journaliers, nous construirons les rendements de l'ETF et étudierons la normalité des rendements, l'évolution de la volatilité dans le temps, puis l'impact de ces caractéristiques sur l'estimation du risque et nous terminerons enfin par une simulation de mouvements browniens. 
Ce projet a pour but de lier modèles financiers et observations, tout en relevant les limites des hypothèses et les enjeux de la modélisation du risque sur les marchés financiers.
## Fonctionnalités du programme Python
- Affichage du prix ajusté de l'ETF
- Calcul et affichage du rendement simple et du rendement simple cumulé
- Calcul et affichage du rendement logarithmique et rendement logarithmique cumulé
- Comparaison, test et affichage d'un histogramme pour savoir si les valeurs suivent une loi normale de répartission, avec superposition de la loi normale pour faciliter la comparaison visuelle
- Calcul et affichage de la volatilité historique et glissante sur 20 et 60 jours
- Calcul de la VaR historique et paramétrique/normale
- Calcul et comparaison des pertes prévues et pertes réelles
- Début de simulation de mouvements browniens
## Installation et Prérequis
### Prérequis
- Python 3.8 à 3.12
- Les bibliothèques Python suivantes:
    - pandas
    - numpy
    - matplotlib
    - scipy
### Installation des dépendances 
Installez les dépendances avec: 
```bash
pip install -r bibliotheques.txt
```
Le projet utilise le fichier CSV suivant contenant l’historique des prix de l’ETF :
``data/Prix_ETF.csv``
## Utilisation
Après avoir installé les bibliothèques nécessaires, exécutez le programme:
```bash
python main.py
```
## Plan du rapport
 - Introduction
 - Données
 - Analyse des prix
 - Analyse des rendements:
     - Les différents rendements
     - Analyse statistique
 - Volatilité
 - Mesure du risque (VaR)
 - Rapide projection vers le mouvement brownien géométrique: 
     - Simulation numérique du mouvement brownien
     - Simulation d'un prix d'actif
 - Discussion
 - Conclusion  

## Quelques graphiques
![Comparaison entre le prix ajusté et les rendements simple/logarithmique](graphiques/prix_vs_rendements.png)
![Histogramme de comparaison entre les rendements logarithmiques et une distribution normale](graphiques/histogramme.png)
![Graphique de cinq simulations de mouvement brownien](graphiques/simul_mvt_brownien.png)

## Résultats / Observations
- Distribution non normale : asymétrie négative et kurtosis élevée, c'est-à-dire une présence de queues épaisses et d'événements extrêmes fréquents.
- Le test de Jarque-Bera rejète l'hypothèse de normalité.
- La volatilité varie dans le temps : sur une fenêtre 20 jours, elle est plus sensible aux variations rapides, et sur une fenêtre de 60 jours, elle capture les tendances à long terme.
- La VaR paramétrique/normale sous-estime légèrement le risque par rapport à la VaR historique, qui reflète mieux les pertes réelles en prenant en compte les queues épaisses.
- La VaR historique est cohérente dans le calcul de pertes.
- La majorité des trajectoires du mouvement brownien oscille autour d'une tendance moyenne, même si certaines réalisent des performances extrêmes
- Les hypothèses classiques (normalité des rendements, volatilité constante) sont simplificatrices.
- Modèles utiles pour la compréhension et la pédagogie, mais insuffisants pour une gestion réaliste du risque.

