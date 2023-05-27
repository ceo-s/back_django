from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views as drf_views
from .views import cabinet_views, coaching_views
from .views import diet_views, libs_views

router = SimpleRouter()

# Cabinet urls
router.register(
    r'users', viewset=cabinet_views.TgUserViewSet, basename="user")
router.register(
    r'profiles', viewset=cabinet_views.ProfileCardViewSet, basename="profile")
router.register(r'posts', viewset=cabinet_views.PostViewSet, basename="post")

# Coaching urls
router.register(
    r'clients', viewset=coaching_views.ClientViewSet, basename="client")
router.register(r'clientstats_active',
                viewset=coaching_views.ClientStatsActiveViewSet, basename="clientstats_active")
router.register(r'clientstats_archieved',
                viewset=coaching_views.ClientStatsArchievedViewSet, basename="clientstats_archieved")
router.register(r'client_base_exercises',
                viewset=coaching_views.ClientBaseExercisesViewSet, basename="client_base_exercises")
router.register(
    r'tprograms', viewset=coaching_views.TrainingProgramViewSet, basename="tprogram")
router.register(
    r'tdays', viewset=coaching_views.TrainingDayViewSet, basename="tday")
router.register(r'exercises_amount',
                viewset=coaching_views.ExerciseAmountViewSet, basename="exercise_amount")

# Diet urls
router.register(
    r'dprograms', viewset=diet_views.DietProgramViewSet, basename="dprogram")
router.register(
    r'nutrients', viewset=diet_views.DayNutrientsViewSet, basename="nutrient")
router.register(r'diet_schedules',
                viewset=diet_views.DietScheduleViewSet, basename="diet_schedule")
router.register(r'foods_amount',
                viewset=diet_views.FoodAmountViewSet, basename="food_amount")
router.register(r'supplements_amount',
                viewset=diet_views.SupplementAmountViewSet, basename="supplement_amount")
router.register(r'meals', viewset=diet_views.MealViewSet, basename="meal")
router.register(r'custom_meals',
                viewset=diet_views.CustomMealViewSet, basename="custom_meal")
router.register(
    r'diet_days', viewset=diet_views.DietProgramDayViewSet, basename="diet_day")

# Libs urls
router.register(r'sports', viewset=libs_views.SportViewSet,
                basename="sport")
router.register(
    r'muscles', viewset=libs_views.MuscleGroupViewSet, basename="muscle")
router.register(r'exercises', viewset=libs_views.ExerciseViewSet,
                basename="exercise")
router.register(r'foods', viewset=libs_views.FoodViewSet, basename="food")
router.register(
    r'supplements', viewset=libs_views.SupplementViewSet, basename="supplements")

# views.ProfileCardViewSet.as_view({"get": "retrieve"})
urlpatterns = router.urls
urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include('rest_framework.urls')),
    # path('api-token-auth/', drf_views.obtain_auth_token),
    path('token-auth/', include('djoser.urls'), name="registration"),
    re_path(r'^auth/', include('djoser.urls.authtoken'), name="authorization"),
]
