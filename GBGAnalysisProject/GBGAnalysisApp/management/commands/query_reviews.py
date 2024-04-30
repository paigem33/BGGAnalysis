import os
import csv
from django.core.management.base import BaseCommand
from GBGAnalysisApp.models import Review 
from django.db.models import Avg, Count


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        # how many countries have written reviews
        # what country tends to leave the highest reviews
        # what country tends to leave the worst reviews
        # what is the average number of reviews by user 

        # reviews follow this structure database: 
            # id = models.AutoField(primary_key=True)
            # gameboard = models.ForeignKey(GameBoard, on_delete=models.CASCADE)
            # username = models.CharField(max_length=255)
            # country = models.CharField(max_length=255, default=None, blank=True, null=True)
            # rating = models.FloatField(default=None, blank=True, null=True)
            # review_text = models.TextField(default=None, blank=True, null=True)

        # how many countries have written reviews
        distinct_countries = Review.objects.exclude(country=None).values_list('country', flat=True).distinct().count()
        self.stdout.write(self.style.SUCCESS("Number of Countries that have written reviews: " + str(distinct_countries)))

        # what country tends to leave the highest reviews
        highest_avg_rating_country = Review.objects.exclude(country=None).values('country').annotate(avg_rating=Avg('rating')).order_by('-avg_rating').first()
        self.stdout.write(self.style.SUCCESS(f"Highest average rating is from {highest_avg_rating_country['country']}: {highest_avg_rating_country['avg_rating']}")) # has one review

        # what country (with at least 10000 reviews) tends to leave the highest reviews
        countries_with_10000_reviews = Review.objects.exclude(country=None).values('country').annotate(review_count=Count('id')).filter(review_count__gte=10000)
        highest_avg_rating_country = countries_with_10000_reviews.annotate(avg_rating=Avg('rating')).order_by('-avg_rating').first()
        self.stdout.write(self.style.SUCCESS(f"Highest average rating is from {highest_avg_rating_country['country']}: {highest_avg_rating_country['avg_rating']}"))

        # what country tends to leave the worst reviews
        lowest_avg_rating_country = Review.objects.exclude(country=None).values('country').annotate(avg_rating=Avg('rating')).order_by('avg_rating').first()
        self.stdout.write(self.style.SUCCESS(f"Lowest average rating is from {lowest_avg_rating_country['country']}: {lowest_avg_rating_country['avg_rating']}")) # has three reviews

        # what country (with at least 10000 reviews) tends to leave the highest reviews
        highest_avg_rating_country = countries_with_10000_reviews.annotate(avg_rating=Avg('rating')).order_by('avg_rating').first()
        self.stdout.write(self.style.SUCCESS(f"Lowest average rating is from {highest_avg_rating_country['country']}: {highest_avg_rating_country['avg_rating']}"))

        # what is the average number of reviews by user 
        average_reviews_per_user = Review.objects.values('username').annotate(total_reviews=Count('id')).aggregate(avg_reviews=Avg('total_reviews'))
        self.stdout.write(self.style.SUCCESS("Average reviews per user: " + str(average_reviews_per_user['avg_reviews'])))

        # user with the most reviews, username and number of reviews
        user_with_most_reviews = Review.objects.values('username').annotate(num_reviews=Count('id')).order_by('-num_reviews').first()
        username = user_with_most_reviews['username']
        num_reviews = user_with_most_reviews['num_reviews']
        self.stdout.write(self.style.SUCCESS(f"User with the most reviews: {username}, Number of reviews: {num_reviews}"))

        # total reviews by country
        reviews_by_country = Review.objects.values('country').annotate(num_reviews=Count('id'))
        reviews_by_country = list(reviews_by_country)
        reviews_by_country = sorted(reviews_by_country, key=lambda x: x['num_reviews'], reverse=True)
        for data in reviews_by_country:
            country = data['country'] if data['country'] else 'No Country'
            num_reviews = data['num_reviews']
            self.stdout.write(self.style.SUCCESS(f"Country: {country}, Number of Reviews: {num_reviews}"))





