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

from .models import Match, Player, Team, Registerd, Registered, Table, Reported, PlayerResult, TeamResult, ClassWinRate, Blog
from django.contrib.auth.mixins import LoginRequiredMixin

def leader():
    return ["エルフ","ロイヤル", "ウィッチ", "ドラゴン", "ヴァンパイア", "ネクロマンサー", "ビショップ", "ネメシス"]

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
    for t in Team.objects.all().order_by('-point')[:5]:

        name = t.team_name
        point = t.point
        grosspoint = t.grosspoint
        dic1[name] = {"name": name, "point": point, "grosspoint": grosspoint}
# 勝利数トップ5を抽出
    for p in Player.objects.all().order_by('-win')[:5]:

        name = p.player_name
        win = p.win
        lose = p.lose
        dic2[name] = {"name": name, "win": win, "lose": lose}

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

def listdate(request):
        m = Match.objects.all().filter(match_table_release=True)
        dic = {}
        for x in m:
            id = x.id
            d = x.match_date

            dic[id] = strdate(d)

        context = {'dic': dic}

        return render(request, 'attendance/listdate.html', context)



def list(request, date):
    t = Table.objects.filter(date=Match.objects.filter(pk=date).get())

    dic = {}
    c = 0
    for x in t:
        c+=1
        try:
            r1 = Registered.objects.filter(date=x.date, team=x.team1).order_by('-pk').first()
            r2 = Registered.objects.filter(date=x.date, team=x.team2).order_by('-pk').first()
            order1 = [r1.first, r1.second, r1.third, r1.fourth, r1.fifth, r1.hoketsu]
            order2 = [r2.first, r2.second, r2.third, r2.fourth, r2.fifth, r2.hoketsu]
            dic[str(c)+x.team1.team_name+" vs "+x.team2.team_name] = {x.team1.team_name: order1, x.team2.team_name: order2}
        except AttributeError:
            dic[str(c)] = {c: "", c: ""}
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
    m = Match.objects.all()
    match_instance = m.get(pk=int(date))
    Registered.objects.create(date=match_instance, team=request.user, first=first, second=second, third=third, fourth= fourth, fifth=fifth, hoketsu=hoketsu)

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
    m = Match.objects.all()#あとでfilterつける
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

    def register(date):
        team = request.user
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

        dics = [{"player": first, "leader": firstl, "winlose": firstwl},
               {"player": second, "leader": secondl, "winlose": secondwl},
               {"player": third, "leader": thirdl, "winlose": thirdwl},
               {"player": fourth, "leader": fourthl, "winlose": fourthwl},
               {"player": fifth, "leader": fifthl, "winlose": fifthwl}]
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
    #PlayerResultとTeamResultに追加
        teamp = 0
        for d in dics:
            PlayerResult.objects.create(date = date, player = Player.objects.filter(player_name=d["player"]).order_by('-pk').first(), leader = d["leader"], wl = d["winlose"])
            if d["winlose"] == "win" :
                teamp+=1

        TeamResult.objects.create(date=date, team=team, point = teamp)
        for m in Match.objects.all():
            try:
                for t in Table.objects.filter(date=m):
                    point1 = TeamResult.objects.filter(date=m, team=t.team1.team_name).order_by("-pk").first().point
                    team1 = t.team1.team_name
                    point2 = TeamResult.objects.filter(date=m, team=t.team2.team_name).order_by("-pk").first().point
                    team2 = t.team2.team_name
                    x1 = Team.objects.filter(team_name = team1).order_by("-pk").first()
                    x1.grosspoint += point1

                    x2 = Team.objects.filter(team_name=team2).order_by("-pk").first()
                    x2.grosspoint += point2
                    if point1 >= 3:
                        x1.point += 1
                    else:
                        x2.point += 1
                    x1.save()
                    x2.save()
            except AttributeError:
                pass

        # Teamポイントの初期化
        for t in Team.objects.all():
            t.point = 0
            t.grosspoint = 0
            t.save()

        #Playerポイントの初期化
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
    #ClassWinRateの初期化
        for c in ClassWinRate.objects.all():
            c.win = 0
            c.lose = 0
            c.rate = 0
            c.total = 0
            c.save()

        # point,grosspointの再計算
        for m in Match.objects.all():
            try:
                for t in Table.objects.filter(date=m):
                        point1 = TeamResult.objects.filter(date=m, team=t.team1.team_name).order_by("-pk").first().point
                        team1 = t.team1.team_name
                        point2 = TeamResult.objects.filter(date=m, team=t.team2.team_name).order_by("-pk").first().point
                        team2 = t.team2.team_name
                        x1 = Team.objects.filter(team_name=team1).order_by("-pk").first()
                        x1.grosspoint += point1

                        x2 = Team.objects.filter(team_name=team2).order_by("-pk").first()
                        x2.grosspoint += point2
                        if point1 >= 3:
                            x1.point += 1
                        else:
                            x2.point += 1
                        x1.save()
                        x2.save()
            except AttributeError:
                    pass

    # プレイヤーオブジェクトにクラス別戦績を追加
            for p in Player.objects.all():
                try:
                            pr = PlayerResult.objects.filter(date=m, player=p).order_by("-pk").first()
                            if pr.leader=="エルフ":
                                if pr.wl == "win":
                                    p.e_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="エルフ").get()
                                    c.win += 1
                                    c.save()


                                else:
                                    p.e_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="エルフ").get()
                                    c.lose += 1
                                    c.save()


                            elif pr.leader == "ネメシス":
                                if pr.wl == "win":
                                    p.nm_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ネメシス").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.nm_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ネメシス").get()
                                    c.lose += 1
                                    c.save()

                            elif pr.leader == "ドラゴン":
                                if pr.wl == "win":
                                    p.d_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ドラゴン").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.d_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ドラゴン").get()
                                    c.lose += 1
                                    c.save()

                            elif pr.leader == "ビショップ":
                                if pr.wl == "win":
                                    p.b_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ビショップ").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.b_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ビショップ").get()
                                    c.lose += 1
                                    c.save()

                            elif pr.leader == "ロイヤル":
                                if pr.wl == "win":
                                    p.r_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ロイヤル").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.r_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ロイヤル").get()
                                    c.lose += 1
                                    c.save()

                            elif pr.leader == "ヴァンパイア":
                                if pr.wl == "win":
                                    p.v_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ヴァンパイア").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.v_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ヴァンパイア").get()
                                    c.lose += 1
                                    c.save()

                            elif pr.leader == "ウィッチ":
                                if pr.wl == "win":
                                    p.w_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ウィッチ").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.w_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ウィッチ").get()
                                    c.lose += 1
                                    c.save()

                            else:
                                if pr.wl == "win":
                                    p.nc_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ネクロマンサー").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.nc_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ネクロマンサー").get()
                                    c.lose += 1
                                    c.save()

                except AttributeError:
                        pass

        for c in ClassWinRate.objects.all():
           try:
                total = c.win+c.lose
                c.rate = c.win/total*100
                c.total = c.win + c.lose
                c.save()

           except   ZeroDivisionError:
               pass

    s_threading = threading.Thread(target=register(date))
    s_threading.start()

    return render(request, 'attendance/report_request.html')

def match_result(request):
    dicts = {}
    dic = {}
    for m in Match.objects.all():
            for t in Table.objects.filter(date=m):
                try:
                    point1 = TeamResult.objects.filter(date=m, team=t.team1.team_name).order_by("-pk").first().point
                    team1 = t.team1.team_name
                    point2 = TeamResult.objects.filter(date=m, team=t.team2.team_name).order_by("-pk").first().point
                    team2 = t.team2.team_name
                    dic[team1+" vs "+team2] = {"team1": team1, "point1": point1,"team2":team2,"point2": point2}
                except AttributeError:
                    pass
            date = strdate(m.match_date)
            dicts[date] = dic
            dic = {}

    return render(request, 'attendance/match_result.html', {'dicts': dicts})