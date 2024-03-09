from flask_cors import CORS
from flask import Flask,render_template,request,jsonify
import pickle
import numpy as np
import pandas 
import json

popularity_df=pickle.load(open('popularity_df.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
scores = pickle.load(open('scores.pkl','rb'))
old_books = pandas.read_pickle('old_books1.pkl')

def top50_api():
    data =  [
                           list(popularity_df['Book-Title'].values),
                           list(popularity_df['Book-Author'].values),
                           list(popularity_df['Image-URL-M'].values),
                           list(popularity_df['num_ratings'].values),
                           list(format(i,".2f") for i in popularity_df['avg_rating'].values)
    ]
    res = []
    for i in range(len(data[0])):
        res.append({'Book-title':str(data[0][i]),
                    'Book-author':str(data[1][i]),
                    'Image-URL-M':str(data[2][i]),
                    'num_ratings':str(data[3][i]),
                    'avg_ratings':str(data[4][i]),
                    })
    print(json.dumps(res))    
top50_api()