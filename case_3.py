import os
from dotenv import load_dotenv

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def connect_to_db():
    
    host = os.getenv("HOST")
    username = os.getenv("USER")
    password = os.getenv("PASSWORD")
    schema = os.getenv("SCHEMA")
    
    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=schema
    )
    
    if connection.is_connected():
        print("Connection to the database was successful!")
        return connection
    else:
        print("Failed to connect to the database.")
        return None
    

if __name__ == '__main__':
    load_dotenv()
    
    connection = connect_to_db()
    
    cursor = connection.cursor(dictionary=True)
    
    query = '''
        SELECT *
        FROM IMDB_movies
    '''
    
    cursor.execute(query)
    
    df = pd.DataFrame(cursor.fetchall())
    
    # Top 10 filmes por receita em milhões
    revenue = df.groupby('Title').sum().sort_values(by='RevenueMillions', ascending=False)['RevenueMillions'].head(10)
    
    # Aqui, foi utilizado apoio do Copilot para a formatação dos plots
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=revenue.values, y=revenue.index, color='skyblue')
    ax.bar_label(ax.containers[0], fmt='%.2f', label_type='edge', fontsize=10)
    plt.title('Top Movies by Revenue')
    plt.xlabel('Revenue (Millions $)')
    plt.ylabel('Movie Title')
    plt.tight_layout()
    plt.show()
    
    # Média ponderada de avaliação por diretor - a função lambda foi feita com apoio do Copilot
    weighted_avg_rating_by_director = df.groupby('Director').apply(lambda x: (x['Rating'] * x['Votes']).sum() / x['Votes'].sum()).sort_values(ascending=False)
    
    # Aqui, foi utilizado apoio do Copilot para a formatação dos plots
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    ax = sns.barplot(x=weighted_avg_rating_by_director.head(10).values, y=weighted_avg_rating_by_director.head(10).index, color='lightgreen')
    ax.bar_label(ax.containers[0], fmt='%.2f', label_type='edge', fontsize=10)
    plt.title('Weighted Average Rating by Director - Top 10')
    plt.xlabel('Weighted Average Rating')
    plt.ylabel('Director')
    plt.subplot(2, 1, 2)
    ax = sns.barplot(x=weighted_avg_rating_by_director.tail(10).values, y=weighted_avg_rating_by_director.tail(10).index, color='salmon')
    ax.bar_label(ax.containers[0], fmt='%.2f', label_type='edge', fontsize=10)
    plt.title('Weighted Average Rating by Director - Bottom 10')
    plt.xlabel('Weighted Average Rating')
    plt.ylabel('Director')
    plt.tight_layout()
    plt.show()
    
    # Receita por gênero
    genres = df['Genre'].str.split(',').explode().unique()
    
    # Essa parte do código foi feita com apoio do Copilot, que sugeriu a criação de um dicionário para armazenar a receita por gênero
    revenue_by_genre = {}
    for genre in genres:
        revenue_by_genre[genre] = df[df['Genre'].str.contains(genre)]['RevenueMillions'].sum()
    
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=sorted(list(revenue_by_genre.values()), reverse=True), y=list(revenue_by_genre.keys()), color='lightcoral')
    ax.bar_label(ax.containers[0], fmt='%.2f', label_type='edge', fontsize=10)
    plt.title('Revenue by Genre')
    plt.xlabel('Revenue (Millions $)')
    plt.ylabel('Genre')
    plt.tight_layout()
    plt.show()
    
    # Metascore médio por ano de lançamento
    avg_metascore_by_year = df.groupby('Year').mean('Metascore')['Metascore']
    
    # Novamente, utilizei apoio do Copilot com os plots, principalmente para os rótulos dos valores.
    plt.figure(figsize=(12, 6))
    ax = sns.lineplot(x=avg_metascore_by_year.index, y=avg_metascore_by_year.values, marker='o', color='purple')
    for i, v in enumerate(avg_metascore_by_year.values):
        ax.text(avg_metascore_by_year.index[i], v + 0.5, f"{v:.2f}", ha='center', fontsize=9)
    plt.title('Average Metascore by Year of Release')
    plt.xlabel('Year of Release')
    plt.ylabel('Average Metascore')
    plt.xticks(avg_metascore_by_year.index, rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()
