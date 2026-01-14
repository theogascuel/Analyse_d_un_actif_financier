import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.stats as stats

fichier = "data/Prix_ETF.csv" #Récupération fichier
df = pd.read_csv(fichier) #Lecture du fichier

df['Date'] = pd.to_datetime(df['Date']) #conversion des dates de str à date python
df = df.sort_values('Date') #tri croissant/ordre chronologique des dates
df = df.set_index('Date') #transforme 'Date' en index de DataFrame
df['rendement_simple'] = [None] + [(df.iloc[i]['Price'] - df.iloc[i-1]['Price']) / df.iloc[i-1]['Price'] for i in range(1, len(df))] # Calcul des rendements simples
df['rendement_log'] = [None] + [np.log(df.iloc[i]['Price'] / df.iloc[i-1]['Price']) for i in range(1,len(df))] # Calcul des rendements logarithmiques

def simple_cum(): # Fonction servant à calculer le rendement simple cumulé
    simple_cumule = []
    cumul = 0
    simple_cumule.append(cumul)
    for i in df['rendement_simple'][1:]:
        cumul = (1+cumul)*(1+i)-1
        simple_cumule.append(cumul)
    return simple_cumule
df['simple_cumulé'] = simple_cum() # Ajoute une nouvelle colonne dans mon DataFrame avec les valeurs du rendement simple cumulé

def log_cum(): # Fonction servant à calculer le rendement logarithmique cumulé
    log_cumule = []
    cumul = 0
    log_cumule.append(cumul)
    for i in df['rendement_log'][1:]:
        cumul += i
        log_cumule.append(cumul)
    return log_cumule
df['log_cumulé'] = log_cum() # Ajoute une colonne dans le DataFrame avec les valeurs du rendement logarithmique cumulé



fig, axes = plt.subplots(1, 2, figsize=(10,6))  #Création de deux graphiques côte à côte pour faciliter la comparaison entre prix et rendements
# Graphique du prix
axes[0].plot(df.index, df['Price'], color='blue', label='Prix ajusté') 
axes[0].set_title("Prix ajusté de l'ETF")
axes[0].set_xlabel("Date")
axes[0].set_ylabel("Prix (€)")
formatter = mdates.DateFormatter('%Y-%m') # Sert à formater les données de l'axe des abscisses pour qu'elles restent lisibles
axes[0].xaxis.set_major_formatter(formatter)
decoupage = mdates.MonthLocator(interval=3)
axes[0].xaxis.set_major_locator(decoupage)
axes[0].tick_params(axis='x', rotation=45) # Incline les dates pour garder une échelle correcte sur le graphique tout en restant lisible
axes[0].grid(alpha=0.3) # Implémente une grille pour faciliter la lecture des abscisses ou ordonnées d'un point 
axes[0].legend()
axes[0].set_xlim(df.index.min(), df.index.max()) # Limite les valeurs des abscisses pour ne conserver seulement les valeurs qui nous interressent
# Graphique des rendements cumulés
axes[1].plot(df.index, df['simple_cumulé'], color='green', label='Simple cumulé') # Tracé du rendement simple cmulé
axes[1].plot(df.index, df['log_cumulé'], color='red', linestyle='--', label='Logarithme cumulé') # Tracé du rendement logarithmique cumulé 
axes[1].set_title("Rendements cumulés")
axes[1].set_xlabel("Date")
axes[1].set_ylabel("Rendement cumulé (%)")
axes[1].xaxis.set_major_formatter(formatter)
axes[1].xaxis.set_major_locator(decoupage)
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(alpha=0.3)
axes[1].legend()
axes[1].set_xlim(df.index.min(), df.index.max())
plt.tight_layout()  # Ajuste l'espace affiché
plt.show()



df_clean = df['rendement_log'][1:] # On crée une nouvelle liste de valeur sans le "None" du départ pour éviter les problèmes dans les calculs qui vont suivre
moyenne = df_clean.mean() # Calcul de la moyenne
variance = df_clean.var() # Calcul de la variance
asymetrie = df_clean.skew() # Calcul de la symétrie
queue = df_clean.kurtosis() # Calcul de la taille et épaisseur des queues 
print(f"Moyenne: {moyenne}") 
print(f"Variance: {variance}")
print(f"Asymétrie: {asymetrie}") # Doit être nulle pour une loi normale
print(f"Queue: {queue}") # Doit être approximativement égal à 3 pour loi normale 



plt.figure(figsize=(10,6))
plt.hist(df_clean, bins=50, density=True, alpha=0.6, color='skyblue') # Création d'un histogramme pour représenter la répartition des valeurs 
mu = df_clean.mean() # Calcul de la moyenne des rendements logarithmiques
sigma = df_clean.std() # Calcul de l'écart-type des rendements journaliers qui correspond à la volatilité journalière 
x = np.linspace(df_clean.min(), df_clean.max(), 100) # Positionne 100 valeurs à equidistance les unes des autres entre la valeur minimale et maximale de df_clean (=futur axe des abscisses)
plt.plot(x, stats.norm.pdf(x, mu, sigma), color='red', label='Loi normale') # Trace la courbe d'une loi normale pour pouvoir comparer avec l'histogramme
plt.title("Histogramme des rendements log")
plt.xlabel("Rendement")
plt.ylabel("Densité")
plt.legend()
plt.show()



jb_test = stats.jarque_bera(df_clean) # Test de Jarque-Bera pour avoir la pvalue (si pvalue < 0.05: rejet de l'hypothèse de normalité)
print("Test de Jarque-Bera:", jb_test)



#Volatilité
vol_historique = np.sqrt(variance) # Calcul de la volatilité historique (=écart-type calculé plus haut)

vol_20j = [] 
for i in range(len(df['rendement_log'])): # Calcul de la volatilité glissante sur 20jours
    if i < 19:
        vol_20j.append(np.nan) # Les premières valeurs sont sautées car il faut 20 jours pour calculer la volatilité glissante
    else:
        fenetre = df['rendement_log'].iloc[i-19:i+1] # On récupère les valeurs du rendements sur 20jours
        moyenne = fenetre.mean() # On calcule la moyenne
        variance = ((fenetre - moyenne)**2).sum() / (len(fenetre) - 1) # Puis la variance
        vol_20j.append(variance)
df['vol_20j'] = vol_20j # Ajoute une colonne dans le DataFrame avec les valeurs de la volatilité glissante sur 20jours

vol_60j = []
for i in range(len(df['rendement_log'])): # Même boucle adaptée au calcul de la volatilité glissante sur 60jours
    if i < 59:
        vol_60j.append(np.nan)
    else:
        fenetre = df['rendement_log'].iloc[i-59:i+1]
        moyenne = fenetre.mean()
        variance = ((fenetre - moyenne)**2).sum() / (len(fenetre) - 1)
        vol_60j.append(variance)
df['vol_60j'] = vol_60j

plt.figure(figsize=(10,6))
plt.plot(df.index, np.sqrt(df['vol_20j']), color='red', label='Volatilité glissante sur 20jours') # Trace la volatilité glissante sur 20jours en fonction de la date
plt.plot(df.index, np.sqrt(df['vol_60j']), color='green', label='Volatilité glissante sur 60jours') # Trace la volatilité glissante sur 60jours en fonction de la date
plt.plot(df.index, [vol_historique]*len(df), color='blue', linestyle='--', label='Volatilité historique') # Trace la valeur constante de la volatilité historique
plt.xlabel("Date")
plt.ylabel("volatilité")
formatter = mdates.DateFormatter('%Y-%m')
decoupage = mdates.MonthLocator(interval=3)
plt.gca().xaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_major_locator(decoupage)
plt.tick_params(axis='x', rotation=45)
plt.grid(alpha=0.3)
plt.legend()
plt.xlim(df.index.min(), df.index.max())
plt.show()

#Calcul VaR
moyenne2 = df['rendement_log'].mean() # Calcul de la moyenne des rendements logarithmiques
sigma = np.sqrt(df['rendement_log'].var()) # Calcul de l'écart-type 
VaR_normale = stats.norm.ppf(0.05, moyenne2, sigma) # Calcul du 5e percentile avec l'hypothèse d'une distribution normale
print(f"VaR 95% (normale): {VaR_normale}") 
VaR_historique = df['rendement_log'].quantile(0.05) # Calcul du 5e percentile sans hypothèse donc uniquement basé sur l'historique 
print(f"VaR 95% (historique): {VaR_historique}")
