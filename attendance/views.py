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
from .models import Match, Player, Team, Registered, Table, Reported, PlayerResult, TeamResult, ClassWinRate, Blog, Tournament, Past, Season, JCGrank, Other_tournament
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
from django.db.models import F
from django.db.models import Value

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
    for t in Team.objects.all().order_by('-point', '-gp'):
        name = t.team_name
        point = t.point
        gp = t.gp
        penalty = t.penalty
        dic1[name] = { "id": name+".png","name": name, "point": point, "grosspoint": gp, "penalty": penalty}
# 勝利数トップ10を抽出
    for n, p in enumerate(Player.objects.all().filter(visible = True).order_by('-win','lose')[:10]):
        name = p.player_name
        win = p.win
        lose = p.lose
        team = p.team.team_name
        dic2[name] = {"name": name,  "team": team+".png", "win": win, "lose": lose}
        if n == 9:
            for x in Player.objects.all().filter(win = win).filter(lose=lose).filter(visible = True):
                if x.player_name in dic2.keys():
                    pass
                else:
                    name = x.player_name
                    win = x.win
                    lose = x.lose
                    team = x.team.team_name
                    dic2[name] = {"name": name, "team": team + ".png", "win": win, "lose": lose}

 #試合数5以上かつ勝率順
    # for n, p in enumerate(Player.objects.all().filter(visible = True).raw(
    #     """SELECT * FROM (SELECT *, rank() OVER(order by rate DESC) AS jun FROM (SELECT *, CAST(CAST(win AS real) / CAST(sum AS real)*100 AS INT64) AS rate  FROM (SELECT *, win + lose AS sum FROM attendance_player WHERE sum >= 6)))"""
    # )):
    #     name = p.player_name
    #     win = p.rate
    #     lose = p.sum
    #     team = p.team.team_name
    #     dic2[name] = {"name": name,  "team": team+".png", "win": win, "lose": lose}
    #     if n == 9:
    #         for x in Player.objects.all().filter(win = win).filter(lose=lose).filter(visible = True):
    #             if x.player_name in dic2.keys():
    #                 pass
    #             else:
    #                 name = x.player_name
    #                 win = x.win
    #                 lose = x.lose
    #                 team = x.team.team_name
    #                 dic2[name] = {"name": name, "team": team + ".png", "win": lose, "lose": win}

#試合数5以上かつ勝率順,Fを使って
    # for n, p in enumerate(Player.objects.all().extra(select={'sum': "win + lose"}).extra(select={'rate':"CAST(CAST(win AS real)/(CAST(lose AS real) + CAST(win AS real))*100 AS INT64)"}).order_by('-rate')[:10]):
    #     name = p.player_name
    #     win = p.sum
    #     lose = p.rate
    #     team = p.team.team_name
    #     dic2[name] = {"name": name,  "team": team+".png", "win": win, "lose": lose}
        # if n == 9:
        #     for x in Player.objects.all().filter(win = win).filter(lose=lose).filter(visible = True):
        #         if x.player_name in dic2.keys():
        #             pass
        #         else:
        #             name = x.player_name
        #             win = x.win
        #             lose = x.lose
        #             team = x.team.team_name
        #             dic2[name] = {"name": name, "team": team + ".png", "win": win, "lose": lose}

# リーダーごとの勝利数を回収
    for c in ClassWinRate.objects.all():
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
    t = Tournament.objects.all().get()
    dicp = {"team1": t.team1+".png", "team2": t.team2+".png", "team3": t.team3+".png", "team4": t.team4+".png", "team5": t.team5+".png", "team6": t.team6+".png",
           "quauter1": t.quauter1+".png", "quauter2": t.quauter2+".png",
           "semi1": t.semi1+".png", "semi2": t.semi2+".png","winner": t.winner+".png"}
    dicn = {"team1": t.team1, "team2": t.team2, "team3": t.team3, "team4": t.team4, "team5": t.team5, "team6": t.team6,
           "quauter1": t.quauter1, "quauter2": t.quauter2,
           "semi1": t.semi1, "semi2": t.semi2,"winner": t.winner}
    dic  = {"dicp": dicp, "dicn": dicn}
    return render(request, 'attendance/final.html', {"dic": dic})

def listdate(request):
        m = Match.objects.all().filter(match_table_release=True)
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
        t = Table.objects.filter(date=Match.objects.filter(pk=date).get())
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
    m = Match.objects.all().filter(register_release=True)
    dic = {}
    for x in m:
        id = x.id
        d = x.match_date
        dic[id] = strdate(d)

    context = {'dic': dic}
    return render(request, 'attendance/index.html', context)

@login_required
def date(request, date):
    x = Team.objects.filter(team_name=request.user).get()
    mylist = []
    for m in Player.objects.all().filter(team = x).filter(visible=True):
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
    m = Match.objects.all()
    match_instance = m.get(pk=int(date))
    time_now = timezone.now()
    Registered.objects.create(date=match_instance, team=request.user, first=first, second=second, third=third, fourth= fourth, fifth=fifth, hoketsu=hoketsu, regist_date=time_now)

    r = Registered.objects.filter(team=request.user)
    m = Match.objects.all()
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
    m = Match.objects.all()
    dic = {}
    for x in m:
        id = x.id
        d = x.match_date

        dic[id] = strdate(d)

    context = {'dic': dic}

    return render(request, 'attendance/reportdate.html', context)
@login_required
def report(request, date):

    r = Registered.objects.filter(team = request.user).filter(date=Match.objects.all().filter(pk=date).get()).order_by('-pk').first()
    mylist = [r.first, r.second, r.third, r.fourth, r.fifth, r.hoketsu]
    context = {'team_member': mylist, 'winlose': ["win", "lose"], 'leader': leader(), 'date': date}
    return render(request, 'attendance/report.html', context)
@login_required
def report_register(request, date):

    team = request.user.username
    date = Match.objects.filter(pk=date).order_by('-pk').first()

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
    try:
        pastrep = Reported.objects.all().filter(date = date).filter(team = team).first()
        for pastpr in PlayerResult.objects.all().filter(rp = pastrep):
            pastpr.delete()
        for pasttr in TeamResult.objects.all().filter(rp = pastrep):
            pasttr.delete()
    except AttributeError:
        pass
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
    rp = Reported.objects.all().order_by("-pk").first()
#PlayerResultとTeamResultに追加
    teamp = 0
    for d in dics:
        PlayerResult.objects.create(date = date, player = Player.objects.filter(player_name=d["player"],team=Team.objects.all().filter(team_name=d["team"]).get()).order_by('-pk').first(), leader = d["leader"], wl = d["winlose"], rp = rp)
        if d["winlose"] == "win" :
            teamp+=1

    TeamResult.objects.create(date=date, team=team, point = teamp, rp = rp)
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
    for m in Match.objects.all().order_by("pk"):
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
    t = Table.objects.filter(date=Match.objects.all().order_by('-pk').first())
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
    for t in Team.objects.all():
        t.point = 0
        t.grosspoint = 0
        t.save()

    for m in Match.objects.all():
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
    for p in Player.objects.all():
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

    for m in Match.objects.all():
        for p in Player.objects.all():
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
    for c in ClassWinRate.objects.all():
        c.win = 0
        c.lose = 0
        c.rate = 0
        c.total = 0
        c.save()


    for m in Match.objects.all():
        for p in Player.objects.all():
            try:
                    pr = PlayerResult.objects.filter(date=m, player=p).order_by("-pk").first()
                    if pr.leader=="エルフ":
                        if pr.wl == "win":
                            # p.e_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="エルフ").get()
                            c.win += 1
                            c.save()


                        else:
                            # p.e_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="エルフ").get()
                            c.lose += 1
                            c.save()


                    elif pr.leader == "ネメシス":
                        if pr.wl == "win":
                            # p.nm_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ネメシス").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.nm_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ネメシス").get()
                            c.lose += 1
                            c.save()

                    elif pr.leader == "ドラゴン":
                        if pr.wl == "win":
                            # p.d_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ドラゴン").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.d_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ドラゴン").get()
                            c.lose += 1
                            c.save()

                    elif pr.leader == "ビショップ":
                        if pr.wl == "win":
                            # p.b_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ビショップ").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.b_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ビショップ").get()
                            c.lose += 1
                            c.save()

                    elif pr.leader == "ロイヤル":
                        if pr.wl == "win":
                            # p.r_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ロイヤル").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.r_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ロイヤル").get()
                            c.lose += 1
                            c.save()

                    elif pr.leader == "ヴァンパイア":
                        if pr.wl == "win":
                            # p.v_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ヴァンパイア").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.v_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ヴァンパイア").get()
                            c.lose += 1
                            c.save()

                    elif pr.leader == "ウィッチ":
                        if pr.wl == "win":
                            # p.w_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ウィッチ").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.w_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ウィッチ").get()
                            c.lose += 1
                            c.save()
                    elif pr.leader == "ネクロマンサー":
                    # else:
                        if pr.wl == "win":
                            # p.nc_win += 1
                            # p.win += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ネクロマンサー").get()
                            c.win += 1
                            c.save()

                        else:
                            # p.nc_lose += 1
                            # p.lose += 1
                            # p.save()
                            c = ClassWinRate.objects.filter(leader="ネクロマンサー").get()
                            c.lose += 1
                            c.save()
                    else:
                        pass

            except AttributeError:
                    pass

    for c in ClassWinRate.objects.all():
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
    for p in Past.objects.all().order_by("-season"):
        dic ={}

        dic["team1"] = p.team1 + ".png"
        dic["team2"] = p.team2 + ".png"
        dic["team3"] = p.team3 + ".png"
        dic["team4"] = p.team4 + ".png"
        dic["team5"] = p.team5 + ".png"
        dic["team6"] = p.team6 + ".png"

        dic["teamname1"] = p.team1
        dic["teamname2"] = p.team2
        dic["teamname3"] = p.team3
        dic["teamname4"] = p.team4
        dic["teamname5"] = p.team5
        dic["teamname6"] = p.team6

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

    return render(request,  'attendance/past.html', {"dict":dict})

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
    m = Match.objects.all()
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
    t = Table.objects.filter(date=Match.objects.filter(pk=date).get())
    ldic = {}
    dic = {}
    c = 0
    for x in t:
        c += 1
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
        fifth = ["五番手", order1[4], order2[4]]
        hoketsu = ["補欠", order1[5], order2[5]]
        dic[str(c) + ":" + x.team1.team_name + " vs " + x.team2.team_name] = [first, second, third, fourth, fifth,
                                                                              hoketsu]
    ldic["dic"] = dic
    ldic["table_release"] = table_release
    ldic["date"] = date
    return render(request, 'attendance/tablesu.html', {'ldic': ldic})


@login_required
def member(request):
    p = Player.objects.filter(team=Team.objects.filter(team_name=request.user).get()).order_by("win")
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
    dic["state"] = state

    return render(request, 'attendance/release_changed.html', {"dic": dic})


def team_page(request, team_name):
    dict = {}
    dict["team"]=team_name + ".png"
    dict["team_name"] = team_name
    t = Team.objects.all().filter(team_name=team_name).get()
    dict["start"]=t.start
    dict["words"]=t.words
    dict["leader"] = t.leader
    dict["los"] = []
    dict["others"]=[]
    for p in Past.objects.all():
        season = p.season
        if t.team_name == p.team1:
            dict["los"].append([season, p.team1, "優勝"])
        elif t.team_name == p.team2:
            dict["los"].append([season, p.team2, "準優勝"])
        elif t.team_name == p.team3:
            dict["los"].append([season, p.team3, "4位"])
        elif t.team_name == p.team4:
            dict["los"].append([season, p.team4, "4位"])
        elif t.team_name == p.team5:
            dict["los"].append([season, p.team5, "6位"])
        elif t.team_name == p.team6:
            dict["los"].append([season, p.team6, "6位"])
    counter = 0
    total = 0
    dic = {}

    for p in Player.objects.all().filter(team=Team.objects.all().filter(team_name=team_name).get()).filter(visible=True):
        try:
            j = JCGrank.objects.all().filter(JCGID=p.playerid).first()
            xx = [p.twitter[1:], j.first, j.second, j.fourth]
            total += j.total
        except:
            xx = [p.twitter[1:],0,0,0]
        losli = []
        pc = 1
        for ps in Past.objects.all():
            if p.player_name == ps.player1:
                losli.append(["1",ps.season, ps.place1])
            elif p.player_name == ps.player2:
                losli.append(["1",ps.season, ps.place2])
            elif p.player_name == ps.player3:
                losli.append(["1",ps.season, ps.place3])
            elif p.player_name == ps.player4:
                losli.append(["1",ps.season, ps.place4])
            elif p.player_name == ps.player5:
                losli.append(["1",ps.season, ps.place5])
            elif p.player_name == ps.player6:
                losli.append(["1",ps.season, ps.place6])
            elif p.player_name == ps.player7:
                losli.append(["1",ps.season, ps.place7])
            elif p.player_name == ps.player8:
                losli.append(["1",ps.season, ps.place8])
            elif p.player_name == ps.player9:
                losli.append(["1",ps.season, ps.place9])
            elif p.player_name == ps.player10:
                losli.append(["1",ps.season, ps.place10])
            pc+=1
        o_li = []
        for o in Other_tournament.objects.all().filter(player=p):
            o_li.append(["1", o.tournament_name, o.Rank])

        dic[p.player_name] = [xx, losli,pc,o_li]
        counter+=1
    dict["counter"] = counter
    dict["total"] = total
    dict["dic"]=dic
    return render(request, 'team_page.html', dict)

def jcgrank(request):
    jp = JCGrank.objects.all().order_by("-total").values_list("total", flat = True)[::-1][::-1]
    mli = sorted(set(jp), key=jp.index)
    li = []
    for m in mli:
        if m >= 10:
            for j in JCGrank.objects.all().filter(total=m):
                dic = {}
                dic["player_name"]=j.player_name
                dic["first"]= j.first
                dic["second"] = j.second
                dic["fourth"] = j.fourth
                dic["total"]=j.total
                try:
                    dic["team"] = Player.objects.all().filter(playerid = j.JCGID).filter(visible=True).first().team.team_name +".png"
                    dic["team_name"] = Player.objects.all().filter(playerid = j.JCGID).filter(visible=True).first().team.team_name
                except:
                    dic["team"] = "-.png"
                    dic["team_name"] = "-"
                li.append(dic)
    dict = {"li": li}
    lastest_reload = Season.objects.all().order_by("-pk").first().lastest_reload
    return render(request, 'jcgrank.html', {"dict":dict, "last_reload": lastest_reload})

def team_page_edit(request):
    # t = Team.objects.all().filter(team=request.user).get()
    return render(request,"attendance/team_page_edit.html")

def team_page_edit_done(request):
    t = Team.objects.all().filter(team_name=request.user).get()
    t.leader = request.GET.get('leader')
    t.start = request.GET.get('establish')
    t.words = request.GET.get('msg')
    t.save()
    return render(request,"attendance/team_page_change_done.html")

def team_page_home(request):
    teamli = []
    for t in Team.objects.all():
        li = []
        li.append(t.team_name)
        li.append(t.team_name+".png")
        teamli.append(li)
        
    return render(request, 'team_page_home.html', {"teamli":teamli})