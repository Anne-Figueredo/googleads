# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 13:48:32 2024

@author: ericc
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


#import des datas
event = pd.read_csv("C:/Users/ericc/Documents/AF DATA/Datas tests/google analytics/events1.csv")
items = pd.read_csv("C:/Users/ericc/Documents/AF DATA/Datas tests/google analytics/items.csv")
users = pd.read_csv("C:/Users/ericc/Documents/AF DATA/Datas tests/google analytics/users.csv")

##CLEANING EVENT
#suppression des lignes vides pour country
event = event.dropna(subset=['country'])

#changement des types de colonnes
event.user_id = event.user_id.astype(str)
event.item_id = event.item_id.astype(str)
event.ga_session_id = event.ga_session_id.astype(str)
event.date= pd.to_datetime(event.date).dt.date


##CLEANING ITEMS
#changement des types de colonnes
items.id = items.id.astype('str')

#changement du nom de la colonne id
items = items.rename(columns ={'id' : 'item_id'})


##CLEANING USERS
#changement de type de colonne
users.date = pd.to_datetime(users.date).dt.date
users.id = users.id.astype('str')

#changement du nom de colonne
users = users.rename(columns ={'id' : 'user_id'})

print("les colonnes de event sont :", event.columns)
print("les colonnes de items sont :", items.columns)
print("les colonnes de users sont :", users.columns)

##VISUALISATIONS

# acheteurs les plus fidèles
bestfidelity_users = event.groupby('user_id').size().reset_index(name='count')
bestfidelity_users = bestfidelity_users.sort_values(by='count', ascending=False).head(10)

sns.countplot(x='user_id', data=bestfidelity_users)
plt.title('Acheteurs les plus récurrents')

#meilleurs acheteurs
best_users = users.sort_values(by='ltv', ascending=False).head(10)


sns.barplot(x='user_id', y='ltv', data = best_users)
plt.title('Meilleurs acheteurs ltv')


#fusion des data event et items
event_items = event.merge(items[['item_id', 'name', 'brand', 'variant', 'category', 'price_in_usd']], on='item_id', how='inner')
print("les colonnes de event_items sont :", event_items.columns)

#evolution des ventes
daily_sales = event_items.groupby('date')['price_in_usd'].sum().reset_index()
daily_sales['date']= pd.to_datetime(daily_sales['date'])
daily_sales.info(5)


plt.figure(figsize=(10, 6))
sns.lineplot(x=daily_sales['date'], y=daily_sales['price_in_usd'], alpha=0.7)
plt.title('Evolution des ventes')

#evolution aux jours de semaines
daily_sales['weekday'] = daily_sales['date'].dt.day_name()
daily_sales.head()

plt.figure(figsize=(10, 6))
sns.barplot(x=daily_sales['weekday'], y=daily_sales['price_in_usd'])
plt.title('Evolution des ventes en semaine')
plt.show()

#distribution des ventes par 5 meilleurs pays
country_sales = event_items.groupby('country')['price_in_usd'].sum().reset_index()
best_country = country_sales.sort_values(by = "price_in_usd", ascending = False).head(5)
best_country.info()

plt.figure(figsize=(8, 8))
plt.pie(
    best_country['price_in_usd'],  # Les valeurs numériques
    labels=best_country['country'],  # Les noms des pays
    autopct='%1.1f%%',  # Pourcentages
    startangle=140
)

plt.title('Répartition des ventes par 5 meilleurs pays')
plt.tight_layout()
plt.show()

#meilleures marques
brand_sales = event_items.groupby('brand')['price_in_usd'].sum().reset_index()

plt.pie(
        brand_sales['price_in_usd'], 
        labels = brand_sales['brand'],
        autopct='%1.1f%%',  # Pourcentages
        startangle=140
    )

plt.title('Répartition des ventes par marques')
plt.tight_layout()
plt.show()

#meilleures catégories
category_sales = event_items.groupby('category')['price_in_usd'].sum().reset_index()
category = category_sales.sort_values(by = 'price_in_usd', ascending=False).head(5)

plt.pie(category['price_in_usd'], labels = category['category'], autopct = '%1.1f%%', startangle=140)
plt.title('Répartition des 5 meilleures catégories vendues')

#evolution des ventes par categories
daily_sales_category = event_items.groupby(['date', 'category'])['price_in_usd'].sum().reset_index()

# Convertir la colonne `date` en format datetime
daily_sales_category['date'] = pd.to_datetime(daily_sales_category['date'])
daily_sales_category.head()

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=daily_sales_category, 
    x='date', 
    y='price_in_usd', 
    hue='category',  # Différencier les catégories par couleur
    alpha=0.7
)

plt.title('Évolution des ventes par catégories')
plt.xlabel('Date')
plt.ylabel('Montant des ventes (USD)')
plt.xticks(rotation=45)
plt.legend(title='Catégorie')
plt.tight_layout()
plt.show()


