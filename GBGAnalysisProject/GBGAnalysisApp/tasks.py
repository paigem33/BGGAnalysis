from celery import shared_task
import requests

@shared_task
def process_api_data():
    # Make API call
    response = requests.get('your_api_endpoint')

    # Process data here
    data = response.json()

    # Perform further operations or save data to the database
    # Example: YourModel.objects.create(data=data)