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
    cooling_machine_number = models.CharField(max_length=100, blank=True, null=True)
    InletTemp = models.FloatField()
    OutletTemp = models.FloatField()
    OutdoorWetBulb = models.FloatField()
    OutdoorAirTemp = models.FloatField()
    OutdoorAirHumidity = models.FloatField()
    Kw_cooling = models.FloatField()
    Kw_Chiller = models.FloatField()
    Delta_T = models.FloatField(null=True, blank=True)
    Approach_Temperature = models.FloatField(null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True)

    @property
    def year(self):
        return self.recorded_at.year

    @property
    def month(self):
        return self.recorded_at.month

    @property
    def day(self):
        return self.recorded_at.day

    @property
    def hour(self):
        return self.recorded_at.hour

    @property
    def minute(self):
        return self.recorded_at.minute

    @property
    def converted_Minute(self):
        if 1 <= self.minute <= 15:
            return 1
        elif 16 <= self.minute <= 30:
            return 2
        elif 31 <= self.minute <= 45:
            return 3
        elif 46 <= self.minute <= 60:
            return 4
        return None

    
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
    def converted_Delta_T(self):
        if self.Delta_T < 7:
            return 1
        elif 7 <= self.Delta_T < 10:
            return 2
        else:
            return 3

    @property
    def converted_Approach_Temperature(self):
        if self.Approach_Temperature < 0:
            return 1
        elif 0 <= self.Approach_Temperature < 7:
            return 2
        else:
            return 3

    def notify_line(self, message):
        try:
            line_bot_api.push_message(LINE_USER_ID, TextSendMessage(text=message))
        except LineBotApiError as e:
            print(f"Failed to send message: {e}")

    def predict_status(self):
        # Compute Delta_T and Approach_Temperature
        self.Delta_T = self.InletTemp - self.OutletTemp
        self.Approach_Temperature = self.OutletTemp - self.OutdoorWetBulb

        # Prepare data for prediction using the converted properties
        data_for_prediction = [[
            self.year, 
            self.month, 
            self.day, 
            self.hour, 
            self.converted_Minute,
            self.converted_InletTemp, 
            self.converted_OutletTemp, 
            self.converted_OutdoorWetBulb, 
            self.converted_OutdoorAirTemp, 
            self.converted_OutdoorAirHumidity, 
            self.converted_Kw_cooling, 
            self.converted_Kw_Chiller, 
            self.converted_Delta_T, 
            self.converted_Approach_Temperature
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

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title