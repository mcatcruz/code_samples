import math
from .ecomeals_models import EcoMeals
from .ecomeals_serializer import EcoMealsSerializer
from rest_framework import generics
from rest_framework.response import Response


# Pre-determined values of total carbon footprint in g CO2-equivalent
CO2E_PLANTBASED_BREAKFAST_GRAMS= 1100
CO2E_PLANTBASED_LUNCH_GRAMS = 980
CO2E_PLANTBASED_DINNER_GRAMS = 1100

CO2E_MEATBASED_BREAKFAST_GRAMS = 2600
CO2E_MEATBASED_LUNCH_GRAMS = 3800
CO2E_MEATBASED_DINNER_GRAMS = 4800

POINTS_AWARDED_100GCO2 =  50

#=============api/eco-meals==================================
#supports GET and POST for authenticated user.
#for the current user token, return all EcoMeals Activities recorded[GET]
#for the current user, add EcoMeals instance to the database [POST]

class EcoMealsView(generics.ListCreateAPIView):

    """
    API view for retrieving and creating EcoMeals instances.

    Methods:
        get_queryset(): Returns a queryset containing all EcoMeals instances.
        perform_create(serializer): Creates a new EcoMeals instance and computes CO2 emissions reduced and eco-meals points.
        calculate_co2_reduced(user_ecomeals_input): Calculates CO2 emissions reduced based on meal choices.
        calculate_ecomeals_points(user_co2_reduced): Calculates eco-meals points earned based on CO2 reductions.
        update_user_profile(user, user_co2_reduced, user_ecomeals_points): Updates the user's profile with points and CO2 reductions.
    """
    
    serializer_class = EcoMealsSerializer

    def get_queryset(self):
        return EcoMeals.objects.all()

    def perform_create(self, serializer):
        # Saves EcoMeals instance
        user = serializer.validated_data['user']
        eco_breakfast = serializer.validated_data['eco_breakfast']
        eco_lunch = serializer.validated_data['eco_lunch']
        eco_dinner = serializer.validated_data['eco_dinner']
        serializer.save(eco_breakfast=eco_breakfast, eco_lunch=eco_lunch, eco_dinner=eco_dinner)

        co2_reduced = self.calculate_co2_reduced(self.request.data)
        ecomeals_points = self.calculate_ecomeals_points(co2_reduced)
        
        # Update EcoMeals instance with co2_reduced and ecomeals_points results
        eco_meals_instance = serializer.instance
        eco_meals_instance.co2_reduced = co2_reduced
        eco_meals_instance.ecomeals_points = ecomeals_points
        eco_meals_instance.save()

        # Update Profile with points from EcoMeals
        self.update_user_profile(user, co2_reduced, ecomeals_points)


    def calculate_co2_reduced(self, user_ecomeals_input):
        co2_reduced = 0

        if user_ecomeals_input['eco_breakfast'] == True:
            co2_reduced = CO2E_MEATBASED_BREAKFAST_GRAMS - CO2E_PLANTBASED_BREAKFAST_GRAMS
        
        elif user_ecomeals_input['eco_lunch'] == True:
            co2_reduced = CO2E_MEATBASED_LUNCH_GRAMS - CO2E_PLANTBASED_LUNCH_GRAMS

        elif user_ecomeals_input['eco_dinner'] == True:
            co2_reduced = CO2E_MEATBASED_DINNER_GRAMS - CO2E_PLANTBASED_DINNER_GRAMS
        
        return co2_reduced

    def calculate_ecomeals_points(self, user_co2_reduced):
        ecomeals_points = math.floor(user_co2_reduced / 100 * POINTS_AWARDED_100GCO2)

        return ecomeals_points

    def update_user_profile(self, user, user_co2_reduced, user_ecomeals_points):
        profile = Profile.objects.get(username=user)
        profile.total_co2e_reduced += user_co2_reduced
        profile.total_points += user_ecomeals_points
        profile.save()

#=================api/eco-meals/<int:pk>=======================
#supports GET for all EcoMeals associated with the specified primary key

class SingleUserAllEcoMealInstancesView(generics.ListAPIView):
    """
    API view for retrieving all EcoMeals instances recorded by a specific user.

    This view allows users to retrieve a list of all EcoMeals activities recorded by a specific user
    based on their user ID.

    Attributes:
        serializer_class (EcoMealsSerializer): The serializer class for EcoMeals instances.

    Methods:
        get_queryset(): Returns a queryset containing all EcoMeals instances for the specified user.
        list(request, *args, **kwargs): Retrieves and serializes all EcoMeals instances for the user. 
    """
    
    serializer_class = EcoMealsSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        return EcoMeals.objects.filter(user=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True) 

        response_data = {
            'EcoMeals': serializer.data
        }

        return Response(response_data, status=200)
    

