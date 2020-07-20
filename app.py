from flask import Flask, request, jsonify, render_template

import pandas as pd
import numpy as np
import sklearn

df = pd.read_csv('mera data.csv')
df['index'] = df['Unnamed: 0']
pd.set_option('max_row', None)
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

feat = ['title', 'genres', 'imdb_rating']
df['comb_feat'] = df['title'] + " " + df['genres']


def get_title_from_index(index):
    return df.loc[df['index']==index ,'title'].iloc[0]


def get_index_from_title(title):
    return df[df.title == title]["Unnamed: 0"].values[0]

# movie_user_like =input("ENTER YOUR FAVOURITE MOVIE")
def rcmd(m):
        #movie_index = df[df.title == m]["Unnamed: 0"].values
        movie_index=df.loc[df['title']==m,'index'].iloc[0]
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(df['comb_feat'])
        cos_sim = cosine_similarity(count_matrix)
        similar_mov = list(enumerate(cos_sim[movie_index]))
        sorted_simliar_mov = sorted(similar_mov, key=lambda x: x[1], reverse=True)
        l=[]
        for movie in sorted_simliar_mov:
              l.append(get_title_from_index(movie[0]))
        return l[1],l[2],l[3],l[4],l[5]






# user_mood= input("Enter your mood")
def mood(user_mood):
    if user_mood == 'sad':
        for each in {'Drama'}:
            sub = each
            df['index'] = df['genres'].str.find(sub)
    if user_mood == "happy":
        for each in ['Action', 'Comedy', 'Musical']:
            sub = each
            df['index'] = df['genres'].str.find(sub)
    if user_mood == 'Excited':
        for each in ['Action', 'Romance']:
            sub = each
            df['index'] = df['genres'].str.find(sub)
    if user_mood == 'Anticipation':
        for each in ['Crime', 'War']:
            sub = each
            df['index'] = df['genres'].str.find(sub)
    if user_mood == 'Anger':
        for each in ['Family', 'Musical', 'Comedy']:
            sub = each
            df['index'] = df['genres'].str.find(sub)
    if user_mood == 'Depressing':
        for each in ['Drama', 'Biography']:
            sub = each
            df['index'] = df['genres'].str.find(sub)
    if user_mood == 'Confusing':
        for each in ['Thriller', 'Fantasy', 'Crime']:
            sub = each
            df['index'] = df['genres'].str.find(sub)
    if user_mood == 'Inspiring':
        for each in ['Biography', 'Documentary', 'Sport', 'War']:
            sub = each
            df['index'] = df['genres'].str.find(sub)
    if user_mood == 'Thrilling':
        for each in ['Horror', 'Mystery']:
            sub = each
            df['index'] = df['genres'].str.find(sub)
    k= list(df[df['index'] >= 0]['title'].unique())
    return k[0],k[1],k[2],k[3],k[4],k[5]
   # feat = df['title'].unique()
   # pd.set_option('max_row', None)
    #print(feat)

    #df.drop_duplicates(subset='title', keep=False)


app = Flask(__name__, template_folder='template')


@app.route("/")
def home():
    return render_template('recommend.html')
@app.route("/recommend",methods=['POST'])
def recommend():
    mv=request.form['mv']
    r=rcmd(mv)
    return render_template('recommend.html',r=r)
@app.route("/moody",methods=['POST'])
def moody():
    moo=request.form['moo']
    k=mood(moo)
    return render_template('recommend.html',k=k)
"""def moody():
    u_mood = request.args.get('mood')
    e= mood(u_mood)
    u_mood = u_mood.upper()
    if type(e)==type('string'):
        return render_template('recommend.html',mood=u_mood)"""

if __name__ == '__main__':
    app.run(debug=True)
