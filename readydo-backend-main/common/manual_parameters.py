from drf_yasg import openapi

CUISINE_TYPES_ARRAY = openapi.Parameter(
    'cuisine_ids', openapi.IN_QUERY,
    description='Example, cuisine_id=1, 2, ..., 14.',
    type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)
)

TASTE_TYPES_ARRAY = openapi.Parameter(
    'taste_ids', openapi.IN_QUERY,
    description='Example, taste_id=1, 2, ..., 4.',
    type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)
)

START_PRICE = openapi.Parameter('start_price', openapi.IN_QUERY, description='start_price', type=openapi.TYPE_INTEGER)

END_PRICE = openapi.Parameter('end_price', openapi.IN_QUERY, description='end_price', type=openapi.TYPE_INTEGER)

BEST_FOODS = openapi.Parameter('chef or meal', openapi.IN_QUERY, description='1=CHEF, 2=MEAL', type=openapi.TYPE_INTEGER)

FOOD_ID = openapi.Parameter('food_id', openapi.IN_QUERY, description='id food', type=openapi.TYPE_INTEGER)

QUERY_BASKET_STATUS = openapi.Parameter('status', openapi.IN_QUERY,
                                        description=' PENDING = 1, SHOPPED = 2, DELIVERED = 3',
                                        type=openapi.TYPE_INTEGER, default=None)

USER_ID = openapi.Parameter('user_id', openapi.IN_QUERY, description='id user', type=openapi.TYPE_INTEGER)

QUERY_FOLLOW_STATUS = openapi.Parameter('status', openapi.IN_QUERY,
                                        description='FOLLOW = 1, UNFOLLOW = 2, IS_FOLLOWING = 3, IS_FOLLOWED_BY = 4',
                                        type=openapi.TYPE_INTEGER, default=None)

FORUM_ID = openapi.Parameter('forum_id', openapi.IN_QUERY, description='id forum', type=openapi.TYPE_INTEGER)
