from django.contrib.auth.models import AbstractUser
from django.db import models
from joblib import load
from datetime import datetime
from django.utils import timezone
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    agency = models.CharField(default="")
    phone = models.CharField(max_length=10, default="")
    job_positions = models.CharField(max_length=100, default="")
    employee_id = models.CharField(max_length=100, default="")
    profile_picture = models.ImageField(blank=True, null=True)
    user = models.OneToOneField("coolingapp.CustomUser", on_delete=models.CASCADE)

model_random_forest = load('coolingapp/model_ml/model_random_forest_cooling.pkl')

LINE_CHANNEL_ACCESS_TOKEN = 'xLnD7d+Lc9/Qq0uJoiF7F/rzClvuZIFCcByie0pNd12qzmNPSiv89AiAtEuSB4sLvn4bKRKAlFvEZjCcDcjHJv9nMCa6beIE+Ehzn5A6NGWYmxkRB0KquHfTS2YkLAOqalYDKRGld8JJ5nzpGCMWzQdB04t89/1O/w1cDnyilFU='
LINE_USER_ID = 'U83f4c214d510392261bd36ffe921a611'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

class CoolingForecast(models.Model):
    recorded_at = models.DateTimeField(default=timezone.now)
    InletTemp = models.FloatField()
    OutletTemp = models.FloatField()
    OutdoorWetBulb = models.FloatField()
    OutdoorAirTemp = models.FloatField()
    OutdoorAirHumidity = models.FloatField()
    Kw_cooling = models.FloatField()
    Kw_Chiller = models.FloatField()
    Design_cooling = models.FloatField(null=True, blank=True)
    Diff_Outlet_Wetbulb = models.FloatField(null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True)

    @property
    def converted_InletTemp(self):
        if self.InletTemp < 95:
            return 1
        elif self.InletTemp == 95:
            return 2
        else:
            return 3

    @property
    def converted_OutletTemp(self):
        if self.OutletTemp < 85:
            return 1
        elif self.OutletTemp == 85:
            return 2
        else:
            return 3

    @property
    def converted_OutdoorWetBulb(self):
        if self.OutdoorWetBulb < 78:
            return 1
        elif self.OutdoorWetBulb == 78:
            return 2
        else:
            return 3

    @property
    def converted_OutdoorAirTemp(self):
        if self.OutdoorAirTemp < 80.6:
            return 1
        elif 80.6 <= self.OutdoorAirTemp <= 87.389:
            return 2
        else:
            return 3

    @property
    def converted_OutdoorAirHumidity(self):
        if self.OutdoorAirHumidity < 57.854:
            return 1
        elif 57.854 <= self.OutdoorAirHumidity <= 79.9:
            return 2
        else:
            return 3

    @property
    def converted_Kw_cooling(self):
        if self.Kw_cooling < 20.333:
            return 1
        else:
            return 2

    @property
    def converted_Kw_Chiller(self):
        if self.Kw_Chiller == 0:
            return 0
        elif self.Kw_Chiller <= 1176.038:
            return 1
        else:
            return 2

    @property
    def converted_Design_cooling(self):
        if self.Design_cooling < 7:
            return 1
        elif 7 <= self.Design_cooling < 10:
            return 2
        else:
            return 3

    @property
    def converted_Diff_Outlet_Wetbulb(self):
        if self.Diff_Outlet_Wetbulb < 0:
            return 1
        elif 0 <= self.Diff_Outlet_Wetbulb < 7:
            return 2
        else:
            return 3

    def notify_line(self, message):
        try:
            line_bot_api.push_message(LINE_USER_ID, TextSendMessage(text=message))
        except LineBotApiError as e:
            print(f"Failed to send message: {e}")

    def predict_status(self):
        # Compute Design_cooling and Diff_Outlet_Wetbulb
        self.Design_cooling = self.InletTemp - self.OutletTemp
        self.Diff_Outlet_Wetbulb = self.OutletTemp - self.OutdoorWetBulb

        # Prepare data for prediction using the converted properties
        data_for_prediction = [[
            self.converted_InletTemp, 
            self.converted_OutletTemp, 
            self.converted_OutdoorWetBulb, 
            self.converted_OutdoorAirTemp, 
            self.converted_OutdoorAirHumidity, 
            self.converted_Kw_cooling, 
            self.converted_Kw_Chiller, 
            self.converted_Design_cooling, 
            self.converted_Diff_Outlet_Wetbulb
        ]]

        forecast_result = model_random_forest.predict(data_for_prediction)
        print(f"Model prediction: {forecast_result}")
        
        self.Status = forecast_result[0]
        print(f"Status before save: {self.Status}")
    
        if self.Status == 1:
            self.notify_line('The forecast status is 1! Please check the cooling tower.')

    def save(self, *args, **kwargs):
        # Step 3 : Forecasting
        self.predict_status()
        print(f"Status at save: {self.Status}") 

        # Call the parent class's save method
        super().save(*args, **kwargs)

    