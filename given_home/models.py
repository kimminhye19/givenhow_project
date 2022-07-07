from django.db import models


class Tour_Spots(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='아이디')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='여행지명')
    add_detail = models.CharField(max_length=100, blank=True, null=True, verbose_name='여행지세부주소')
    gps_x = models.FloatField(blank=True, null=True, verbose_name='x좌표')
    gps_y = models.FloatField(blank=True, null=True, verbose_name='y좌표')
    image_src = models.CharField(max_length=100, blank=True, null=True, verbose_name='이미지_경로')
    tel = models.CharField(max_length=100, blank=True, null=True, verbose_name='전화번호')
    hits = models.IntegerField(blank=True, null=True, verbose_name='조회수')
    com_code_rg_id = models.ForeignKey('given_home.Com_Code', on_delete=models.SET_NULL, null=True, db_column='com_code_rg_id',
                                 related_name='공통코드_지역아이디', verbose_name='공통코드_지역아이디')
    com_code_tm_id = models.ForeignKey('given_home.Com_Code', on_delete=models.SET_NULL, null=True, db_column='com_code_tm_id',
                                  related_name='공통코드_테마아이디', verbose_name='공통코드_테마아이디')

    class Meta :
        db_table = 'tour_spots'
        managed = True
        verbose_name = '여행지'
        verbose_name_plural = '여행지'


class Com_Code(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='아이디')
    gr_code = models.ForeignKey('given_home.Group_Code', db_column= "gr_code",
                                on_delete=models.CASCADE, verbose_name="공통그룹코드")
    com_code = models.CharField(max_length=100, blank=True, null=True, verbose_name='공통코드')
    code_nm = models.CharField(max_length=100, blank=True, null=True, verbose_name="코드명")
    upper_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="상위코드")
    comment = models.TextField(blank=True, null=True, verbose_name="설명")

    class Meta:
        managed = True
        db_table = 'com_code'


class Group_Code(models.Model):
    gr_code = models.CharField(max_length=100, primary_key=True, verbose_name="공통그룹코드")
    gr_code_nm = models.CharField(max_length=100, blank=True, null=True, verbose_name="공통그룹코드명")
    upper_gr_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="상위그룹코드")
    gr_comment = models.TextField(blank=True, null=True, verbose_name="설명")

    class Meta:
        managed = True
        db_table = 'group_code'


