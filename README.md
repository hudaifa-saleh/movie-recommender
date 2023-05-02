# movie-recommender

A movie-recommendation engine using Django & a Machine Learning technique called Collaborative Filtering.

# A project like this is really a collection of 3 parts:

  - Web Process: Setup up Django to collect user's interest and provide recommendations once available.
  - Machine Learning Pipeline: Extract data from Django, transform it, and train a Collaborative Filtering model.
  - Worker Process: This is the glue. We'll use Celery to schedule/run the trained model predictions and update data for Django-related user recommendations.
