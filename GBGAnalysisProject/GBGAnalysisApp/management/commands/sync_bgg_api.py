import os
import csv
import requests as req
import pandas as pd
import time
from django.core.management.base import BaseCommand
from GBGAnalysisApp.models import GameBoard

def get_objects_in_chunks(chunk_limit=None, chunk_size: int = 500):
    queryset = GameBoard.objects.all()
    for start in range(0, queryset.count(), chunk_size):
        yield queryset[start:start + chunk_size]
        if chunk_limit != None and chunk_limit - 1 <= start / chunk_size:
            return
    

class Command(BaseCommand):
    # the api call function
    def get_and_add_game_info(self, ids):
        xml_data = req.get('https://boardgamegeek.com/xmlapi/boardgame/' + ids)
        current = time.time()
        if xml_data.status_code != 200:
            self.stdout.write(self.style.ERROR(xml_data.status_code))
        df = pd.read_xml(xml_data.content)
        for i in range(len(df)):
            row = df.iloc[i]
            GameBoard.objects.filter(id=row['objectid']).update(
                min_players=row['minplayers'],
                max_players=row['maxplayers'],
                min_playtime=row['minplaytime'],
                max_playtime=row['maxplaytime'],
                age=row['age'],
                description=row['description'],
                publisher=row['boardgamepublisher']
            )
        return current
    
    def update_percent(self, obj_count, current):
        self.stdout.write(f'{current}/{obj_count} | {current/obj_count * 100}%')

    help = 'Import data from Django API. WARNING: takes several hours'

    def handle(self, *args, **kwargs):
        start_time = 100
        chunk_limit = 5         # change chunk limit here
        chunk_size = 500
        objects_count = GameBoard.objects.all().count()
        if chunk_limit is not None:
            objects_count = chunk_limit * chunk_size
        i = 0
        self.update_percent(objects_count, i * chunk_size )
        for chunk in get_objects_in_chunks(chunk_limit, chunk_size):
            ids = ''
            i += 1
            for entry in chunk:
                ids += str(entry.id) + ','
            ids = ids[:-1]
            while time.time() - start_time <= 2:
                pass
            start_time = self.get_and_add_game_info(ids)
            self.update_percent(objects_count, i * chunk_size )


        self.stdout.write(self.style.SUCCESS('Successfully imported data from API'))
