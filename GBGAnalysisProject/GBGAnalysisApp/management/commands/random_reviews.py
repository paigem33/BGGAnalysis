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
        output_csv_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/random_10k_reviews.csv'))

        reviews_df = pd.read_csv(csv_file_path)
        users_df = pd.read_csv(users_csv_file, quotechar='"')

        merged_df = pd.merge(reviews_df, users_df, how='left', left_on='user', right_on='users')

        random_10k_rows = merged_df.sample(n=10000, random_state=42)

        random_10k_rows.to_csv(output_csv_file, index=False)

        self.stdout.write(self.style.SUCCESS("Random 10,000 reviews saved to CSV file!"))