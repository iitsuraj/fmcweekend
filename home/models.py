from django.db import models
# from multiselectfield import MultiSelectField
# ONLINE_CHOICES=(
#         ('0','Online Events'),
#         ('1','e1'),
#         ('2','e2'),
#         ('3','e3'),
#         ('4','e4'),
#         ('5','e5'),   
# )
# Create your models here.

class Registration(models.Model):
    team_name=models.CharField(max_length=50)
    team_leader=models.CharField(max_length=100)
    email=models.EmailField()
    contact=models.CharField(max_length=10)
    team_size=models.PositiveIntegerField()
    accomodation=models.IntegerField(default=0)
    amount_paid=models.FloatField(default=0.0)
    payment_status=models.BooleanField(default=False)
    payment_id=models.CharField(max_length=50,null=True)
    payment_request_id=models.CharField(max_length=50,null=True)
    offline_reg=models.BooleanField(default=False)
    e_against_all_odds=models.BooleanField(default=False)
    e_write_o_maniac=models.BooleanField(default=False)
    e_documentary_making=models.BooleanField(default=False)
    e_cover_art=models.BooleanField(default=False)
    e_escapade=models.BooleanField(default=False)
    f_3draw=models.BooleanField(default=False)
    f_allin=models.BooleanField(default=False)
    f_take_two=models.BooleanField(default=False)
    f_selfie=models.BooleanField(default=False)
    f_memoravel=models.BooleanField(default=False)
    f_monogram=models.BooleanField(default=False)
    # w_design=models.IntegerField(default=0)
    # w_nikon=models.IntegerField(default=0)
    def __str__(self):
        return self.team_name
    class Meta:
        ordering=('team_name',)