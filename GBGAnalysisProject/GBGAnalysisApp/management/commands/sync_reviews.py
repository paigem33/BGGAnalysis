import pandas as pd
import os
import csv
from django.core.management.base import BaseCommand
from GBGAnalysisApp.models import GameBoard 
from GBGAnalysisApp.models import Review

class Command(BaseCommand):
    help = 'Import data from a CSV file and create Review models'

    def handle(self, *args, **kwargs):
    
        csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/bgg-19m-reviews.csv'))
        users_csv_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/users.csv'))

        reviews_df = pd.read_csv(csv_file_path)
        users_df = pd.read_csv(users_csv_file, quotechar='"')
        
        merged_df = pd.merge(reviews_df, users_df, how='left', left_on='user', right_on='users')
        
        for index, row in merged_df.iterrows():
            username = row['user']
            gameboard_id = int(row['ID'])
            rating = float(row['rating'])
            review_text = row['comment'] if pd.notna(row['comment']) else None
            country = row['country'] if pd.notna(row['country']) else None

            try:
                gameboard = GameBoard.objects.get(id=gameboard_id)
            except GameBoard.DoesNotExist:
                print(f"Gameboard with ID {gameboard_id} does not exist. Skipping.")
                continue

            # Create a Review model instance and save it
            review = Review(
                gameboard=gameboard,
                username=username,
                country=country,
                rating=rating,
                review_text=review_text
            )
            review.save()
            if index % 50 == 0:
                self.stdout.write(self.style.SUCCESS(f"{index} reviews saved!"))