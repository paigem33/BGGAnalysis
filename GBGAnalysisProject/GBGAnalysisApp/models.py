from django.db import models

# Create your models here.

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

    def __str__(self):
        return self.name