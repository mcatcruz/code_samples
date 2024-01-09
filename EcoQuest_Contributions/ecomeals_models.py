from django.db import models

class EcoMeals(models.Model):
    
    """
    Represents user-recorded eco-friendly meal choices and their impact.

    Attributes:
        user (ForeignKey to Profile): The user who recorded the eco-friendly meal choice.
        eco_breakfast (BooleanField): Indicates if the choice includes an eco-friendly breakfast.
        eco_lunch (BooleanField): Indicates if the choice includes an eco-friendly lunch.
        eco_dinner (BooleanField): Indicates if the choice includes an eco-friendly dinner.
        co2_reduced (FloatField, optional): The amount of CO2 emissions reduced by the meal choice.
            It is nullable because this is not entered by the user.
        ecomeals_points (SmallIntegerField, optional): The eco-meals points earned for making eco-conscious choices.
            It is nullable because this is not entered by the user.
        activity_date (DateField): The date when the meal choice was recorded.
    """

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    eco_breakfast = models.BooleanField(default=False)
    eco_lunch = models.BooleanField(default=False)
    eco_dinner = models.BooleanField(default=False)
    co2_reduced = models.FloatField(null=True, blank=True)
    ecomeals_points = models.SmallIntegerField(null=True, blank=True)
    activity_date = models.DateField(db_index = True, auto_now=True)

    def __str__(self):
        return self.user.username
