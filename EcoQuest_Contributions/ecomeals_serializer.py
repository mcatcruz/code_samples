from rest_framework import serializers
from .ecomeals_models import EcoMeals

class EcoMealsSerializer(serializers.ModelSerializer):
    """
    Serializer for the EcoMeals model, providing string representation of meal choices.

    Attributes:
        meal_type (SerializerMethodField): A dynamically computed field representing the meal type.

    Meta:
        model (EcoMeals): The model class to be serialized.
        fields (list or '__all__'): The fields to be included in the serialized representation.

    Methods:
        get_meal_type(instance): Returns string representing meal type based on boolean value of eco_breakfast, eco_lunch, and eco_dinner.
    
    """
    
    meal_type = serializers.SerializerMethodField()

    def get_meal_type(self, instance):
        if instance.eco_breakfast:
            return "Breakfast"
        elif instance.eco_lunch:
            return "Lunch"
        elif instance.eco_dinner:
            return "Dinner"
        
    class Meta:
        model = EcoMeals
        fields = "__all__"
