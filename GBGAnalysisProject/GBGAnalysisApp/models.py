from django.db import models

# Create your models here.

class Mechanics(models.Model):
    name = models.CharField(max_length=255)

class GameBoard(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    year_published = models.IntegerField()
    rank = models.IntegerField()
    bayes_average = models.FloatField()
    average = models.FloatField()
    users_rated = models.IntegerField()
    abstracts_rank = models.IntegerField(default=None, blank=True, null=True)
    cgs_rank = models.IntegerField(default=None, blank=True, null=True)
    childrens_games_rank = models.IntegerField(default=None, blank=True, null=True)
    family_games_rank = models.IntegerField(default=None, blank=True, null=True)
    party_games_rank = models.IntegerField(default=None, blank=True, null=True)
    strategy_games_rank = models.IntegerField(default=None, blank=True, null=True)
    thematic_rank = models.IntegerField(default=None, blank=True, null=True)
    war_games_rank = models.IntegerField(default=None, blank=True, null=True)
        # from API
    min_players = models.IntegerField(default=1, blank=True, null=True)
    max_players = models.IntegerField(default=1, blank=True, null=True)
    min_playtime = models.IntegerField(default=0, blank=True, null=True)
    max_playtime = models.IntegerField(default=0, blank=True, null=True)
    age = models.IntegerField(default=None, blank=True, null=True)
    description = models.TextField(null=True)
    publisher = models.CharField(max_length=255, default=None, blank=True, null=True)
    mechanics = models.ManyToManyField(Mechanics)
    category = models.CharField(max_length=255, default=None, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    gameboard = models.ForeignKey(GameBoard, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default=None, blank=True, null=True)
    rating = models.FloatField(default=None, blank=True, null=True)
    review_text = models.TextField(default=None, blank=True, null=True)