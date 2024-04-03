import os
import csv
from django.core.management.base import BaseCommand
from GBGAnalysisApp.models import GameBoard  # Import your Game model

class Command(BaseCommand):
    help = 'Import data from a CSV file and create GameBoard models'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/boardgames_ranks.csv'))
        with open(csv_file_path, 'r') as file: 
            reader = csv.DictReader(file)
            for row in reader:
                for key, value in row.items():
                    if value == '':
                        row[key] = None

                GameBoard.objects.create(
                    name=row['name'],
                    year_published=row['yearpublished'],
                    rank=row['rank'],
                    bayes_average=row['bayesaverage'],
                    average=row['average'],
                    users_rated=row['usersrated'],
                    abstracts_rank=row['abstracts_rank'],
                    cgs_rank=row['cgs_rank'],
                    childrens_games_rank=row['childrensgames_rank'],
                    family_games_rank=row['familygames_rank'],
                    party_games_rank=row['partygames_rank'],
                    strategy_games_rank=row['strategygames_rank'],
                    thematic_rank=row['thematic_rank'],
                    war_games_rank=row['wargames_rank']
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV file'))
