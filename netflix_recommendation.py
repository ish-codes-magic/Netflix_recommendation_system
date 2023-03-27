'''Import basic modules.'''
import pandas as pd
import numpy as np


'''Customize visualization
Seaborn and matplotlib visualization.'''
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

netflix_path = "netflix.csv"


df = pd.read_csv(netflix_path)

df['Genres'] = df['listed_in'].str.extract('([A-Z]\w{2,})', expand=True)

df["date_added"] = pd.to_datetime(df['date_added'])
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month

df['season_count'] = df.apply(lambda x : x['duration'].split(" ")[0] if "Season" in x['duration'] else "", axis = 1)
df['duration'] = df.apply(lambda x : x['duration'].split(" ")[0] if "Season" not in x['duration'] else "", axis = 1)

features=['Genres','director','cast','description','title']
filters = df[features]

filters['director'] = filters['director'].fillna(filters['director'].mode()[0])
filters['cast'] = filters['cast'].fillna(filters['cast'].mode()[0])

#Cleaning the data by making all the words in lower case.
def clean_data(x):
        return str.lower(x.replace(" ", ""))
    
    
for feature in features:
    filters[feature] = filters[feature].apply(clean_data)
    
def create_soup(x):
    return x['director'] + ' ' + x['cast'] + ' ' +x['Genres']+' '+ x['description']



filters['soup'] = filters.apply(create_soup, axis=1)


count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(filters['soup'])


cosine_sim2 = cosine_similarity(count_matrix, count_matrix)



# Reset index of our main DataFrame and construct reverse mapping as before
filters=filters.reset_index()
indices = pd.Series(filters.index, index=filters['title'])


def netflix_recommendations(title, cosine_sim=cosine_sim2):
    title=title.replace(' ','').lower()
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]
    


    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    
    movie = []
    score = []
    
    number = 0
    for movie_no in movie_indices:
        movie.append(df['title'].loc[movie_no])
        score.append(round((sim_scores[number][1]*100),2))
        number += 1

    # Return the top 10 most similar movies
    return movie, score








        
        
        








