from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from given_home.models import Tour_Spots, Com_Code
from chucheon.models import Survey, Ai_Result
from accounts.models import Users
from chucheon.models import Survey
import random
# from chucheon.views import Recommendation_result


def General_chucheon(request):

    # 장고의 orm을 이용하기 위해 원형을 유지하고자 함
    # values에서 필요한 컬럼을 '컬럼명' 형식으로 나열. 이때 다른 테이블의 데이터를 참고하는 경우 'foreign key__컬럼명' 형식으로 나열
    # ex. 모델링 결과 변수 필터 filter(com_code_gr_id= 123, com_code_tm_id__upper_code= pr_tm_code3)


    # 1번째 함수 시작 (화면단 first table data)
    general_chucheon = Tour_Spots.objects.values('id','name','add_detail','image_src','tel','hits',
                                        'com_code_rg_id',
                                        'com_code_rg_id__com_code', 'com_code_rg_id__code_nm', 'com_code_rg_id__upper_code',
                                        'com_code_tm_id',
                                        'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                        'com_code_tm_id__upper_code').order_by('hits')[0:3]
    # 모든 여행지 중에서 조회수(hit)가 가장 높은 여행지 3곳을 반환하는 쿼리셋

    pr_tm_code1 = list(general_chucheon.values('com_code_tm_id__upper_code')[0].values())[0]
    # == > A0202 <==  A0202까지는 Tour_spots에서 uppercode로 역조회
    # 부모코드명이 궁금한 쿼리셋의 upper_code를 변수에 저장하고, 변수의 value만 list형식으로 저장해 값을 빼내기 위해 [0]으로 슬라이싱
    # print("pr_tm_code1.values(): ", pr_tm_code1.values())
    # print("list(pr_tm_code1.values())[0]: ", list(pr_tm_code1.values())[0])
    pr_tm_name1 = Com_Code.objects.filter(com_code=pr_tm_code1).values('code_nm')
    # Com_Code 테이블에서 com_code == com_code_tm_id__upper_code인 data를 찾아 code_nm(코드명)을 반환
    # print("pr_tm_name1: ", pr_tm_name1)

    pr_rg_code1 = list(general_chucheon.values('com_code_rg_id__upper_code')[0].values())[0]
    pr_rg_name1 = Com_Code.objects.filter(com_code=pr_rg_code1).values('code_nm')
    print("pr_rg_name1: ", pr_rg_name1)
    # tm코드와 동일한 방식으로 추출


    # 2번째 함수 시작(화면단 second table data)
    ran_rg = [31240, 1110, 3830, 31370, 31100, 34380, 3430, 3920, 3870, 2310]
    # 가장 조회수가 높은(인기가 많은) 여행지역의 지역코드! 해당 지역코드들을 랜덤으로 filter값으로 사용하여 여행지 반환
    general_chucheon_ran_rg = Tour_Spots.objects.values('id','name','add_detail','image_src','tel','hits',
                                        'com_code_rg_id',
                                        'com_code_rg_id__com_code', 'com_code_rg_id__code_nm', 'com_code_rg_id__upper_code',
                                        'com_code_tm_id',
                                        'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                        'com_code_tm_id__upper_code').filter(com_code_rg_id__com_code=random.choice(ran_rg)).order_by('hits')[0:3]
                                                                    # com_code에 대한 정보를 스캔하려면 foreign key로 접근

    pr_tm_code2 = list(general_chucheon_ran_rg.values('com_code_tm_id__upper_code')[0].values())[0]
    pr_tm_name2 = Com_Code.objects.filter(com_code=pr_tm_code2).values('code_nm')

    pr_rg_code2 = list(general_chucheon_ran_rg.values('com_code_rg_id__upper_code')[0].values())[0]
    pr_rg_name2 = Com_Code.objects.filter(com_code=pr_rg_code2).values('code_nm')
    print("pr_rg_name2: ", pr_rg_name2)
    # 프론트용 주소찍기
    rg_name2 = list(general_chucheon_ran_rg.values('com_code_rg_id__code_nm')[0].values())
    print("rg_name2: ", rg_name2)

    # 3번째 함수 시작(화면단 third table data)
    ran_tm = ['A0101', 'A0102', 'A0201', 'A0202', 'A0203', 'A0205', 'A0206', 'A0207', 'A0208']
    # A0204 지역명 깨져서 잠시 보류.
    # 여행테마 중분류의 com_code 해당 테마코드(여행지는 소분류 기준이기 때문에 upper_code가 됨)들을 랜덤으로 filter값으로 사용하여 여행지 반환
    general_chucheon_ran_tm = Tour_Spots.objects.values('id','name','add_detail','image_src','tel','hits',
                                        'com_code_rg_id',
                                        'com_code_rg_id__com_code', 'com_code_rg_id__code_nm', 'com_code_rg_id__upper_code',
                                        'com_code_tm_id',
                                        'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                        'com_code_tm_id__upper_code').filter(com_code_tm_id__upper_code=random.choice(ran_tm)).order_by('hits')[0:3]
                                                                    # upper_code 대한 정보를 스캔하려면 foreign key로 접근
                                                                    # upper_code로 찾는 이유는 중분류라서!

    # rg_name_3 = Com_Code.objects.values('code_nm').filter(com_code=general_chucheon_ran_tm.values('com_code_rg_id__com_code'))
    # tm_pr_name_3 = Com_Code.objects.values('code_nm').filter(com_code=(general_chucheon_ran_tm.values('com_code_tm_id__upper_code')[0]))
    # print("tm_pr_name_3: ",tm_pr_name_3)

    pr_tm_code3 = list(general_chucheon_ran_tm.values('com_code_tm_id__upper_code')[0].values())[0]
    pr_tm_name3 = Com_Code.objects.filter(com_code=pr_tm_code3).values('code_nm')

    pr_rg_code3 = list(general_chucheon_ran_tm.values('com_code_rg_id__upper_code')[0].values())[0]
    pr_rg_name3 = Com_Code.objects.filter(com_code=pr_rg_code3).values('code_nm')
    print("pr_rg_name3: ", pr_rg_name3)

    return render(request, "home/home.html", {'general_chucheon': general_chucheon, 'pr_tm_name1': pr_tm_name1, 'pr_rg_name1': pr_rg_name1,
                                              'general_chucheon_ran_rg': general_chucheon_ran_rg, 'pr_tm_name2': pr_tm_name2, 'pr_rg_name2': pr_rg_name2, 'rg_name2': rg_name2,
                                              'general_chucheon_ran_tm': general_chucheon_ran_tm, 'pr_tm_name3': pr_tm_name3, 'pr_rg_name3': pr_rg_name3})


def TripLocal_Chucheon(request):

    # 장고의 orm을 이용하기 위해 원형을 유지하고자 함
    # values에서 필요한 컬럼을 '컬럼명' 형식으로 나열. 이때 다른 테이블의 데이터를 참고하는 경우 'foreign key__컬럼명' 형식으로 나열
    # ex. 모델링 결과 변수 필터 filter(com_code_gr_id= 123, com_code_tm_id__upper_code= pr_tm_code3)


    # 1번째 함수 시작 (화면단 first table data)
    general_chucheon = Tour_Spots.objects.values('id','name','add_detail','image_src','tel','hits',
                                        'com_code_rg_id',
                                        'com_code_rg_id__com_code', 'com_code_rg_id__code_nm', 'com_code_rg_id__upper_code',
                                        'com_code_tm_id',
                                        'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                        'com_code_tm_id__upper_code').order_by('hits')[0:3]
    # 모든 여행지 중에서 조회수(hit)가 가장 높은 여행지 3곳을 반환하는 쿼리셋

    pr_tm_code1 = list(general_chucheon.values('com_code_tm_id__upper_code')[0].values())[0]
    # == > A0202 <==  A0202까지는 Tour_spots에서 uppercode로 역조회
    # 부모코드명이 궁금한 쿼리셋의 upper_code를 변수에 저장하고, 변수의 value만 list형식으로 저장해 값을 빼내기 위해 [0]으로 슬라이싱
    # print("pr_tm_code1.values(): ", pr_tm_code1.values())
    # print("list(pr_tm_code1.values())[0]: ", list(pr_tm_code1.values())[0])
    pr_tm_name1 = Com_Code.objects.filter(com_code=pr_tm_code1).values('code_nm')
    # Com_Code 테이블에서 com_code == com_code_tm_id__upper_code인 data를 찾아 code_nm(코드명)을 반환
    # print("pr_tm_name1: ", pr_tm_name1)

    pr_rg_code1 = list(general_chucheon.values('com_code_rg_id__upper_code')[0].values())[0]
    pr_rg_name1 = Com_Code.objects.filter(com_code=pr_rg_code1).values('code_nm')
    print("pr_rg_name1: ", pr_rg_name1)
    # tm코드와 동일한 방식으로 추출


    # 2번째 함수 시작(화면단 second table data)
    ran_rg = [31240, 1110, 3830, 31370, 31100, 34380, 3430, 3920, 3870, 2310]
    # 가장 조회수가 높은(인기가 많은) 여행지역의 지역코드! 해당 지역코드들을 랜덤으로 filter값으로 사용하여 여행지 반환
    general_chucheon_ran_rg = Tour_Spots.objects.values('id','name','add_detail','image_src','tel','hits',
                                        'com_code_rg_id',
                                        'com_code_rg_id__com_code', 'com_code_rg_id__code_nm', 'com_code_rg_id__upper_code',
                                        'com_code_tm_id',
                                        'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                        'com_code_tm_id__upper_code').filter(com_code_rg_id__com_code=random.choice(ran_rg)).order_by('hits')[0:3]
                                                                    # com_code에 대한 정보를 스캔하려면 foreign key로 접근

    pr_tm_code2 = list(general_chucheon_ran_rg.values('com_code_tm_id__upper_code')[0].values())[0]
    pr_tm_name2 = Com_Code.objects.filter(com_code=pr_tm_code2).values('code_nm')

    pr_rg_code2 = list(general_chucheon_ran_rg.values('com_code_rg_id__upper_code')[0].values())[0]
    pr_rg_name2 = Com_Code.objects.filter(com_code=pr_rg_code2).values('code_nm')
    print("pr_rg_name2: ", pr_rg_name2)
    # 프론트용 주소찍기
    rg_name2 = list(general_chucheon_ran_rg.values('com_code_rg_id__code_nm')[0].values())
    print("rg_name2: ", rg_name2)

    # 3번째 함수 시작(화면단 third table data)
    ran_tm = ['A0101', 'A0102', 'A0201', 'A0202', 'A0203', 'A0205', 'A0206', 'A0207', 'A0208']
    # A0204 지역명 틀어져서 잠깐 자름
    # 여행테마 중분류의 com_code 해당 테마코드(여행지는 소분류 기준이기 때문에 upper_code가 됨)들을 랜덤으로 filter값으로 사용하여 여행지 반환
    general_chucheon_ran_tm = Tour_Spots.objects.values('id','name','add_detail','image_src','tel','hits',
                                        'com_code_rg_id',
                                        'com_code_rg_id__com_code', 'com_code_rg_id__code_nm', 'com_code_rg_id__upper_code',
                                        'com_code_tm_id',
                                        'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                        'com_code_tm_id__upper_code').filter(com_code_tm_id__upper_code=random.choice(ran_tm)).order_by('hits')[0:3]
                                                                    # upper_code 대한 정보를 스캔하려면 foreign key로 접근
                                                                    # upper_code로 찾는 이유는 중분류라서!

    # rg_name_3 = Com_Code.objects.values('code_nm').filter(com_code=general_chucheon_ran_tm.values('com_code_rg_id__com_code'))
    # tm_pr_name_3 = Com_Code.objects.values('code_nm').filter(com_code=(general_chucheon_ran_tm.values('com_code_tm_id__upper_code')[0]))
    # print("tm_pr_name_3: ",tm_pr_name_3)

    pr_tm_code3 = list(general_chucheon_ran_tm.values('com_code_tm_id__upper_code')[0].values())[0]
    pr_tm_name3 = Com_Code.objects.filter(com_code=pr_tm_code3).values('code_nm')

    pr_rg_code3 = list(general_chucheon_ran_tm.values('com_code_rg_id__upper_code')[0].values())[0]
    pr_rg_name3 = Com_Code.objects.filter(com_code=pr_rg_code3).values('code_nm')
    
    
    # 설문한 지역의 시도, 시군구
    user_id = request.session.get('user')
    users = Users.objects.get(userid=user_id)
    airesult = Ai_Result()
    airesult.userid = users
    userid = airesult.userid

    sido_sigungu = Survey.objects.filter(writer_id=users).values('sido_sigungu_1','sido_sigungu_2','sido_sigungu_3')
    sido_sigungu_1, sido_sigungu_2, sido_sigungu_3 = list(sido_sigungu.get().values())
    sido_sigungu_1_up = list(Com_Code.objects.filter(com_code=sido_sigungu_1).values('upper_code').get().values())[0]
    sido_sigungu_1_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_1_up).values('code_nm').get().values())[0]
    sido_sigungu_1_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_1).values('code_nm').get().values())[0]
    sido_sigungu_2_up = list(Com_Code.objects.filter(com_code=sido_sigungu_2).values('upper_code').get().values())[0]
    sido_sigungu_2_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_2_up).values('code_nm').get().values())[0]
    sido_sigungu_2_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_2).values('code_nm').get().values())[0]
    sido_sigungu_3_up = list(Com_Code.objects.filter(com_code=sido_sigungu_3).values('upper_code').get().values())[0]
    sido_sigungu_3_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_3_up).values('code_nm').get().values())[0]
    sido_sigungu_3_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_3).values('code_nm').get().values())[0]

    return render(request, "home/chucheon_home.html", {'general_chucheon': general_chucheon, 'pr_tm_name1': pr_tm_name1, 'pr_rg_name1': pr_rg_name1,
                                              'general_chucheon_ran_rg': general_chucheon_ran_rg, 'pr_tm_name2': pr_tm_name2, 'pr_rg_name2': pr_rg_name2, 'rg_name2': rg_name2,
                                              'general_chucheon_ran_tm': general_chucheon_ran_tm, 'pr_tm_name3': pr_tm_name3, 'pr_rg_name3': pr_rg_name3,
                                                      'sido_sigungu_1_pr':sido_sigungu_1_pr, 'sido_sigungu_1_nm':sido_sigungu_1_nm,
                                                      'sido_sigungu_2_pr':sido_sigungu_2_pr, 'sido_sigungu_2_nm':sido_sigungu_2_nm,
                                                      'sido_sigungu_3_pr':sido_sigungu_3_pr, 'sido_sigungu_3_nm':sido_sigungu_3_nm,})



# def TripLocal_Chucheon(request):
#     TripLocals1 = Tour_Spots.objects.raw("""
#          SELECT * FROM tour_spots
#          WHERE com_code_rg_id is not '' 
#          and hits is not ''
#          and image_src is not ''
#          and name like '바다%'
#          order by hits desc
#          limit 3;
#          """)

#     TripLocals2 = Tour_Spots.objects.raw("""
#          SELECT * FROM tour_spots
#          WHERE com_code_rg_id is not ''
#          and hits is not ''
#          and image_src is not ''
#          and com_code_rg_id == '163'
#          order by hits desc
#          limit 3;
#          """)

#     TripLocals3 = Tour_Spots.objects.raw("""
#          SELECT * FROM tour_spots
#          WHERE com_code_rg_id is not ''
#          and hits is not ''
#          and image_src is not ''
#          and com_code_tm_id like '441'
#          order by hits desc
#          limit 3;
#          """)
#     return render(request, "home/chucheon_home.html", {'TripLocals1': TripLocals1, 'TripLocals2': TripLocals2, 'TripLocals3': TripLocals3})



def TripLocal_Chucheon_like1(request):
    TripLocals1 = Tour_Spots.objects.raw("""
         SELECT * FROM tour_spots
         WHERE com_code_rg_id is not '' 
         and hits is not ''
         and image_src is not ''
         and name like '바다%'
         order by hits desc
         limit 3;
         """)

    TripLocals2 = Tour_Spots.objects.raw("""
         SELECT * FROM tour_spots
         WHERE com_code_rg_id is not ''
         and hits is not ''
         and image_src is not ''
         and com_code_rg_id == '163'
         order by hits desc
         limit 3;
         """)

    TripLocals3 = Tour_Spots.objects.raw("""
         SELECT * FROM tour_spots
         WHERE com_code_rg_id is not ''
         and hits is not ''
         and image_src is not ''
         and com_code_tm_id like '441'
         order by hits desc
         limit 3;
         """)
    return render(request, "home/chucheon_home.html", {'TripLocals1': TripLocals1, 'TripLocals2': TripLocals2, 'TripLocals3': TripLocals3})



def TripLocal_Chucheon_like2(request):
    TripLocals1 = Tour_Spots.objects.raw("""
         SELECT * FROM tour_spots
         WHERE com_code_rg_id is not '' 
         and hits is not ''
         and image_src is not ''
         and name like '바다%'
         order by hits desc
         limit 3;
         """)

    TripLocals2 = Tour_Spots.objects.raw("""
         SELECT * FROM tour_spots
         WHERE com_code_rg_id is not ''
         and hits is not ''
         and image_src is not ''
         and com_code_rg_id == '163'
         order by hits desc
         limit 3;
         """)

    TripLocals3 = Tour_Spots.objects.raw("""
         SELECT * FROM tour_spots
         WHERE com_code_rg_id is not ''
         and hits is not ''
         and image_src is not ''
         and com_code_tm_id like '441'
         order by hits desc
         limit 3;
         """)
    return render(request, "home/chucheon_home.html", {'TripLocals1': TripLocals1, 'TripLocals2': TripLocals2, 'TripLocals3': TripLocals3})



def TripLocal_Chucheon_like3(request):
    TripLocals1 = Tour_Spots.objects.raw("""
         SELECT * FROM tour_spots
         WHERE com_code_rg_id is not '' 
         and hits is not ''
         and image_src is not ''
         and name like '바다%'
         order by hits desc
         limit 3;
         """)

    TripLocals2 = Tour_Spots.objects.raw("""
         SELECT * FROM tour_spots
         WHERE com_code_rg_id is not ''
         and hits is not ''
         and image_src is not ''
         and com_code_rg_id == '163'
         order by hits desc
         limit 3;
         """)

    TripLocals3 = Tour_Spots.objects.raw("""
         SELECT * FROM tour_spots
         WHERE com_code_rg_id is not ''
         and hits is not ''
         and image_src is not ''
         and com_code_tm_id like '441'
         order by hits desc
         limit 3;
         """)
    return render(request, "home/chucheon_home.html", {'TripLocals1': TripLocals1, 'TripLocals2': TripLocals2, 'TripLocals3': TripLocals3})

