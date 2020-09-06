from flask_seeder import Seeder, Faker, generator
from VirtualAssistants import db

class VirtualAssistant(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    job = db.Column(db.String(30))
    image_filename = db.Column(db.String)
    image_url = db.Column(db.String)

    def __init__(self, id=None, name=None, last_name=None, job=None, image_filename=None, image_url=None):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.job = job
        self.image_filename = image_filename
        self.image_url = image_url

    def __str__(self):
        return "id=%d, name=%s, last_name=%s, job=%s, image_filename=%s, image_url=%s, " % (self.id, self.name, self.last_name, self.job, self.image_filename, self.image_url)

class DemoSeeder(Seeder):

    def run(self):
        faker = Faker(
            cls=VirtualAssistant,
            init={
                "id": generator.Sequence(),
                "name": generator.Name(),
                "last_name": generator.Name(),
                "job": generator.String("(1st pressman|1st Pressman On Web Press|2nd Grade Teacher|2nd pressman|3d animator)"),
                "image_filename": generator.String("[0-9]{1,2}.jpg"),
                "image_url": generator.String("(https://fwcdn.pl/ppo/70/74/57074/449882.2.jpg|https://fwcdn.pl/ppo/01/09/109/449960.2.jpg|https://fwcdn.pl/ppo/03/16/316/449937.2.jpg|https://ssl-gfx.filmweb.pl/ph/06/99/640699/831926_1.2.jpg|https://ssl-gfx.filmweb.pl/ph/97/46/399746/245837_1.2.jpg)"),
            }
        )

        #Create 5 virtul assistants
        for assistant in faker.create(5):
          print("Adding VirtualAssistant: %s" % assistant)
          self.db.session.add(assistant)

        #flask seed run
