from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Survey, Ai_Result
from accounts.models import Users
from given_home.models import Tour_Spots, Com_Code
import random
import csv
import json
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib import messages
from .forms import TripForm
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


@csrf_exempt
def survey_view(request):
    if request.method == 'GET':
        return render(request, 'chucheon/survey.html')
    elif request.method == 'POST':
        user_id = request.session.get('user')
        users = Users.objects.get(userid=user_id)
        survey = Survey()
        survey.writer = users
        writer = survey.writer
        sido_sigungu_1 = request.POST.get('sido1', None)+request.POST.get('sigungu1', None)
        satisfaction1 = request.POST.get('satisfaction1', None)
        sido_sigungu_2 = request.POST.get('sido2', None)+ request.POST.get('sigungu2', None)
        satisfaction2 = request.POST.get('satisfaction2', None)
        sido_sigungu_3 = request.POST.get('sido3', None)+ request.POST.get('sigungu3', None)
        satisfaction3 = request.POST.get('satisfaction3', None)
        com_code_tm_id = request.POST.get('theme', None)
        res_data = {}
        print("request3 : ", request)
        if not (sido_sigungu_1 and satisfaction1 and sido_sigungu_2 and satisfaction2 and sido_sigungu_3 and satisfaction3 and com_code_tm_id):
            res_data['error'] = '모든 값을 선택하세요!'
            return render(request, 'chucheon/survey.html', res_data)
        else:
            spots = Survey( writer=writer, sido_sigungu_1=sido_sigungu_1, satisfaction1=satisfaction1,
                            sido_sigungu_2=sido_sigungu_2, satisfaction2=satisfaction2,
                            sido_sigungu_3=sido_sigungu_3, satisfaction3=satisfaction3,
                            com_code_tm_id=Com_Code.objects.get(com_code=com_code_tm_id))
            print(request)
            spots.save()
        return redirect('/chucheon/result') # 나중에 /chucheon_home 으로 바꿔줘야 함

@csrf_exempt
def Recommendation_result(x):
    # -- 분석시작 --
    # 파일 불러오기
    ratings = pd.read_csv("ml_model/final_rating.csv", encoding='cp949')
    regions = pd.read_csv("ml_model/final_region.csv", encoding='utf-8')

    ratings['region_id'] = ratings['region_id'].astype(object)
    regions['region_id'] = regions['region_id'].astype(object)

    # print(ratings[ratings['region_id'].isnull()])
    trip_score = pd.merge(ratings, regions, on = 'region_id')
    # trip_score.drop('genres', inplace=True, axis=1)
    trip_user_rating = trip_score.pivot_table('rating', index='user_id', columns="region_id").fillna(0)
    # trip_user_rating.info()
    data1 = trip_user_rating.transpose()
    trip_sim = cosine_similarity(data1, data1)
    # print("trip_sim.info():", trip_sim.dtype)

    # 유사도 출력
    # trip_sim_df = pd.DataFrame(data = trip_sim, index= data1.index, columns=data1.index)[2:]
    trip_sim_df = pd.DataFrame(data=trip_sim, index=data1.index, columns=data1.index)

    # 여행지 추천
    # chucheon_region = trip_sim_df[x].sort_values(ascending=False)[1:4]
    # print(chucheon_region)

    # 예외처리 한것것
    try:
        chucheon_region = trip_sim_df[x].sort_values(ascending=False)[1:4]
        # print("chucheon_region: ", chucheon_region)
    except KeyError:
        print("해당 지역에 방문한 유저가 없습니다. total top 여행지를 대신 추천합니다.")
        random_rg = [31240, 1110, 3830, 31370, 31100, 34380, 3430, 3920, 3870, 2310]
        chucheon_region = trip_sim_df[random.choice(random_rg)].sort_values(ascending=False)[1:4]

    # 여행지명과 유사도 출력, 그리고 zip파일로 합쳐놓음
    regions_result = chucheon_region.index
    ratings_result = chucheon_region.values
    chucheon_list = zip(regions_result, ratings_result)
    # print("chucheon_list : ", chucheon_list) # values 하나 넣어서 지역 3개 나옴

    return chucheon_list

@csrf_exempt
# 추천받은 여행지를 DB에 넣는 과정
def getAiResult(request):
    user_id = request.session.get('user')
    users = Users.objects.get(userid=user_id)
    airesult = Ai_Result()
    airesult.userid = users
    userid = airesult.userid

    sido_sigungu = Survey.objects.filter(writer_id=users).values('sido_sigungu_1','sido_sigungu_2','sido_sigungu_3')
    sido_sigungu_1, sido_sigungu_2, sido_sigungu_3 = list(sido_sigungu.get().values())
    likes = list(sido_sigungu.get().values())   #유저가 설문에서 답한 여행지역 3곳

    # 설문한 여행지에 대한 추천받은 여행지역 3가지 쪼개기
    x = int(likes[0])
    rc_loc_1 = x
    like1, similarity1 = zip(*Recommendation_result(x))
    # Similarity1 = Recommendation_result(x)[1]
    rc_loc_1_1 = like1[0] # like1의 첫번째 추천지역
    rc_loc_1_2 = like1[1] # like1의 두번째 추천지역
    rc_loc_1_3 = like1[2] # like1의 세번째 추천지역

    x = int(likes[1])
    rc_loc_2 = x
    like2, similarity2 = zip(*Recommendation_result(x))
    # Similarity2 = Recommendation_result(x)[1]
    rc_loc_2_1 = like2[0]  # like2의 첫번째 추천지역
    rc_loc_2_2 = like2[1]  # like2의 두번째 추천지역
    rc_loc_2_3 = like2[2]  # like2의 세번째 추천지역

    x = int(likes[2])
    rc_loc_3 = x
    like3, similarity3 = zip(*Recommendation_result(x))
    # Similarity3 = Recommendation_result(x)[1]
    rc_loc_3_1 = like3[0]  # like3의 첫번째 추천지역
    rc_loc_3_2 = like3[1]  # like3의 두번째 추천지역
    rc_loc_3_3 = like3[2]  # like3의 세번째 추천지역
    
    # 설문한 지역의 시도, 시군구
    sido_sigungu_1_up = list(Com_Code.objects.filter(com_code=sido_sigungu_1).values('upper_code').get().values())[0]
    sido_sigungu_1_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_1_up).values('code_nm').get().values())[0]
    sido_sigungu_1_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_1).values('code_nm').get().values())[0]
    sido_sigungu_2_up = list(Com_Code.objects.filter(com_code=sido_sigungu_2).values('upper_code').get().values())[0]
    sido_sigungu_2_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_2_up).values('code_nm').get().values())[0]
    sido_sigungu_2_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_2).values('code_nm').get().values())[0]
    sido_sigungu_3_up = list(Com_Code.objects.filter(com_code=sido_sigungu_3).values('upper_code').get().values())[0]
    sido_sigungu_3_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_3_up).values('code_nm').get().values())[0]
    sido_sigungu_3_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_3).values('code_nm').get().values())[0]
    
    # 추천받은 지역 1,2,3의 시도, 시군구
    rc_loc_1_1_upper = list(Com_Code.objects.filter(com_code=rc_loc_1_1).values('upper_code').get().values())[0]
    rc_loc_1_1_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_1_1_upper).values('code_nm').get().values())[0]
    rc_loc_1_2_upper = list(Com_Code.objects.filter(com_code=rc_loc_1_2).values('upper_code').get().values())[0]
    rc_loc_1_2_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_1_2_upper).values('code_nm').get().values())[0]
    rc_loc_1_3_upper = list(Com_Code.objects.filter(com_code=rc_loc_1_3).values('upper_code').get().values())[0]
    rc_loc_1_3_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_1_3_upper).values('code_nm').get().values())[0]
    
    rc_loc_2_1_upper = list(Com_Code.objects.filter(com_code=rc_loc_2_1).values('upper_code').get().values())[0]
    rc_loc_2_1_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_2_1_upper).values('code_nm').get().values())[0]
    rc_loc_2_2_upper = list(Com_Code.objects.filter(com_code=rc_loc_2_2).values('upper_code').get().values())[0]
    rc_loc_2_2_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_2_2_upper).values('code_nm').get().values())[0]
    rc_loc_2_3_upper = list(Com_Code.objects.filter(com_code=rc_loc_2_3).values('upper_code').get().values())[0]
    rc_loc_2_3_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_2_3_upper).values('code_nm').get().values())[0]
    
    rc_loc_3_1_upper = list(Com_Code.objects.filter(com_code=rc_loc_3_1).values('upper_code').get().values())[0]
    rc_loc_3_1_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_3_1_upper).values('code_nm').get().values())[0]
    rc_loc_3_2_upper = list(Com_Code.objects.filter(com_code=rc_loc_3_2).values('upper_code').get().values())[0]
    rc_loc_3_2_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_3_2_upper).values('code_nm').get().values())[0]
    rc_loc_3_3_upper = list(Com_Code.objects.filter(com_code=rc_loc_3_3).values('upper_code').get().values())[0]
    rc_loc_3_3_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_3_3_upper).values('code_nm').get().values())[0]
    
    
    rc_loc_1_1_nm = list(Com_Code.objects.filter(com_code=rc_loc_1_1).values('code_nm').get().values())[0]
    rc_loc_1_2_nm = list(Com_Code.objects.filter(com_code=rc_loc_1_2).values('code_nm').get().values())[0]
    rc_loc_1_3_nm = list(Com_Code.objects.filter(com_code=rc_loc_1_3).values('code_nm').get().values())[0]
    rc_loc_2_1_nm = list(Com_Code.objects.filter(com_code=rc_loc_2_1).values('code_nm').get().values())[0]
    rc_loc_2_2_nm = list(Com_Code.objects.filter(com_code=rc_loc_2_2).values('code_nm').get().values())[0]
    rc_loc_2_3_nm = list(Com_Code.objects.filter(com_code=rc_loc_2_3).values('code_nm').get().values())[0]
    rc_loc_3_1_nm = list(Com_Code.objects.filter(com_code=rc_loc_3_1).values('code_nm').get().values())[0]
    rc_loc_3_2_nm = list(Com_Code.objects.filter(com_code=rc_loc_3_2).values('code_nm').get().values())[0]
    rc_loc_3_3_nm = list(Com_Code.objects.filter(com_code=rc_loc_3_3).values('code_nm').get().values())[0]
    

    airesult_rc = Ai_Result(userid=userid, rc_loc_1_1=Com_Code.objects.get(com_code=rc_loc_1_1).id,
                            rc_loc_1_2=Com_Code.objects.get(com_code=rc_loc_1_2).id,
                            rc_loc_1_3=Com_Code.objects.get(com_code=rc_loc_1_3).id,
                            rc_loc_2_1=Com_Code.objects.get(com_code=rc_loc_2_1).id,
                            rc_loc_2_2=Com_Code.objects.get(com_code=rc_loc_2_2).id,
                            rc_loc_2_3=Com_Code.objects.get(com_code=rc_loc_2_3).id,
                            rc_loc_3_1=Com_Code.objects.get(com_code=rc_loc_3_1).id,
                            rc_loc_3_2=Com_Code.objects.get(com_code=rc_loc_3_2).id,
                            rc_loc_3_3=Com_Code.objects.get(com_code=rc_loc_3_3).id)
    airesult_rc.save()
    return render(request, "chucheon/result.html", {"userid": userid, "sido_sigungu_1_nm":sido_sigungu_1_nm, "sido_sigungu_1_pr":sido_sigungu_1_pr,
                                                    "sido_sigungu_2_nm":sido_sigungu_2_nm, "sido_sigungu_2_pr":sido_sigungu_2_pr,
                                                    "sido_sigungu_3_nm":sido_sigungu_3_nm, "sido_sigungu_3_pr":sido_sigungu_3_pr,
                                                    "rc_loc_1_1_nm": rc_loc_1_1_nm, "rc_loc_1_1_pr_nm":rc_loc_1_1_pr_nm,
                                                    "rc_loc_1_2_nm": rc_loc_1_2_nm, "rc_loc_1_2_pr_nm":rc_loc_1_2_pr_nm,
                                                    "rc_loc_1_3_nm": rc_loc_1_3_nm, "rc_loc_1_3_pr_nm":rc_loc_1_3_pr_nm,
                                                    "rc_loc_2_1_nm": rc_loc_2_1_nm, "rc_loc_2_1_pr_nm":rc_loc_2_1_pr_nm,
                                                    "rc_loc_2_2_nm": rc_loc_2_2_nm, "rc_loc_2_2_pr_nm":rc_loc_2_2_pr_nm,
                                                    "rc_loc_2_3_nm": rc_loc_2_3_nm, "rc_loc_2_3_pr_nm":rc_loc_2_3_pr_nm,
                                                    "rc_loc_3_1_nm": rc_loc_3_1_nm, "rc_loc_3_1_pr_nm":rc_loc_3_1_pr_nm,
                                                    "rc_loc_3_2_nm": rc_loc_3_2_nm, "rc_loc_3_2_pr_nm":rc_loc_3_2_pr_nm,
                                                    "rc_loc_3_3_nm": rc_loc_3_3_nm, "rc_loc_3_3_pr_nm":rc_loc_3_3_pr_nm})



@csrf_exempt
def getAiResult_like1(request):
    # test 결과에 쓸 지역 이름을 갖고온다.
    user_id = request.session.get('user')
    users = Users.objects.get(userid=user_id)
    airesult = Ai_Result()
    airesult.userid = users
    userid = airesult.userid

    sido_sigungu = Survey.objects.filter(writer_id=users).values('sido_sigungu_1', 'sido_sigungu_2', 'sido_sigungu_3')
    sido_sigungu_1, sido_sigungu_2, sido_sigungu_3 = list(sido_sigungu.get().values())  # 유저가 설문에서 답한 여행지역 3곳

    sido_sigungu_1_up = list(Com_Code.objects.filter(com_code=sido_sigungu_1).values('upper_code').get().values())[0]
    sido_sigungu_1_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_1_up).values('code_nm').get().values())[0]
    sido_sigungu_1_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_1).values('code_nm').get().values())[0]
    sido_sigungu_2_up = list(Com_Code.objects.filter(com_code=sido_sigungu_2).values('upper_code').get().values())[0]
    sido_sigungu_2_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_2_up).values('code_nm').get().values())[0]
    sido_sigungu_2_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_2).values('code_nm').get().values())[0]
    sido_sigungu_3_up = list(Com_Code.objects.filter(com_code=sido_sigungu_3).values('upper_code').get().values())[0]
    sido_sigungu_3_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_3_up).values('code_nm').get().values())[0]
    sido_sigungu_3_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_3).values('code_nm').get().values())[0]

    # 추천받은 여행지역1_1,1_2,1_3 필터링작업 -> 각각 3개씩 여행지 출력!
    # 추천받은 여행지역 1_1,1_2,1_3 나눠줌
    rc_loc_1 = Ai_Result.objects.filter(userid=users).values('rc_loc_1_1', 'rc_loc_1_2', 'rc_loc_1_3')
    rc_loc_1_1, rc_loc_1_2, rc_loc_1_3 = list(rc_loc_1.get().values())
    rc_loc_1_1_nm = list(Com_Code.objects.filter(id=rc_loc_1_1).values('code_nm').get().values())[0]
    rc_loc_1_2_nm = list(Com_Code.objects.filter(id=rc_loc_1_2).values('code_nm').get().values())[0]
    rc_loc_1_3_nm = list(Com_Code.objects.filter(id=rc_loc_1_3).values('code_nm').get().values())[0]

    # 추천받은 지역의 시도 이름들
    rc_loc_1_upper = list(Com_Code.objects.filter(id=rc_loc_1_1).values('upper_code').get().values())[0]
    rc_loc_1_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_1_upper).values('code_nm').get().values())[0]

    rc_loc_2_upper = list(Com_Code.objects.filter(id=rc_loc_1_2).values('upper_code').get().values())[0]
    rc_loc_2_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_2_upper).values('code_nm').get().values())[0]

    rc_loc_3_upper = list(Com_Code.objects.filter(id=rc_loc_1_3).values('upper_code').get().values())[0]
    rc_loc_3_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_3_upper).values('code_nm').get().values())[0]

    # 설문에서 테마id 가져오기
    temem = Survey.objects.filter(writer_id=users).values('com_code_tm_id')
    com_code_tm_id = list(temem.get().values())[0]
    com_code_tm_id_gr = list(Com_Code.objects.filter(id=com_code_tm_id).values('gr_code').get().values())[0]
    pr_tm_name = list(Com_Code.objects.filter(id=com_code_tm_id).values('code_nm').get().values())[0]


    # 추천받은 여행지역1의 여행지 3곳출력
    TripLocals1 = Tour_Spots.objects.values('id', 'name', 'add_detail', 'image_src', 'tel', 'hits', 'com_code_rg_id',
                                            'com_code_rg_id__com_code', 'com_code_rg_id__code_nm',
                                            'com_code_rg_id__upper_code', 'com_code_tm_id',
                                            'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                            'com_code_tm_id__upper_code').filter(com_code_rg_id=rc_loc_1_1,
                                                                                 com_code_tm_id__gr_code=com_code_tm_id_gr).order_by(
        'hits')[0:3]

    TripLocals2 = Tour_Spots.objects.values('id', 'name', 'add_detail', 'image_src', 'tel', 'hits', 'com_code_rg_id',
                                            'com_code_rg_id__com_code', 'com_code_rg_id__code_nm',
                                            'com_code_rg_id__upper_code', 'com_code_tm_id',
                                            'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                            'com_code_tm_id__upper_code').filter(com_code_rg_id=rc_loc_1_2,
                                                                                 com_code_tm_id__gr_code=com_code_tm_id_gr).order_by(
        'hits')[0:3]

    TripLocals3 = Tour_Spots.objects.values('id', 'name', 'add_detail', 'image_src', 'tel', 'hits', 'com_code_rg_id',
                                            'com_code_rg_id__com_code', 'com_code_rg_id__code_nm',
                                            'com_code_rg_id__upper_code', 'com_code_tm_id',
                                            'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                            'com_code_tm_id__upper_code').filter(com_code_rg_id=rc_loc_1_3,
                                                                                 com_code_tm_id__gr_code=com_code_tm_id_gr).order_by(
        'hits')[0:3]

    return render(request, "home/chucheon_home_like1.html",
                  {'TripLocals1': TripLocals1, 'TripLocals2': TripLocals2, 'TripLocals3': TripLocals3,
                   'rc_loc_1_pr_nm': rc_loc_1_pr_nm, 'rc_loc_2_pr_nm': rc_loc_2_pr_nm, 'rc_loc_3_pr_nm': rc_loc_3_pr_nm,
                   "sido_sigungu_1_nm": sido_sigungu_1_nm,
                   "sido_sigungu_2_nm": sido_sigungu_2_nm,
                   "sido_sigungu_3_nm": sido_sigungu_3_nm,
                   "rc_loc_1_1_nm": rc_loc_1_1_nm,
                   "rc_loc_1_2_nm": rc_loc_1_2_nm,
                   "rc_loc_1_3_nm": rc_loc_1_3_nm,
                   'pr_tm_name': pr_tm_name,
                   'sido_sigungu_1_pr':sido_sigungu_1_pr,
                   'sido_sigungu_2_pr':sido_sigungu_2_pr,
                   'sido_sigungu_3_pr':sido_sigungu_3_pr
                   })


@csrf_exempt
def getAiResult_like2(request):
    # test 결과에 쓸 지역 이름을 갖고온다.
    user_id = request.session.get('user')
    users = Users.objects.get(userid=user_id)
    airesult = Ai_Result()
    airesult.userid = users
    userid = airesult.userid

    sido_sigungu = Survey.objects.filter(writer_id=users).values('sido_sigungu_1', 'sido_sigungu_2', 'sido_sigungu_3')
    sido_sigungu_1, sido_sigungu_2, sido_sigungu_3 = list(sido_sigungu.get().values())  # 유저가 설문에서 답한 여행지역 3곳

    sido_sigungu_1_up = list(Com_Code.objects.filter(com_code=sido_sigungu_1).values('upper_code').get().values())[0]
    sido_sigungu_1_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_1_up).values('code_nm').get().values())[0]
    sido_sigungu_1_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_1).values('code_nm').get().values())[0]
    sido_sigungu_2_up = list(Com_Code.objects.filter(com_code=sido_sigungu_2).values('upper_code').get().values())[0]
    sido_sigungu_2_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_2_up).values('code_nm').get().values())[0]
    sido_sigungu_2_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_2).values('code_nm').get().values())[0]
    sido_sigungu_3_up = list(Com_Code.objects.filter(com_code=sido_sigungu_3).values('upper_code').get().values())[0]
    sido_sigungu_3_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_3_up).values('code_nm').get().values())[0]
    sido_sigungu_3_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_3).values('code_nm').get().values())[0]

    # 추천받은 여행지역1_1,1_2,1_3 필터링작업 -> 각각 3개씩 여행지 출력!
    # 추천받은 여행지역 1_1,1_2,1_3 나눠줌
    rc_loc_2 = Ai_Result.objects.filter(userid=users).values('rc_loc_2_1', 'rc_loc_2_2', 'rc_loc_2_3')
    rc_loc_2_1, rc_loc_2_2, rc_loc_2_3 = list(rc_loc_2.get().values())
    rc_loc_2_1_nm = list(Com_Code.objects.filter(id=rc_loc_2_1).values('code_nm').get().values())[0]
    rc_loc_2_2_nm = list(Com_Code.objects.filter(id=rc_loc_2_2).values('code_nm').get().values())[0]
    rc_loc_2_3_nm = list(Com_Code.objects.filter(id=rc_loc_2_3).values('code_nm').get().values())[0]

    # 추천받은 지역의 시도 이름들
    rc_loc_1_upper = list(Com_Code.objects.filter(id=rc_loc_2_1).values('upper_code').get().values())[0]
    rc_loc_1_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_1_upper).values('code_nm').get().values())[0]

    rc_loc_2_upper = list(Com_Code.objects.filter(id=rc_loc_2_2).values('upper_code').get().values())[0]
    rc_loc_2_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_2_upper).values('code_nm').get().values())[0]

    rc_loc_3_upper = list(Com_Code.objects.filter(id=rc_loc_2_3).values('upper_code').get().values())[0]
    rc_loc_3_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_3_upper).values('code_nm').get().values())[0]


    # 설문에서 테마id 가져오기
    temem = Survey.objects.filter(writer_id=users).values('com_code_tm_id')
    com_code_tm_id = list(temem.get().values())[0]
    com_code_tm_id_gr = list(Com_Code.objects.filter(id=com_code_tm_id).values('gr_code').get().values())[0]
    pr_tm_name = list(Com_Code.objects.filter(id=com_code_tm_id).values('code_nm').get().values())[0]
    
    # 추천받은 여행지역1의 여행지 3곳출력
    TripLocals1 = Tour_Spots.objects.values('id', 'name', 'add_detail', 'image_src', 'tel', 'hits', 'com_code_rg_id',
                                            'com_code_rg_id__com_code', 'com_code_rg_id__code_nm',
                                            'com_code_rg_id__upper_code', 'com_code_tm_id',
                                            'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                            'com_code_tm_id__upper_code').filter(com_code_rg_id=rc_loc_2_1,
                                                                                 com_code_tm_id__gr_code=com_code_tm_id_gr).order_by(
        'hits')[0:3]

    TripLocals2 = Tour_Spots.objects.values('id', 'name', 'add_detail', 'image_src', 'tel', 'hits', 'com_code_rg_id',
                                            'com_code_rg_id__com_code', 'com_code_rg_id__code_nm',
                                            'com_code_rg_id__upper_code', 'com_code_tm_id',
                                            'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                            'com_code_tm_id__upper_code').filter(com_code_rg_id=rc_loc_2_2,
                                                                                 com_code_tm_id__gr_code=com_code_tm_id_gr).order_by(
        'hits')[0:3]

    TripLocals3 = Tour_Spots.objects.values('id', 'name', 'add_detail', 'image_src', 'tel', 'hits', 'com_code_rg_id',
                                            'com_code_rg_id__com_code', 'com_code_rg_id__code_nm',
                                            'com_code_rg_id__upper_code', 'com_code_tm_id',
                                            'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                            'com_code_tm_id__upper_code').filter(com_code_rg_id=rc_loc_2_3,
                                                                                 com_code_tm_id__gr_code=com_code_tm_id_gr).order_by(
        'hits')[0:3]

    return render(request, "home/chucheon_home_like2.html",
                  {'TripLocals1': TripLocals1, 'TripLocals2': TripLocals2, 'TripLocals3': TripLocals3,
                   'rc_loc_1_pr_nm': rc_loc_1_pr_nm, 'rc_loc_2_pr_nm': rc_loc_2_pr_nm, 'rc_loc_3_pr_nm': rc_loc_3_pr_nm,
                   "sido_sigungu_1_nm": sido_sigungu_1_nm,
                   "sido_sigungu_2_nm": sido_sigungu_2_nm,
                   "sido_sigungu_3_nm": sido_sigungu_3_nm,
                   "rc_loc_2_1_nm": rc_loc_2_1_nm,
                   "rc_loc_2_2_nm": rc_loc_2_2_nm,
                   "rc_loc_2_3_nm": rc_loc_2_3_nm,
                   'pr_tm_name': pr_tm_name,
                   'sido_sigungu_1_pr':sido_sigungu_1_pr,
                   'sido_sigungu_2_pr':sido_sigungu_2_pr,
                   'sido_sigungu_3_pr':sido_sigungu_3_pr
                   })


@csrf_exempt
def getAiResult_like3(request):
    # test 결과에 쓸 지역 이름을 갖고온다.
    user_id = request.session.get('user')
    users = Users.objects.get(userid=user_id)
    airesult = Ai_Result()
    airesult.userid = users
    userid = airesult.userid

    sido_sigungu = Survey.objects.filter(writer_id=users).values('sido_sigungu_1', 'sido_sigungu_2', 'sido_sigungu_3')
    sido_sigungu_1, sido_sigungu_2, sido_sigungu_3 = list(sido_sigungu.get().values())  # 유저가 설문에서 답한 여행지역 3곳

    sido_sigungu_1_up = list(Com_Code.objects.filter(com_code=sido_sigungu_1).values('upper_code').get().values())[0]
    sido_sigungu_1_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_1_up).values('code_nm').get().values())[0]
    sido_sigungu_1_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_1).values('code_nm').get().values())[0]
    sido_sigungu_2_up = list(Com_Code.objects.filter(com_code=sido_sigungu_2).values('upper_code').get().values())[0]
    sido_sigungu_2_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_2_up).values('code_nm').get().values())[0]
    sido_sigungu_2_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_2).values('code_nm').get().values())[0]
    sido_sigungu_3_up = list(Com_Code.objects.filter(com_code=sido_sigungu_3).values('upper_code').get().values())[0]
    sido_sigungu_3_pr = list(Com_Code.objects.filter(com_code=sido_sigungu_3_up).values('code_nm').get().values())[0]
    sido_sigungu_3_nm = list(Com_Code.objects.filter(com_code=sido_sigungu_3).values('code_nm').get().values())[0]

    # 추천받은 여행지역1_1,1_2,1_3 필터링작업 -> 각각 3개씩 여행지 출력!
    # 추천받은 여행지역 1_1,1_2,1_3 나눠줌
    rc_loc_3 = Ai_Result.objects.filter(userid=users).values('rc_loc_3_1', 'rc_loc_3_2', 'rc_loc_3_3')
    rc_loc_3_1, rc_loc_3_2, rc_loc_3_3 = list(rc_loc_3.get().values())
    rc_loc_3_1_nm = list(Com_Code.objects.filter(id=rc_loc_3_1).values('code_nm').get().values())[0]
    rc_loc_3_2_nm = list(Com_Code.objects.filter(id=rc_loc_3_2).values('code_nm').get().values())[0]
    rc_loc_3_3_nm = list(Com_Code.objects.filter(id=rc_loc_3_3).values('code_nm').get().values())[0]
    
    # 추천받은 지역의 시도 이름들
    rc_loc_1_upper = list(Com_Code.objects.filter(id=rc_loc_3_1).values('upper_code').get().values())[0]
    rc_loc_1_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_1_upper).values('code_nm').get().values())[0]

    rc_loc_2_upper = list(Com_Code.objects.filter(id=rc_loc_3_2).values('upper_code').get().values())[0]
    rc_loc_2_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_2_upper).values('code_nm').get().values())[0]

    rc_loc_3_upper = list(Com_Code.objects.filter(id=rc_loc_3_3).values('upper_code').get().values())[0]
    rc_loc_3_pr_nm = list(Com_Code.objects.filter(com_code=rc_loc_3_upper).values('code_nm').get().values())[0]

    # 설문에서 테마id 가져오기
    temem = Survey.objects.filter(writer_id=users).values('com_code_tm_id')
    com_code_tm_id = list(temem.get().values())[0]
    com_code_tm_id_gr = list(Com_Code.objects.filter(id=com_code_tm_id).values('gr_code').get().values())[0]
    pr_tm_name = list(Com_Code.objects.filter(id=com_code_tm_id).values('code_nm').get().values())[0]

    # 추천받은 여행지역1의 여행지 3곳출력
    TripLocals1 = Tour_Spots.objects.values('id', 'name', 'add_detail', 'image_src', 'tel', 'hits', 'com_code_rg_id',
                                            'com_code_rg_id__com_code', 'com_code_rg_id__code_nm',
                                            'com_code_rg_id__upper_code', 'com_code_tm_id',
                                            'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                            'com_code_tm_id__upper_code').filter(com_code_rg_id=rc_loc_3_1,
                                                                                 com_code_tm_id__gr_code=com_code_tm_id_gr).order_by(
        'hits')[0:3]

    TripLocals2 = Tour_Spots.objects.values('id', 'name', 'add_detail', 'image_src', 'tel', 'hits', 'com_code_rg_id',
                                            'com_code_rg_id__com_code', 'com_code_rg_id__code_nm',
                                            'com_code_rg_id__upper_code', 'com_code_tm_id',
                                            'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                            'com_code_tm_id__upper_code').filter(com_code_rg_id=rc_loc_3_2,
                                                                                 com_code_tm_id__gr_code=com_code_tm_id_gr).order_by(
        'hits')[0:3]

    TripLocals3 = Tour_Spots.objects.values('id', 'name', 'add_detail', 'image_src', 'tel', 'hits', 'com_code_rg_id',
                                            'com_code_rg_id__com_code', 'com_code_rg_id__code_nm',
                                            'com_code_rg_id__upper_code', 'com_code_tm_id',
                                            'com_code_tm_id__com_code', 'com_code_tm_id__code_nm',
                                            'com_code_tm_id__upper_code').filter(com_code_rg_id=rc_loc_3_3,
                                                                                 com_code_tm_id__gr_code=com_code_tm_id_gr).order_by(
        'hits')[0:3]

    return render(request, "home/chucheon_home_like3.html",
                  {'TripLocals1': TripLocals1, 'TripLocals2': TripLocals2, 'TripLocals3': TripLocals3,
                   'rc_loc_1_pr_nm': rc_loc_1_pr_nm, 'rc_loc_2_pr_nm': rc_loc_2_pr_nm, 'rc_loc_3_pr_nm': rc_loc_3_pr_nm,
                   "sido_sigungu_1_nm": sido_sigungu_1_nm,
                   "sido_sigungu_2_nm": sido_sigungu_2_nm,
                   "sido_sigungu_3_nm": sido_sigungu_3_nm,
                   "rc_loc_3_1_nm": rc_loc_3_1_nm,
                   "rc_loc_3_2_nm": rc_loc_3_2_nm,
                   "rc_loc_3_3_nm": rc_loc_3_3_nm,
                   'pr_tm_name': pr_tm_name,
                   'sido_sigungu_1_pr':sido_sigungu_1_pr,
                   'sido_sigungu_2_pr':sido_sigungu_2_pr,
                   'sido_sigungu_3_pr':sido_sigungu_3_pr
                   })

