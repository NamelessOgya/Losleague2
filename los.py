from attendance.models import Match, Player, Team, Registered, Table, Reported, PlayerResult, TeamResult, ClassWinRate, Blog, Season, Tournament, Past
def season():
    s = Season.objects.order_by('-pk').first()
    return s.season

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
                x1.grosspoint += point1-point2

                x2 = Team.objects.filter(team_name=team2).order_by("-pk").first()
                x2.grosspoint += point2-point1
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

#####################2nd###################################
noleader = 0
namelist = []
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
                    noleader += 1
                    namelist.append(pr.player.player_name)
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

#print(noleader)
#print(namelist)