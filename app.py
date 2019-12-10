from flask import Flask, render_template, redirect
from forms import addMovieForm, searchMovieForm
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.secret_key = "secret key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/user-movies"
mongo = PyMongo(app)

@app.route('/')
def userMovies():
    favMovies = mongo.db.userMovies.find()
    return render_template('userMovies.html', favMovies=favMovies)

@app.route('/addMovie', methods=['GET','POST'])
def addMovie():
    form = addMovieForm()

    if form.validate_on_submit():
        form_data = {'_id': form.movieId.data, 
                    'title': form.movieTitle.data, 
                    'genre': form.movieGenre.data, 
                    'rating': form.movieRating.data, 
                    'released': form.movieReleased.data}
        addToDb = mongo.db.userMovies.insert(form_data)
        return redirect('/')
    return render_template('addMovie.html', form=form)

@app.route('/searchMovie', methods=['GET','POST'])
def searchMovie():
    form = searchMovieForm()

    if form.validate_on_submit():
        result = mongo.db.userMovies.find({'title':{'$regex':form.movieTitle.data}})
        return render_template('userMovies.html', favMovies=result)
    return render_template('searchMovie.html', form=form)
    
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')