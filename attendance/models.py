
from django.db import models
from django.utils import timezone



class Team(models.Model):
    team_name = models.CharField(max_length=100)
    point = models.IntegerField(verbose_name='勝ち点', blank=True, null=True, default=0)
    grosspoint = models.IntegerField(verbose_name='得点差(ペナルティ除く)', blank=True, null=True, default=0)
    penalty = models.IntegerField(verbose_name='ペナルティ(正の数でつけてください)', blank=True, null=True, default=0)
    gp = models.IntegerField(verbose_name='得点差-ペナルティ', blank=True, null=True, default=0)
    start = models.CharField(max_length=100, default="",null=True)
    words = models.TextField(max_length=500, default="",null=True)
    leader = models.CharField(max_length=100, default="",null=True)

    def __str__(self):
        return self.team_name

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=100)
    visible = models.BooleanField(verbose_name='在籍(脱退時外す)', default=True)
    win = models.IntegerField(verbose_name='win', blank=True, null=True, default=0)
    lose = models.IntegerField(verbose_name='lose', blank=True, null=True, default=0)
    e_win = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    e_lose = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    nm_win = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    nm_lose = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    d_win = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    d_lose = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    b_win = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    b_lose = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    r_win = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    r_lose = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    v_win = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    v_lose = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    w_win = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    w_lose = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    nc_win = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    nc_lose = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    playerid = models.IntegerField(verbose_name='ID', blank=True, null=True, default=0)
    twitter = models.CharField(max_length=100)

    def __str__(self):
        return self.player_name

class Match(models.Model):
    match_date = models.DateTimeField('date published')
    match_table_release = models.BooleanField(verbose_name='マッチング表の公表', default=False)
    register_release = models.BooleanField(verbose_name='登録ページの公表', default=False,)

    def __str__(self):
        return str(self.match_date)

class Registered(models.Model):
    date = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.CharField(max_length=100, default="")

    first = models.CharField(max_length=100, default="")#登録メンバー
    second = models.CharField(max_length=100, default="")
    third = models.CharField(max_length=100, default="")
    fourth = models.CharField(max_length=100, default="")
    fifth = models.CharField(max_length=100, default="")
    hoketsu = models.CharField(max_length=100, default="")
    regist_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
            return str(self.date)+"/"+self.team


class Table(models.Model):
    date = models.ForeignKey(Match, on_delete=models.CASCADE)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2")

    def __str__(self):
            return self.team1.team_name+"/"+self.team2.team_name+"/"+str(self.date)

class Reported(models.Model):
    date = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.CharField(max_length=100, default="")

    first = models.CharField(max_length=100, default="")#登録メンバー
    second = models.CharField(max_length=100, default="")
    third = models.CharField(max_length=100, default="")
    fourth = models.CharField(max_length=100, default="")
    fifth = models.CharField(max_length=100, default="")

    firstl = models.CharField(max_length=100, default="")  # 登録メンバー
    secondl = models.CharField(max_length=100, default="")
    thirdl = models.CharField(max_length=100, default="")
    fourthl = models.CharField(max_length=100, default="")
    fifthl = models.CharField(max_length=100, default="")

    firstwl = models.CharField(max_length=100, default="")  # 登録メンバー
    secondwl = models.CharField(max_length=100, default="")
    thirdwl = models.CharField(max_length=100, default="")
    fourthwl = models.CharField(max_length=100, default="")
    fifthwl = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.date) + "/" + self.team

class PlayerResult(models.Model):
    date = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    leader = models.CharField(max_length=100, default="")
    wl = models.CharField(max_length=100, default="")
    rp = models.ForeignKey(Reported, on_delete=models.CASCADE, default=None)



class TeamResult(models.Model):
    date = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.CharField(max_length=100, default="")
    point = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    rp = models.ForeignKey(Reported, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return str(self.date) + "/" + self.team

class ClassWinRate(models.Model):
    leader = models.CharField(max_length=100, default="")
    win = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    lose = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    rate = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    total = models.IntegerField(verbose_name='', blank=True, null=True, default=0)

    def __str__(self):
        return self.leader

class Blog(models.Model):
    title = models.CharField(max_length=500, default="")
    context = models.TextField(max_length=500, default="")

    def __str__(self):
        return self.title

class Tournament(models.Model):
    team1 = models.CharField(max_length=100, default="-")
    team2 = models.CharField(max_length=100, default="-")
    team3 = models.CharField(max_length=100, default="-")
    team4 = models.CharField(max_length=100, default="-")
    team5 = models.CharField(max_length=100, default="-")
    team6 = models.CharField(max_length=100, default="-")
    team7 = models.CharField(max_length=100, default="-")
    team8 = models.CharField(max_length=100, default="-")

    quauter1 = models.CharField(max_length=100, default="-")
    quauter2 = models.CharField(max_length=100, default="-")
    quauter3 = models.CharField(max_length=100, default="-")
    quauter4 = models.CharField(max_length=100, default="-")
    semi1 = models.CharField(max_length=100, default="-")
    semi2 = models.CharField(max_length=100, default="-")

    winner = models.CharField(max_length=100, default="-")

class Past(models.Model):
    season = models.IntegerField(verbose_name='season', blank=True, null=True, default=0)
    team1 = models.CharField(max_length=100, default="-")
    team2 = models.CharField(max_length=100, default="-")
    team3 = models.CharField(max_length=100, default="-")
    team4 = models.CharField(max_length=100, default="-")
    team5 = models.CharField(max_length=100, default="-")
    team6 = models.CharField(max_length=100, default="-")
    player1 = models.CharField(max_length=100, default="-")
    r1= models.CharField(max_length=100, default="-")
    place1 = models.CharField(max_length=100, default="-")
    player2 = models.CharField(max_length=100, default="-")
    r2= models.CharField(max_length=100, default="-")
    place2 = models.CharField(max_length=100, default="-")
    player3 = models.CharField(max_length=100, default="-")
    r3 = models.CharField(max_length=100, default="-")
    place3 = models.CharField(max_length=100, default="-")
    player4 = models.CharField(max_length=100, default="-")
    r4 = models.CharField(max_length=100, default="-")
    place4 = models.CharField(max_length=100, default="-")
    player5 = models.CharField(max_length=100, default="-")
    r5 = models.CharField(max_length=100, default="-")
    place5 = models.CharField(max_length=100, default="-")
    player6 = models.CharField(max_length=100, default="-")
    r6 =  models.CharField(max_length=100, default="-")
    place6 = models.CharField(max_length=100, default="-")
    player7 = models.CharField(max_length=100, default="-")
    r7 = models.CharField(max_length=100, default="-")
    place7 = models.CharField(max_length=100, default="-")
    player8 = models.CharField(max_length=100, default="-")
    r8 = models.CharField(max_length=100, default="-")
    place8 = models.CharField(max_length=100, default="-")
    player9 = models.CharField(max_length=100, default="-")
    r9 = models.CharField(max_length=100, default="-")
    place9 = models.CharField(max_length=100, default="-")
    player10 = models.CharField(max_length=100, default="-")
    r10 = models.CharField(max_length=100, default="-")
    place10 = models.CharField(max_length=100, default="-")
    def __str__(self):
        return "LOSリーグシーズン"+str(self.season)

class Season(models.Model):
    season = models.IntegerField(verbose_name='season', blank=True, null=True, default=0)
    lastest_reload = models.CharField(max_length=100, default="-")

    def __str__(self):
        return "現在のシーズン"

class JCGrank(models.Model):
    player_name = models.CharField(max_length=100, default="-")
    JCGID = models.IntegerField(verbose_name='JCGID', blank=True, null=True, default=0)
    first = models.IntegerField(verbose_name='1st', blank=True, null=True, default=0)
    second = models.IntegerField(verbose_name='2nd', blank=True, null=True, default=0)
    fourth = models.IntegerField(verbose_name='4th', blank=True, null=True, default=0)
    total = models.IntegerField(verbose_name='total', blank=True, null=True, default=0)
    def __str__(self):
        return self.player_name

class Other_tournament(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament_name = models.CharField(max_length=100, default="-")
    Rank = models.CharField(max_length=100, default="-")
    prize = models.IntegerField(verbose_name='prize', blank=True, null=True, default=0)

    def __str__(self):
        return self.player.player_name+self.tournament_name+str(self.prize)
