import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.stats as stats

fichier = "data/Prix_ETF.csv" #Récupération du fichier
df = pd.read_csv(fichier) #Lecture du fichier

df['Date'] = pd.to_datetime(df['Date']) # Conversion des dates de str à date Python
df = df.sort_values('Date') # Tri croissant/ordre chronologique des dates
df = df.set_index('Date') # Transforme 'Date' en index de DataFrame
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



fig, axes = plt.subplots(1, 2, figsize=(10,6))  #Création de deux graphiques côte à côte pour faciliter la comparaison entre le prix et les rendements
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
axes[0].grid(alpha=0.3) # Implémente une grille pour faciliter la lecture des coordonnées d'un point 
axes[0].legend()
axes[0].set_xlim(df.index.min(), df.index.max()) # Limite les valeurs des abscisses pour ne conserver que les valeurs qui nous intérressent
# Graphique des rendements cumulés
axes[1].plot(df.index, df['simple_cumulé'], color='green', label='Simple cumulé') # Tracé du rendement simple cumulé
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
plt.tight_layout()  # Ajuste automatiquement l'espace affiché
plt.show()



df_nouv = df['rendement_log'][1:] # On crée une nouvelle liste de valeurs sans le "None" du départ pour éviter les problèmes dans les calculs qui vont suivre
moyenne = df_nouv.mean() # Calcul de la moyenne
variance = df_nouv.var() # Calcul de la variance
asymetrie = df_nouv.skew() # Calcul de l'asymétrie
queue = df_nouv.kurtosis() # Calcul de la taille et de l'épaisseur des queues 
print(f"Moyenne: {moyenne}") 
print(f"Variance: {variance}")
print(f"Asymétrie: {asymetrie}") # Doit être nulle pour une loi normale
print(f"Queue: {queue}") # Doit être approximativement égale à 3 pour une loi normale 



plt.figure(figsize=(10,6))
plt.hist(df_nouv, bins=50, density=True, alpha=0.6, color='blue') # Création d'un histogramme pour représenter la répartition des valeurs 
mu = df_nouv.mean() # Calcul de la moyenne des rendements logarithmiques
sigma = df_nouv.std() # Calcul de l'écart-type des rendements journaliers, qui correspond à la volatilité journalière 
x = np.linspace(df_nouv.min(), df_nouv.max(), 100) # Positionne 100 valeurs à équidistance les unes des autres entre la valeur minimale et maximale de df_clean (=futur axe des abscisses)
plt.plot(x, stats.norm.pdf(x, mu, sigma), color='red', label='Loi normale') # Trace la courbe d'une loi de distribution normale pour pouvoir comparer avec l'histogramme
plt.title("Histogramme des rendements log")
plt.xlabel("Rendement")
plt.ylabel("Densité")
plt.legend()
plt.show()



jb_test = stats.jarque_bera(df_nouv) # Test de Jarque-Bera pour avoir la p-value (si p-value < 0.05: rejet de l'hypothèse de normalité)
print("Test de Jarque-Bera:", jb_test)



# Volatilité
vol_historique = np.sqrt(variance) # Calcul de la volatilité historique

vol_20j = [] 
for i in range(len(df['rendement_log'])): # Calcul de la volatilité glissante sur 20 jours
    if i < 19:
        vol_20j.append(np.nan) # Les premières valeurs sont ignorées car il faut 20 jours pour calculer la volatilité glissante
    else:
        fenetre = df['rendement_log'].iloc[i-19:i+1] # On récupère les valeurs du rendements sur 20jours
        moyenne = fenetre.mean() # On calcule la moyenne
        variance = ((fenetre - moyenne)**2).sum() / (len(fenetre) - 1) # Puis la variance
        vol_20j.append(variance)
df['vol_20j'] = vol_20j # Ajoute une colonne dans le DataFrame avec les valeurs de la volatilité glissante sur 20 jours

vol_60j = []
for i in range(len(df['rendement_log'])): # Même boucle adaptée au calcul de la volatilité glissante sur 60 jours
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


# Calcul VaR
moyenne2 = df['rendement_log'].mean() # Calcul de la moyenne des rendements logarithmiques
sigma = np.sqrt(df['rendement_log'].var()) # Calcul de l'écart-type 
VaR_normale = stats.norm.ppf(0.05, moyenne2, sigma) # Calcul du 5e percentile avec l'hypothèse d'une distribution normale
print(f"VaR 95% (normale): {VaR_normale}") 
VaR_historique = df['rendement_log'].quantile(0.05) # Calcul du 5e percentile sans hypothèse donc uniquement basé sur l'historique des prix 
print(f"VaR 95% (historique): {VaR_historique}")


# Comparaison entre pertes observées et pertes prévues par la VaR
df['perte'] = -df['rendement_log'] # Signe négatif pour obtenir des pertes de signe positif
df['depassements'] = df['perte'] > abs(VaR_historique) # Ajout nouvelle colonne seulement pour pouvoir faire la somme du nombre de valeur dépassant la valeur de VaR en absolu
nb_dep = df['depassements'].sum() # Calcul du nombre total de dépassements 
N = df['depassements'].count() # Comptage du nombre de valeur non nulles dans la colonne
a = 0.05*N
print(f"Dépassements observés : {nb_dep}")
print(f"Dépassements attendus : {a}")
borne_sup = a+0.1*a # On pose une borne inférieure et supérieure pour pouvoir comparer la valeur attendue et la valeur obtenue
borne_inf = a-0.1*a 
if borne_inf <= nb_dep <= borne_sup: #Test de la cohérence de la VaR 
    print("VaR cohérente")
elif nb_dep < borne_inf:
    print("La VaR sur estime le risque")
else:
    print("La VaR sous-estime le risque")
    
    
# Début de simulation de mouvement brownien
M = 252 # Nombre de pas correspondant aux nombres de jours ouvrés par an en moyenne
nombre_trace = 5 # Nombre de simulations à effectuer
t = np.arange(M+1) # Création d'un vecteur allant de 0 jusqu'à 252
plt.figure(figsize=(10,6)) 
for j in range(nombre_trace):
    dW = np.random.normal(0,1,size=M) # Grâce à la théorie, on sait que dW suit une loi normale centrée réduite
    W = np.zeros(M+1) # Création d'un vecteur contenant 253 zéros
    for i in range(1,M+1):
        W[i] = W[i-1]+dW[i-1] # Calcul de la valeur du mouvement brownien au jour i
    P = np.zeros(M+1) 
    P[0] = df['Price'].iloc[-1] # Assignation à la valeur initiale du dernier prix connu de l'ETF
    for i in range(1,M+1):
        P[i] = P[i-1]*np.exp(moyenne+sigma*dW[i-1]) # Solution de l'équation de Black-Scholes
    plt.plot(t,P)
plt.title("Simulation de plusieurs trajectoires du mouvement brownien")
plt.xlabel("Temps t")
plt.ylabel("W(t)")
plt.grid()
plt.show()

