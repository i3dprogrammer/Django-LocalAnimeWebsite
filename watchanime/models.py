from django.db import models

class Anime(models.Model):
	title = models.CharField(max_length=140)
	episode = models.IntegerField()
	date = models.DateTimeField(auto_now=True)
	image = models.ImageField(null=True)
	file = models.FileField(null=True)
	quality = models.CharField(max_length=5, null=True)
	
	def __str__(self):
		return self.title
		
class AnimeList(models.Model):
	animeName = models.CharField(max_length=140)
	releaseDay = models.IntegerField()
	releaseTime = models.TimeField()
	currentEpisode = models.IntegerField()
	maxEpisodes = models.IntegerField()

	def __str__(self):
		return self.animeName