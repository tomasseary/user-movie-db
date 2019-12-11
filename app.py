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

@app.route('/delete/<id>', methods=['POST'])
def delete_movie(id):
    mongo.db.userMovies.delete_one({'_id': id})
    return redirect('/')


@app.route('/searchMovie', methods=['GET','POST'])
def searchMovie():
    form = searchMovieForm()

    if form.validate_on_submit():
        result = mongo.db.userMovies.find({'title':{'$regex':form.movieTitle.data}})
        return render_template('userMovies.html', favMovies=result)
    return render_template('searchMovie.html', form=form)

@app.route('/watch/<id>', methods=['POST'])
def watched_movie(id):
    mongo.db.userMovies.update({'_id':id},{'$set':{'watched': 'true'}})
    return redirect('/')

@app.route('/unwatch/<id>', methods=['POST'])
def unwatch_movie(id):
    mongo.db.userMovies.update({'_id':id},{'$set':{'watched': 'false'}})
    return redirect('/')
