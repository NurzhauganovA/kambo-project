from auth_user.models import User
from foods.models import EstimationTypes, Estimation, Food


def recalculate_grade(type, value_id):
    if type == 1:
        chef = Estimation.objects.filter(type=EstimationTypes.CHEF, value_id=value_id)

        grade = sum(value.grade for value in chef) / chef.count()
        User.objects.filter(id=value_id).update(grade=grade)
        return

    food = Estimation.objects.filter(type=EstimationTypes.FOOD, value_id=value_id)
    grade = sum(value.grade for value in food) / food.count()
    Food.objects.filter(id=value_id).update(grade=grade)
