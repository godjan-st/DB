from os import listdir
from os.path import isfile, join
from random import randint
from django.conf import settings
from django.apps import apps

def rnd_avatar(path):
	avatar_path = join(settings.STATIC_PATH, path)
	pictures = [f for f in listdir(avatar_path) if isfile(join(avatar_path, f))]
	key = randint(0, (len(pictures)-1))
	avatar = join('/profile_images/', pictures[key])
	return avatar
	
# def rnd_slurl(model_name):
	# key = randint(0, 999)
	# model = apps.get_model("rango", model_name)
	# for f in model.objects.all():
		# if key == f.slurl:
			# key = randint(0, 999)
			# f = model.objects.get().first()
	# return str(key)