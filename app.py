from flask_cors import CORS
from flask import Flask,render_template,request,jsonify
import pickle
import numpy as np
import pandas 


popularity_df=pickle.load(open('popularity_df.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
scores = pickle.load(open('scores.pkl','rb'))
old_books = pandas.read_pickle('old_books1.pkl')


app = Flask(__name__)
cors = CORS(app,resources={r'/*':{'origin':'*'}})


@app.route('/')
def index_ui():
    return render_template('index.html')




@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    idx = np.where(pt.index==user_input)[0][0]
    items = sorted(list(enumerate(scores[idx])),key = lambda x:x[1],reverse=True)[1:9]
    data=[]
    
    for i in items:            
        item=[]
        temp = books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))       
        item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return render_template('index.html',data=data)

@app.route('/top')
def top_ui():
    return render_template('top50.html',
                           book_name = list(popularity_df['Book-Title'].values),
                           author=list(popularity_df['Book-Author'].values),
                           image=list(popularity_df['Image-URL-M'].values),
                           no_ratings=list(popularity_df['num_ratings'].values),
                           rating=list(format(i,".2f") for i in popularity_df['avg_rating'].values)
                           )


@app.route('/classics')
def classics():
    return render_template('classics.html',
                            book_name = list(old_books['Book-Title'].values),
                           author=list(old_books['Book-Author'].values),
                           image=list(old_books['Image-URL-M'].values),
                           no_ratings=list(old_books['num_ratings'].values),
                           rating=list(format(i,".2f") for i in old_books['avg_rating'].values))
    
    
@app.route('/top50_api')
def top50_api():
    data =  [
                           list(popularity_df['Book-Title'].values),
                           list(popularity_df['Book-Author'].values),
                           list(popularity_df['Image-URL-M'].values),
                           list(popularity_df['num_ratings'].values),
                           list(format(i,".2f") for i in popularity_df['avg_rating'].values)
    ]
    res = []
    for i in range(50):
        res.append({'Book-title':str(data[0][i]),
                    'Book-author':str(data[1][i]),
                    'Image-URL-M':str(data[2][i]),
                    'num_ratings':str(data[3][i]),
                    'avg_ratings':str(data[4][i]),
                    })
    return jsonify(res),200

@app.route('/reccomended_books_10',methods=['post'])
def reccomended_books_10():
    
    
    return request.json,200
    return jsonify({'msg':"hi"}),200


if __name__ == '__main__':
    app.run(debug=True)