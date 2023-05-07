from ratings.models import RatingChoice


def ratings_choice(request):
    return {"ratings_choice": RatingChoice.values}
