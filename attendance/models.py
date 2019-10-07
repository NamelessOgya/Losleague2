
from django.db import models



class Team(models.Model):
    team_name = models.CharField(max_length=100)
    point = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    grosspoint = models.IntegerField(verbose_name='', blank=True, null=True, default=0)


    def __str__(self):
        return self.team_name

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=100)
    win = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
    lose = models.IntegerField(verbose_name='', blank=True, null=True, default=0)
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

    def __str__(self):
            return str(self.date)+"/"+self.team


class Registerd(models.Model):
    date = models.CharField(max_length=100, default="")

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

    def __str__(self):
        return str(self.date) + "/" + self.player


class TeamResult(models.Model):
    date = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.CharField(max_length=100, default="")
    point = models.IntegerField(verbose_name='', blank=True, null=True, default=0)

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
    title = models.CharField(max_length=100, default="")
    context = models.CharField(max_length=200, default="")










