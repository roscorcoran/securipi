#!/usr/bin/python
import peewee
from peewee import *

db = MySQLDatabase('securipi', user='root',passwd='Blaz1ng')

# create a base model class that our application's models will extend
class BaseModel(peewee.Model):
	class Meta:
		database = db

class Image(BaseModel):
	path = peewee.TextField()
	ts = peewee.DateTimeField(default=peewee.datetime.datetime.now)
	uploaded = BooleanField(default=False)

db.connect()

# create the tables
Image.create_table(True)

image = Image.create(path='bla.jpg', uploaded=False)

image.save();

sq = Image.select().where(Image.uploaded == False)
qr = sq.execute()

for i in qr:
	print("Image {} is uploaded {}".format(i.path, i.uploaded))


