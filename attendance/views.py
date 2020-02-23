#フォーム作成https://arakan-pgm-ai.hatenablog.com/entry/2019/02/14/090000

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from . import forms
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
import threading
from threading import Thread
from django.contrib.auth.decorators import user_passes_test
from .models import Match, Player, Team, Registered, Table, Reported, PlayerResult, TeamResult, ClassWinRate, Blog, Season, Tournament, Past
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone
def leader():
    return ["不戦勝/不戦敗","エルフ","ロイヤル", "ウィッチ", "ドラゴン", "ヴァンパイア", "ネクロマンサー", "ビショップ", "ネメシス"]

def season():
    s = Season.objects.order_by('-pk').first()
    return s.season

def strdate(d):
    year = d.year
    month = d.month
    day = d.day
    return str(year) + "/" + str(month) + "/" + str(day)




def home(request):
# チームポイント順で並び替えて上位チームを選抜
    dic1 = {}
    dic2 = {}
    dic3 = {}
    dic4 = {}
#get top5 teams
    for t in Team.objects.all().filter(season=season()).order_by('-point', '-gp'):
        name = t.team_name
        point = t.point
        grosspoint = t.grosspoint
        penalty = t.penalty
        dic1[name] = {"name": name, "point": point, "grosspoint": grosspoint, "penalty": penalty}
# 勝利数トップ10を抽出
    for p in Player.objects.all().filter(season=season()).order_by('-win','lose')[:10]:
        name = p.player_name
        win = p.win
        lose = p.lose
        team = p.team.team_name
        dic2[name] = {"name": name,  "team": team+".png", "win": win, "lose": lose}
# リーダーごとの勝利数を回収
    for c in ClassWinRate.objects.filter(season=season()).all():
        name = c.leader
        rate = c.rate
        total = c.total
        dic3[name] = {"name": name, "rate": rate, "total": total}
#ブログ内容を回収
    for b in Blog.objects.all():
        title = b.title
        context = b.context
        dic4[title]= {"title": title, "context": context}

    return render(request, 'home.html', {"dic1": dic1, "dic2": dic2, "dic3": dic3, "dic4": dic4})

def user (request):
    return render(request, 'attendance/user.html')

def logout(request):
    return render(request, 'logout.html')

def final(request):
    t = Tournament.objects.all().filter(season=season()).get()
    dic = {"team1": t.team1, "team2": t.team2, "team3": t.team3, "team4": t.team4, "team5": t.team5, "team6": t.team6, "team7": t.team7, "team8": t.team8,
           "quauter1": t.quauter1, "quauter2": t.quauter2, "quauter3":t.quauter3, "quauter4": t.quauter4,
           "semi1": t.semi1, "semi2": t.semi2,"winner": t.winner, "season": t.season}
    return render(request, 'attendance/final.html', {"dic": dic})

def listdate(request):
        m = Match.objects.all().filter(season=season()).filter(match_table_release=True)
        dic = {}
        for x in m:
            id = x.id
            d = x.match_date

            dic[id] = strdate(d)

        context = {'dic': dic}

        return render(request, 'attendance/listdate.html', context)



# def list(request, date):
#     t = Table.objects.filter(season=season()).filter(date=Match.objects.filter(pk=date).get())
#
#     dic = {}
#     c = 0
#     for x in t:
#         c+=1
#         try:
#             r1 = Registered.objects.filter(date=x.date, team=x.team1).order_by('-pk').first()
#             r2 = Registered.objects.filter(date=x.date, team=x.team2).order_by('-pk').first()
#             order1 = [r1.first, r1.second, r1.third, r1.fourth, r1.fifth, r1.hoketsu]
#             order2 = [r2.first, r2.second, r2.third, r2.fourth, r2.fifth, r2.hoketsu]
#             dic[str(c)+":"+x.team1.team_name+" vs "+x.team2.team_name] = {x.team1.team_name: order1, x.team2.team_name: order2}
#         except AttributeError:
#             dic[str(c)] = {c: "", c: ""}
#
#
#
#     return render(request, 'attendance/table.html', {'dic': dic})

def listmake(request, date):
    if Match.objects.filter(pk=date).get().match_table_release == True:
        t = Table.objects.filter(season=season()).filter(date=Match.objects.filter(pk=date).get())
        dic = {}
        c = 0
        for x in t:
            c+=1
            try:
                r1 = Registered.objects.filter(date=x.date, team=x.team1).order_by('-pk').first()
                order1 = [r1.first, r1.second, r1.third, r1.fourth, r1.fifth, r1.hoketsu]
            except AttributeError:
                order1 = ["###未提出###", "###未提出###", "###未提出###", "###未提出###", "###未提出###", "###未提出###"]

            try:
                r2 = Registered.objects.filter(date=x.date, team=x.team2).order_by('-pk').first()
                order2 = [r2.first, r2.second, r2.third, r2.fourth, r2.fifth, r2.hoketsu]
            except AttributeError:
                order2 = ["###未提出###", "###未提出###", "###未提出###", "###未提出###", "###未提出###", "###未提出###"]

            first = ["一番手", order1[0], order2[0]]
            second = ["二番手", order1[1], order2[1]]
            third = ["三番手", order1[2], order2[2]]
            fourth = ["四番手", order1[3], order2[3]]
            fifth=["五番手", order1[4], order2[4]]
            hoketsu=["補欠", order1[5], order2[5]]
            dic[str(c)+":"+x.team1.team_name+" vs "+x.team2.team_name] = [first, second, third, fourth, fifth, hoketsu]
    return render(request, 'attendance/table.html', {'dic': dic})


@login_required
def index(request):
    m = Match.objects.all().filter(season=season()).filter(register_release=True)
    dic = {}
    for x in m:
        id = x.id
        d = x.match_date
        dic[id] = strdate(d)

    context = {'dic': dic}
    return render(request, 'attendance/index.html', context)

@login_required
def date(request, date):
    x = Team.objects.filter(season=season()).filter(team_name=request.user).get()
    mylist = []
    for m in x.player_set.all():
        mylist.append(m.player_name)
    return render(request, 'attendance/date.html', {"date": date, "team_member": mylist})
@login_required
def result(request, date):
    # フォーム送信された値を受け取る
    first = request.GET.get('first')
    second = request.GET.get('second')
    third = request.GET.get('third')
    fourth = request.GET.get('fourth')
    fifth = request.GET.get('fifth')
    hoketsu = request.GET.get('hoketsu')
    #データベースに変更を加えるぉ
    m = Match.objects.all().filter(season=season())
    match_instance = m.get(pk=int(date))
    time_now = timezone.now()
    Registered.objects.create(date=match_instance, team=request.user, first=first, second=second, third=third, fourth= fourth, fifth=fifth, hoketsu=hoketsu, regist_date=time_now)

    r = Registered.objects.filter(team=request.user)
    m = Match.objects.all().filter(season=season())
    dic = {}
    for x in m:  # Matchをforで回して、そのなかで一番古い登録データからfirst,...を抜く。未登録の場合は..
        try:
            order = r.filter(date=x).order_by('-pk').first()
            first = order.first
            second = order.second
            third = order.third
            fourth = order.fourth
            fifth = order.fifth
            hoketsu = order.hoketsu

            d = x.match_date
            DDD = strdate(d)
            dic[DDD] = {'一番手': first, '二番手': second, '三番手': third, '四番手': fourth, '五番手': fifth,
                           'リザーバー': hoketsu}
        except AttributeError:
            pass

    return render(request, 'attendance/result.html', {'dic': dic})

@login_required
def reportdate(request):
    m = Match.objects.all().filter(season=season())
    dic = {}
    for x in m:
        id = x.id
        d = x.match_date

        dic[id] = strdate(d)

    context = {'dic': dic}

    return render(request, 'attendance/reportdate.html', context)
@login_required
def report(request, date):

    r = Registered.objects.filter(team = request.user).filter(date=Match.objects.all().filter(season=season()).filter(pk=date).get()).order_by('-pk').first()
    mylist = [r.first, r.second, r.third, r.fourth, r.fifth, r.hoketsu]
    context = {'team_member': mylist, 'winlose': ["win", "lose"], 'leader': leader(), 'date': date}
    return render(request, 'attendance/report.html', context)
@login_required
def report_register(request, date):

    team = request.user.username
    date = Match.objects.filter(season=season()).filter(pk=date).order_by('-pk').first()

    first = request.GET.get('first')
    second = request.GET.get('second')
    third = request.GET.get('third')
    fourth = request.GET.get('fourth')
    fifth = request.GET.get('fifth')

    firstl = request.GET.get('firstl')
    secondl = request.GET.get('secondl')
    thirdl = request.GET.get('thirdl')
    fourthl = request.GET.get('fourthl')
    fifthl = request.GET.get('fifthl')

    firstwl = request.GET.get('firstwl')
    secondwl = request.GET.get('secondwl')
    thirdwl = request.GET.get('thirdwl')
    fourthwl = request.GET.get('fourthwl')
    fifthwl = request.GET.get('fifthwl')

    dics = [{"player": first, "leader": firstl, "winlose": firstwl,"team": team},
           {"player": second, "leader": secondl, "winlose": secondwl,"team": team},
           {"player": third, "leader": thirdl, "winlose": thirdwl,"team": team},
           {"player": fourth, "leader": fourthl, "winlose": fourthwl,"team": team},
           {"player": fifth, "leader": fifthl, "winlose": fifthwl,"team": team}]
# レポートに登録
    Reported.objects.create(
    date=date,
    team=team,

    first = first,
    second = second,
    third = third,
    fourth = fourth,
    fifth = fifth,

    firstl = firstl,
    secondl =secondl,
    thirdl = thirdl,
    fourthl = fourthl,
    fifthl = fifthl,

    firstwl = firstwl,
    secondwl = secondwl,
    thirdwl = thirdwl,
    fourthwl = fourthwl,
    fifthwl = fifthwl,
    )
    # Teamポイントの初期化(updateへ移動)
    # for t in Team.objects.all().filter(season=season()):
    #     t.point = 0
    #     t.grosspoint = 0
    #     t.save()

#PlayerResultとTeamResultに追加
    teamp = 0
    for d in dics:
        PlayerResult.objects.create(date = date, player = Player.objects.filter(player_name=d["player"],team=Team.objects.all().filter(team_name=d["team"]).get()).order_by('-pk').first(), leader = d["leader"], wl = d["winlose"])
        if d["winlose"] == "win" :
            teamp+=1

    TeamResult.objects.create(date=date, team=team, point = teamp)
    # for m in Match.objects.all():
    #     try:
    #          for t in Table.objects.filter(date=m):
    #             point1 = TeamResult.objects.filter(date=m, team=t.team1.team_name).order_by("-pk").first().point
    #             team1 = t.team1.team_name
    #             point2 = TeamResult.objects.filter(date=m, team=t.team2.team_name).order_by("-pk").first().point
    #             team2 = t.team2.team_name
    #             x1 = Team.objects.filter(team_name=team1).order_by("-pk").first()
    #             x1.grosspoint += point1
    #
    #             x2 = Team.objects.filter(team_name=team2).order_by("-pk").first()
    #             x2.grosspoint += point2
    #             if point1 >= 3:
    #                 x1.point += 1
    #             else:
    #                 x2.point += 1
    #             x1.save()
    #             x2.save()
    #     except AttributeError:
    #          pass


    #Playerポイントの初期化（ここから先はupdatへ）
#     for p in Player.objects.all().filter(season=season()):
#         p.win = 0
#         p.lose = 0
#         p.e_win = 0
#         p.e_lose = 0
#         p.nm_win = 0
#         p.nm_lose = 0
#         p.d_win = 0
#         p.d_lose = 0
#         p.b_win = 0
#         p.b_lose = 0
#         p.r_win = 0
#         p.r_lose = 0
#         p.v_win = 0
#         p.v_lose = 0
#         p.w_win = 0
#         p.w_lose = 0
#         p.nc_win = 0
#         p.nc_lose = 0
#         p.save()
# #ClassWinRateの初期化
#     for c in ClassWinRate.objects.all().filter(season=season()):
#         c.win = 0
#         c.lose = 0
#         c.rate = 0
#         c.total = 0
#         c.save()
#
#     # point,grosspointの再計算
#     for m in Match.objects.all().filter(season=season()):
#
#         for t in Table.objects.filter(date=m):
#             try:
#                     point1 = TeamResult.objects.filter(date=m, team=t.team1.team_name).order_by("-pk").first().point
#                     team1 = t.team1.team_name
#                     point2 = TeamResult.objects.filter(date=m, team=t.team2.team_name).order_by("-pk").first().point
#                     team2 = t.team2.team_name
#                     x1 = Team.objects.filter(team_name=team1).order_by("-pk").first()
#                     x1.grosspoint += point1
#
#                     x2 = Team.objects.filter(team_name=team2).order_by("-pk").first()
#                     x2.grosspoint += point2
#                     if point1 >= 3:
#                         x1.point += 1
#                     else:
#                         x2.point += 1
#                     x1.save()
#                     x2.save()
#             except AttributeError:
#                     pass
#
# # プレイヤーオブジェクトにクラス別戦績を追加
#         for p in Player.objects.all().filter(season=season()):
#             try:
#                         pr = PlayerResult.objects.filter(date=m, player=p).order_by("-pk").first()
#                         if pr.leader=="エルフ":
#                             if pr.wl == "win":
#                                 p.e_win += 1
#                                 p.win += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="エルフ").get()
#                                 c.win += 1
#                                 c.save()
#
#
#                             else:
#                                 p.e_lose += 1
#                                 p.lose += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="エルフ").get()
#                                 c.lose += 1
#                                 c.save()
#
#
#                         elif pr.leader == "ネメシス":
#                             if pr.wl == "win":
#                                 p.nm_win += 1
#                                 p.win += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ネメシス").get()
#                                 c.win += 1
#                                 c.save()
#
#                             else:
#                                 p.nm_lose += 1
#                                 p.lose += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ネメシス").get()
#                                 c.lose += 1
#                                 c.save()
#
#                         elif pr.leader == "ドラゴン":
#                             if pr.wl == "win":
#                                 p.d_win += 1
#                                 p.win += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ドラゴン").get()
#                                 c.win += 1
#                                 c.save()
#
#                             else:
#                                 p.d_lose += 1
#                                 p.lose += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ドラゴン").get()
#                                 c.lose += 1
#                                 c.save()
#
#                         elif pr.leader == "ビショップ":
#                             if pr.wl == "win":
#                                 p.b_win += 1
#                                 p.win += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ビショップ").get()
#                                 c.win += 1
#                                 c.save()
#
#                             else:
#                                 p.b_lose += 1
#                                 p.lose += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ビショップ").get()
#                                 c.lose += 1
#                                 c.save()
#
#                         elif pr.leader == "ロイヤル":
#                             if pr.wl == "win":
#                                 p.r_win += 1
#                                 p.win += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ロイヤル").get()
#                                 c.win += 1
#                                 c.save()
#
#                             else:
#                                 p.r_lose += 1
#                                 p.lose += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ロイヤル").get()
#                                 c.lose += 1
#                                 c.save()
#
#                         elif pr.leader == "ヴァンパイア":
#                             if pr.wl == "win":
#                                 p.v_win += 1
#                                 p.win += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ヴァンパイア").get()
#                                 c.win += 1
#                                 c.save()
#
#                             else:
#                                 p.v_lose += 1
#                                 p.lose += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ヴァンパイア").get()
#                                 c.lose += 1
#                                 c.save()
#
#                         elif pr.leader == "ウィッチ":
#                             if pr.wl == "win":
#                                 p.w_win += 1
#                                 p.win += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ウィッチ").get()
#                                 c.win += 1
#                                 c.save()
#
#                             else:
#                                 p.w_lose += 1
#                                 p.lose += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ウィッチ").get()
#                                 c.lose += 1
#                                 c.save()
#                         elif pr.leader == "ネクロマンサー":
#                         # else:
#                             if pr.wl == "win":
#                                 p.nc_win += 1
#                                 p.win += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ネクロマンサー").get()
#                                 c.win += 1
#                                 c.save()
#
#                             else:
#                                 p.nc_lose += 1
#                                 p.lose += 1
#                                 p.save()
#                                 c = ClassWinRate.objects.filter(season=season()).filter(leader="ネクロマンサー").get()
#                                 c.lose += 1
#                                 c.save()
#                         else:
#                             pass
#
#             except AttributeError:
#                     pass
#
#     for c in ClassWinRate.objects.all().filter(season=season()):
#        try:
#             total = c.win+c.lose
#             c.rate = c.win/total*100
#             c.total = c.win + c.lose
#             c.save()
#
#        except   ZeroDivisionError:
#            pass
#
    return render(request, 'attendance/report_request.html')

def match_result(request):
    # dicts = {}
    # dic = {}
    # for m in Match.objects.all().filter(season=season()):
    #         for t in Table.objects.filter(date=m):
    #             try:
    #                 point1 = TeamResult.objects.filter(date=m, team=t.team1.team_name).order_by("-pk").first().point
    #                 team1 = t.team1.team_name
    #                 point2 = TeamResult.objects.filter(date=m, team=t.team2.team_name).order_by("-pk").first().point
    #                 team2 = t.team2.team_name
    #                 dic[team1+" vs "+team2] = {"team1": team1, "point1": point1,"team2":team2,"point2": point2}
    #             except AttributeError:
    #                 pass
    #         date = strdate(m.match_date)
    #         dicts[date] = dic
    #         dic = {}
    #
    # return render(request, 'attendance/match_result.html', {'dicts': dicts})
    dicts = {}
    dic = {}
    for m in Match.objects.all().filter(season=season()).order_by("pk"):
            for t in Table.objects.filter(date=m):
                try:
                    point1 = TeamResult.objects.filter(date=m, team=t.team1.team_name).order_by("-pk").first().point
                except AttributeError:
                    point1 = "###未登録###"
                try:
                    point2 = TeamResult.objects.filter(date=m, team=t.team2.team_name).order_by("-pk").first().point
                except AttributeError:
                    point2 = "###未登録###"

                e=0
                try:
                    sum = point1+point2
                    if sum ==5:
                        pass
                    else:
                        e=1
                except TypeError:
                    e=1


                team1 = t.team1.team_name
                team2 = t.team2.team_name
                dic[team1+" vs "+team2] = {"team1": team1, "point1": point1,"team2":team2,"point2": point2, "error": e}

            date = strdate(m.match_date)
            dicts[date] = dic
            dic = {}

    return render(request, 'attendance/match_result.html', {'dicts': dicts})


def schedule(request):
    return render(request,'attendance/schedule.html')

@user_passes_test(lambda u: u.is_superuser)
def check(request):
    t = Table.objects.filter(season=season()).filter(date=Match.objects.all().order_by('-pk').first())
    m = strdate(Match.objects.all().order_by('-pk').first().match_date)
    dic = {}
    c = 0
    for x in t:
        c+=1
        try:
            r1 = Registered.objects.filter(date=x.date, team=x.team1).order_by('-pk').first()
            order1 = [r1.first, r1.second, r1.third, r1.fourth, r1.fifth, r1.hoketsu]
        except AttributeError:
            order1 = ["###未提出###", "###未提出###", "###未提出###", "###未提出###", "###未提出###", "###未提出###"]

        try:
            r2 = Registered.objects.filter(date=x.date, team=x.team2).order_by('-pk').first()
            order2 = [r2.first, r2.second, r2.third, r2.fourth, r2.fifth, r2.hoketsu]
        except AttributeError:
            order2 = ["###未提出###", "###未提出###", "###未提出###", "###未提出###", "###未提出###", "###未提出###"]

        first = ["一番手", order1[0], order2[0]]
        second = ["二番手", order1[1], order2[1]]
        third = ["三番手", order1[2], order2[2]]
        fourth = ["四番手", order1[3], order2[3]]
        fifth=["五番手", order1[4], order2[4]]
        hoketsu=["補欠", order1[5], order2[5]]
        dic[str(c)+":"+x.team1.team_name+" vs "+x.team2.team_name] = [first, second, third, fourth, fifth, hoketsu]
    largedict = {m: dic}


    return render(request, 'attendance/check.html', {'largedict': largedict})

# def update(request):
#
#     #Playerポイントの初期化
#     for p in Player.objects.all().filter(season=season()):
#         p.win = 0
#         p.lose = 0
#         p.e_win = 0
#         p.e_lose = 0
#         p.nm_win = 0
#         p.nm_lose = 0
#         p.d_win = 0
#         p.d_lose = 0
#         p.b_win = 0
#         p.b_lose = 0
#         p.r_win = 0
#         p.r_lose = 0
#         p.v_win = 0
#         p.v_lose = 0
#         p.w_win = 0
#         p.w_lose = 0
#         p.nc_win = 0
#         p.nc_lose = 0
#         p.save()
# #ClassWinRateの初期化
#     for c in ClassWinRate.objects.all().filter(season=season()):
#         c.win = 0
#         c.lose = 0
#         c.rate = 0
#         c.total = 0
#         c.save()
# # teamポイントの初期化
#     for t in Team.objects.all().filter(season=season()):
#         t.point = 0
#         t.grosspoint = 0
#         t.save()
#
#     # point,grosspointの再計算
#     for m in Match.objects.all().filter(season=season()):
# # teamポイント追加
#         for t in Table.objects.filter(date=m):
#             try:
#                     point1 = TeamResult.objects.filter(date=m, team=t.team1.team_name).order_by("-pk").first().point
#                     team1 = t.team1.team_name
#                     point2 = TeamResult.objects.filter(date=m, team=t.team2.team_name).order_by("-pk").first().point
#                     team2 = t.team2.team_name
#                     x1 = Team.objects.filter(team_name=team1).order_by("-pk").first()
#                     x1.grosspoint += point1
#
#                     x2 = Team.objects.filter(team_name=team2).order_by("-pk").first()
#                     x2.grosspoint += point2
#                     if point1 >= 3:
#                         x1.point += 1
#                     else:
#                         x2.point += 1
#                     x1.save()
#                     x2.save()
#             except AttributeError:
#                     pass
#
# # プレイヤーオブジェクトにクラス別戦績を追加
#         for p in Player.objects.all().filter(season=season()):
#             try:
#                     pr = PlayerResult.objects.filter(date=m, player=p).order_by("-pk").first()
#                     if pr.leader=="エルフ":
#                         if pr.wl == "win":
#                             p.e_win += 1
#                             p.win += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="エルフ").get()
#                             c.win += 1
#                             c.save()
#
#
#                         else:
#                             p.e_lose += 1
#                             p.lose += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="エルフ").get()
#                             c.lose += 1
#                             c.save()
#
#
#                     elif pr.leader == "ネメシス":
#                         if pr.wl == "win":
#                             p.nm_win += 1
#                             p.win += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ネメシス").get()
#                             c.win += 1
#                             c.save()
#
#                         else:
#                             p.nm_lose += 1
#                             p.lose += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ネメシス").get()
#                             c.lose += 1
#                             c.save()
#
#                     elif pr.leader == "ドラゴン":
#                         if pr.wl == "win":
#                             p.d_win += 1
#                             p.win += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ドラゴン").get()
#                             c.win += 1
#                             c.save()
#
#                         else:
#                             p.d_lose += 1
#                             p.lose += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ドラゴン").get()
#                             c.lose += 1
#                             c.save()
#
#                     elif pr.leader == "ビショップ":
#                         if pr.wl == "win":
#                             p.b_win += 1
#                             p.win += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ビショップ").get()
#                             c.win += 1
#                             c.save()
#
#                         else:
#                             p.b_lose += 1
#                             p.lose += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ビショップ").get()
#                             c.lose += 1
#                             c.save()
#
#                     elif pr.leader == "ロイヤル":
#                         if pr.wl == "win":
#                             p.r_win += 1
#                             p.win += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ロイヤル").get()
#                             c.win += 1
#                             c.save()
#
#                         else:
#                             p.r_lose += 1
#                             p.lose += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ロイヤル").get()
#                             c.lose += 1
#                             c.save()
#
#                     elif pr.leader == "ヴァンパイア":
#                         if pr.wl == "win":
#                             p.v_win += 1
#                             p.win += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ヴァンパイア").get()
#                             c.win += 1
#                             c.save()
#
#                         else:
#                             p.v_lose += 1
#                             p.lose += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ヴァンパイア").get()
#                             c.lose += 1
#                             c.save()
#
#                     elif pr.leader == "ウィッチ":
#                         if pr.wl == "win":
#                             p.w_win += 1
#                             p.win += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ウィッチ").get()
#                             c.win += 1
#                             c.save()
#
#                         else:
#                             p.w_lose += 1
#                             p.lose += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ウィッチ").get()
#                             c.lose += 1
#                             c.save()
#                     elif pr.leader == "ネクロマンサー":
#                     # else:
#                         if pr.wl == "win":
#                             p.nc_win += 1
#                             p.win += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ネクロマンサー").get()
#                             c.win += 1
#                             c.save()
#
#                         else:
#                             p.nc_lose += 1
#                             p.lose += 1
#                             p.save()
#                             c = ClassWinRate.objects.filter(season=season()).filter(leader="ネクロマンサー").get()
#                             c.lose += 1
#                             c.save()
#                     else:
#                         pass
#
#             except AttributeError:
#                     pass
#
#     for c in ClassWinRate.objects.all().filter(season=season()):
#        try:
#             total = c.win+c.lose
#             c.rate = c.win/total*100
#             c.total = c.win + c.lose
#             c.save()
#
#        except   ZeroDivisionError:
#            pass
#
#     return render(request, 'attendance/report_request.html')

def update(request):#チームポイントの集計
    #Playerポイントの初期化
    for t in Team.objects.all().filter(season=season()):
        t.point = 0
        t.grosspoint = 0
        t.save()

    for m in Match.objects.all().filter(season=season()):
        for t in Table.objects.filter(date=m):
            try:
                    point1 = TeamResult.objects.filter(date=m, team=t.team1.team_name).order_by("-pk").first().point
                    team1 = t.team1.team_name
                    point2 = TeamResult.objects.filter(date=m, team=t.team2.team_name).order_by("-pk").first().point
                    team2 = t.team2.team_name
                    x1 = Team.objects.filter(team_name=team1).order_by("-pk").first()
                    x1.grosspoint += point1

                    x2 = Team.objects.filter(team_name=team2).order_by("-pk").first()
                    x2.grosspoint += point2
                    if point1 >= 3:
                        x1.point += 3
                    else:
                        x2.point += 3
                    x1.save()
                    x2.save()
            except AttributeError:
                    pass

    for t in Team.objects.all():
        t.gp = t.grosspoint - t.penalty
        t.save()
    return render(request, 'attendance/report_request.html')



def update2(request):#プレイヤー勝敗数の集計
    for p in Player.objects.all().filter(season=season()):
        p.win = 0
        p.lose = 0
        p.e_win = 0
        p.e_lose = 0
        p.nm_win = 0
        p.nm_lose = 0
        p.d_win = 0
        p.d_lose = 0
        p.b_win = 0
        p.b_lose = 0
        p.r_win = 0
        p.r_lose = 0
        p.v_win = 0
        p.v_lose = 0
        p.w_win = 0
        p.w_lose = 0
        p.nc_win = 0
        p.nc_lose = 0
        p.save()

    for m in Match.objects.all().filter(season=season()):
        for p in Player.objects.all().filter(season=season()):
            try:
                pr = PlayerResult.objects.filter(date=m, player=p).order_by("-pk").first()
                if pr.wl == "win":
                    p.win += 1
                    p.save()
                else:
                    p.lose += 1
                    p.save()
            except AttributeError:
                pass




    return render(request, 'attendance/report_request.html')


def update3(request):#クラス勝率の計算
    for c in ClassWinRate.objects.all().filter(season=season()):
        c.win = 0
        c.lose = 0
        c.rate = 0
        c.total = 0
        c.save()


    for m in Match.objects.all().filter(season=season()):
        for p in Player.objects.all().filter(season=season()):
            try:
                    pr = PlayerResult.objects.filter(date=m, player=p).order_by("-pk").first()
                    if pr.leader=="エルフ":
                        if pr.wl == "win":
                            # p.e_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="エルフ").get()
                            c.win += 1
                            c.save()


                        else:
                            # p.e_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="エルフ").get()
                            c.lose += 1
                            c.save()


                    elif pr.leader == "ネメシス":
                        if pr.wl == "win":
                            # p.nm_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ネメシス").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.nm_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ネメシス").get()
                            c.lose += 1
                            c.save()

                    elif pr.leader == "ドラゴン":
                        if pr.wl == "win":
                            # p.d_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ドラゴン").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.d_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ドラゴン").get()
                            c.lose += 1
                            c.save()

                    elif pr.leader == "ビショップ":
                        if pr.wl == "win":
                            # p.b_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ビショップ").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.b_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ビショップ").get()
                            c.lose += 1
                            c.save()

                    elif pr.leader == "ロイヤル":
                        if pr.wl == "win":
                            # p.r_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ロイヤル").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.r_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ロイヤル").get()
                            c.lose += 1
                            c.save()

                    elif pr.leader == "ヴァンパイア":
                        if pr.wl == "win":
                            # p.v_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ヴァンパイア").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.v_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ヴァンパイア").get()
                            c.lose += 1
                            c.save()

                    elif pr.leader == "ウィッチ":
                        if pr.wl == "win":
                            # p.w_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ウィッチ").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.w_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ウィッチ").get()
                            c.lose += 1
                            c.save()
                    elif pr.leader == "ネクロマンサー":
                    # else:
                        if pr.wl == "win":
                            # p.nc_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ネクロマンサー").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.nc_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(season=season()).filter(leader="ネクロマンサー").get()
                            c.lose += 1
                            c.save()
                    else:
                        pass

            except AttributeError:
                    pass

    for c in ClassWinRate.objects.all().filter(season=season()):
       try:
            total = c.win+c.lose
            c.rate = c.win/total*100
            c.total = total
            c.save()
       except   ZeroDivisionError:
           pass
    return render(request, 'attendance/report_request.html')

def past(request):#過去の戦績の参照
    dict = {}
    for p in Past.objects.all():
        dic ={}

        dic["team1"] = p.team1
        dic["team2"] = p.team2
        dic["team3"] = p.team3
        dic["team4"] = p.team4
        dic["team5"] = p.team5
        dic["team6"] = p.team6

        dic["player1"] = p.player1
        dic["r1"]  = p.r1
        dic["player2"] = p.player2
        dic["r2"]  = p.r2
        dic["player3"] = p.player3
        dic["r3"]  = p.r3
        dic["player4"] = p.player4
        dic["r4"] = p.r4
        dic["player5"] = p.player5
        dic["r5"]  = p.r5
        dic["player6"]  = p.player6
        dic["r6"]  = p.r6
        dic["player7"] = p.player7
        dic["r7"]  = p.r7
        dic["player8"] = p.player8
        dic["r8"]  = p.r8
        dic["player9"] = p.player9
        dic["r9"]  = p.r9
        dic["player10"] = p.player10
        dic["r10"]  = p.r10
        dict[p.season]=dic

    return render(request, 'attendance/past.html', {"dict":dict})

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('user')
    template_name = 'attendance/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context

@user_passes_test(lambda u: u.is_superuser)
def check(request):
    m = Match.objects.all().filter(season=season()).all()
    dic = {}
    for x in m:
        id = x.id
        d = x.match_date

        dic[id] = strdate(d)

    context = {'dic': dic}

    return render(request, 'attendance/listdatesu.html', context)

@user_passes_test(lambda u: u.is_superuser)
def listsu(request, date):
        m = Match.objects.filter(pk=date).get()
        if m.match_table_release == True:
            table_release = "checked"
        else:
            table_release = ""
        t = Table.objects.filter(season=season()).filter(date=Match.objects.filter(pk=date).get())
        ldic = {}
        dic = {}
        c = 0
        for x in t:
            c+=1
            try:
                r1 = Registered.objects.filter(date=x.date, team=x.team1).order_by('-pk').first()
                order1 = [r1.first, r1.second, r1.third, r1.fourth, r1.fifth, r1.hoketsu]
            except AttributeError:
                order1 = ["###未提出###", "###未提出###", "###未提出###", "###未提出###", "###未提出###", "###未提出###"]

            try:
                r2 = Registered.objects.filter(date=x.date, team=x.team2).order_by('-pk').first()
                order2 = [r2.first, r2.second, r2.third, r2.fourth, r2.fifth, r2.hoketsu]
            except AttributeError:
                order2 = ["###未提出###", "###未提出###", "###未提出###", "###未提出###", "###未提出###", "###未提出###"]

            first = ["一番手", order1[0], order2[0]]
            second = ["二番手", order1[1], order2[1]]
            third = ["三番手", order1[2], order2[2]]
            fourth = ["四番手", order1[3], order2[3]]
            fifth=["五番手", order1[4], order2[4]]
            hoketsu=["補欠", order1[5], order2[5]]
            dic[str(c)+":"+x.team1.team_name+" vs "+x.team2.team_name] = [first, second, third, fourth, fifth, hoketsu]
        ldic["dic"] = dic
        ldic["table_release"] = table_release
        ldic["date"] = date
        return render(request, 'attendance/tablesu.html', {'ldic': ldic})
@login_required
def member(request):
    p = Player.objects.filter(team = Team.objects.filter(team_name=request.user).get()).order_by("win")
    li = []
    for q in p:
        li.append([q.player_name, q.win, q.lose])
    return render(request, 'attendance/member.html', {'dic': li})

@user_passes_test(lambda u: u.is_superuser, date)

def release_changed(request, date):
    m = Match.objects.filter(pk=date).get()
    if request.GET["table_release"] == "on":
        m.match_table_release = True
        state = "公開中、オーダー提出はできない状態"
        m.register_release = False
    else:
        m.match_table_release = False
        state = "非公開、オーダー提出は可能な状態"

        m.register_release = True

    m.save()
    dic = {}
    dic["day"] = strdate(m.match_date)
    dic["state"]= state


    return render(request, 'attendance/release_changed.html', {"dic":dic})

