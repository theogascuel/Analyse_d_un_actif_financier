# Projet 1
## Introduction provisoire
La bourse, et plus généralement les marchés financiers, sont caractérisés par une incertitude permanente, rendant la compréhension et la mesure du risque centrales en finance. Dans la finance moderne, l'analyse des rendements d'actifs repose sur certaines hypothèses simplificatrices, comme la normalité des rendements ou la constance de la volatilité, qui permettent de créer des modèles, comme celui de Black-Scholes-Merton.
L'objectif de ce projet est d'étudier empiriquement les rendements de l'ETF Amundi PEA MSCI Europe, qui réplique un indice d'actions européen. Le choix d'un ETF permet de limiter la volatilité, ce qui est intéressant pour cette étude. J'ai personnellement opté pour cet ETF car c'a été mon premier investissement en bourse.
A partir de données de prix journaliers, nous construirons les rendements de l'ETF et étudierons la normalité des rendements, l'évolution de la volatilité dans le temps, et l'impact de ces caractéristiques sur l'estimation du risque.
Ce projet a pour but de lier modèles financiers et observations, tout en relevant les limites des hypothèses et les enjeux de la modélisation du risque sur les marchés financiers.
## Fonctionnalités 
- Affichage du prix ajusté de l'ETF
- Calcul et affichage du rendement simple et du rendement simple cumulé
- Calcul et affichage du rendement logarithmique et rendement logarithmique cumulé
- Comparaison, test et affichage d'un histogramme pour savoir si les valeurs suivent une loi normale de répartission, avec superposition de la loi normale pour faciliter la comparaison visuelle
- Calcul et affichage de la volatilité historique et glissante sur 20 et 60 jours
- Calcul de la VaR historique et paramétrique/normale
## Installation et Prérequis
### Prérequis
- Python 3.8 ou supérieur
- Les bibliothèques Python suivantes:
    - pandas
    - numpy
    - matplotlib
    - scipy
### Installation des dépendances 
Installer les dépendances avec: 
```bash
pip install -r bibliothèques.txt
