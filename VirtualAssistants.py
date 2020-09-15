import os

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from forms import AddVirtualAssistant, UpdateVirtualAssistant

from flask_seeder import FlaskSeeder

from flask_caching import Cache

from flask_uploads import UploadSet, IMAGES, configure_uploads
from PIL import Image
from werkzeug.utils import secure_filename

from flask_migrate import Migrate

import requests
import json
import urllib.request


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))


app = Flask(__name__)


photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
configure_uploads(app, photos)

config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app.config["SECRET_KEY"] = "thisissecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_mapping(config)


db = SQLAlchemy(app)


db.init_app(app)
seeder = FlaskSeeder()
seeder.init_app(app, db)

cache = Cache(app)

migrate = Migrate(app, db)

class VirtualAssistant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))#added as a test for migrations check
    last_name = db.Column(db.String(30))
    job = db.Column(db.String(30))
    image_filename = db.Column(db.String)
    image_url = db.Column(db.String)

    def __repr__(self, name, last_name, job, image_filename, image_url):
        self.name = name
        self.last_name = last_name
        self.job = job
        self.image_filename
        self.image_url



def resize_photo(path):
    thumb_size = 100, 100
    thumbnail = Image.open(path)
    thumbnail.thumbnail(thumb_size, Image.ANTIALIAS)
    thumbnail.save(path)

@cache.cached(timeout=300, key_prefix="json_data")
def cache_json_data():
    url = "http://api.dataatwork.org/v1/jobs"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data


@app.route("/", methods=["GET", "POST"])
def add_virtual_assistant():
    cached_data = cache_json_data()
    virtual_assistants = VirtualAssistant.query.all()
    form = AddVirtualAssistant()
    form.job.choices = list(enumerate([i["title"] for i in cached_data if "title" in i], 1))
    job_title = dict(form.job.choices).get(form.job.data)

    if request.method == "POST":
         if form.validate_on_submit():
            photo = request.files["photo"]
            filename = photos.save(form.photo.data)
            url = photos.url(filename)
            path = "C:\\Users\\Luiza\\VirtualAssistants\\static\\img\\" + filename
            resize_photo(path)
            new_virtual_assistant = VirtualAssistant(name=form.name.data, last_name= form.last_name.data, job=job_title, image_filename=filename, image_url=url)
            db.session.add(new_virtual_assistant)
            db.session.commit()
            flash("new virtual assistant has been added")
            return redirect("/")
         else:
            print(form.errors.items())
            return "something is wrong"


    return render_template("AddVirtualAssistant.html", form=form, virtual_assistants=virtual_assistants)


@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update_virtual_assistant(id):
    cached_data = cache_json_data()
    updated_virtual_assistant = VirtualAssistant.query.get_or_404(id)
    form = UpdateVirtualAssistant(obj=updated_virtual_assistant)
    form.job.choices = list(enumerate([i["title"] for i in cached_data if "title" in i], 1))
    job_title = dict(form.job.choices).get(form.job.data)
    if request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(updated_virtual_assistant)
            if "photo" in request.files:
                photo = request.files["photo"]
                filename = photos.save(form.photo.data)
                url = photos.url(filename)
                path = "C:\\Users\\Luiza\\VirtualAssistants\\static\\img\\" + filename
                resize_photo(path)
                updated_virtual_assistant.image_url = url
                updated_virtual_assistant.image_filename = filename
                updated_virtual_assistant.job = job_title
            db.session.commit()
            flash("the virtual assistant has been updated")
            return redirect("/")
        else:
            print(form.errors.items())
            return "something is wrong"
    return render_template("UpdateVirtualAssistant.html", updated_virtual_assistant=updated_virtual_assistant, form=form)

@app.route("/delete/<int:id>/", methods=["GET"])
def delete_virtual_assistant(id):
    deleted_assistant = VirtualAssistant.query.get_or_404(id)
    db.session.delete(deleted_assistant)
    db.session.commit()
    flash("the virtual assistant has been deleted")
    return redirect("/")




if __name__ == "__main__":
    app.run(debug=True)