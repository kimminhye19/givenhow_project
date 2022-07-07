from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateField, IntegerField
from django.db.models.fields.related import ForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from sklearn.tree import DecisionTreeClassifier


# db데이터 순서는 여기 순서대로 간다~ dbeaver는 이상한 컬럼순서대로 있음;
class Survey(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='추천메타아이디')
    writer = models.ForeignKey('accounts.Users', on_delete=models.SET_NULL, null=True, verbose_name="작성자")
    gender = models.CharField(max_length=10, null=True, verbose_name='성별')
    birth_year = models.DateTimeField(null=True, verbose_name='생일년도')
    birth_mmdd = models.DateTimeField(null=True, verbose_name='생일월일')
    sido_sigungu_1 = models.CharField(max_length=100, null=True, verbose_name='선호지역 시도 시군구1')
    satisfaction1 = models.IntegerField(null=True, verbose_name='선호지역1의 만족도')
    sido_sigungu_2 = models.CharField(max_length=100, null=True, verbose_name='선호지역 시도 시군구2')
    satisfaction2 = models.IntegerField(null=True, verbose_name='선호지역2의 만족도')
    sido_sigungu_3 = models.CharField(max_length=100, null=True, verbose_name='선호지역 시도 시군구3')
    satisfaction3 = models.IntegerField(null=True, verbose_name='선호지역3의 만족도')
    # theme = models.CharField(max_length=100, null=True, verbose_name='선호테마')
    created_dt = models.DateTimeField(auto_now_add=True, verbose_name='작성날짜', null=True)
    com_code_rg_id = models.ForeignKey('given_home.Com_Code', on_delete=models.SET_NULL, related_name='공통코드_거주지역아이디',
                                null=True, db_column= "com_code_rg_id", verbose_name='공통코드_거주지역아이디')
    com_code_tm_id = models.ForeignKey('given_home.Com_Code', on_delete=models.SET_NULL, related_name='공통코드_선호테마아이디',
                                 null=True, db_column= "com_code_tm_id", verbose_name='공통코드_선호테마아이디')
    earnings = models.IntegerField(null=True, verbose_name='수입')
    spec = models.CharField(max_length=100, null=True, verbose_name='학력')

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'survey'
        verbose_name = 'survey'
        verbose_name_plural = 'survey'


class Chucheon_Spot(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='아이디')
    rate = models.FloatField(null=True, verbose_name='일치율')
    rc_date = models.DateTimeField(auto_now_add=True, verbose_name='추천일자', null=True)
    user_id = models.ForeignKey('accounts.Users', on_delete=models.SET_NULL, null=True, db_column= "user_id", verbose_name='회원 아이디')
    rc_id = models.ForeignKey('chucheon.Survey', on_delete=models.SET_NULL, null=True, db_column= "rc_id", verbose_name='추천테마 아이디')
    trip_id = models.ForeignKey('given_home.Tour_Spots', on_delete=models.SET_NULL, null=True, db_column= "trip_id", verbose_name='여행지 아이디')
    star = models.FloatField(null=True, verbose_name='만족도')

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'chucheon_spot'
        verbose_name = 'chucheon_spot'
        verbose_name_plural = 'chucheon_spot'


class Ai_Result(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='아이디')
    rc_loc_1_1 = models.CharField(max_length=100, null=True, verbose_name='추천지역1_1')
    rc_loc_1_2 = models.CharField(max_length=100, null=True, verbose_name='추천지역1_2')
    rc_loc_1_3 = models.CharField(max_length=100, null=True, verbose_name='추천지역1_3')
    rc_loc_2_1 = models.CharField(max_length=100, null=True, verbose_name='추천지역2_1')
    rc_loc_2_2 = models.CharField(max_length=100, null=True, verbose_name='추천지역2_2')
    rc_loc_2_3 = models.CharField(max_length=100, null=True, verbose_name='추천지역2_3')
    rc_loc_3_1 = models.CharField(max_length=100, null=True, verbose_name='추천지역3_1')
    rc_loc_3_2 = models.CharField(max_length=100, null=True, verbose_name='추천지역3_2')
    rc_loc_3_3 = models.CharField(max_length=100, null=True, verbose_name='추천지역3_2')
    userid = models.ForeignKey('accounts.Users', on_delete=models.SET_NULL, null=True, db_column= "user_id", verbose_name='회원 아이디')
    rc_id= models.ForeignKey('chucheon.Survey', on_delete=models.SET_NULL, null=True, db_column= "rc_id", verbose_name='추천테마 아이디')

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'ai_result'
        verbose_name = 'ai_result'
        verbose_name_plural = 'ai_result'





