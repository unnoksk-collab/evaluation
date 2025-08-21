from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Rank model
class Rank(models.Model):
    name = models.CharField("ランク名", max_length=50)
    required_score = models.IntegerField("必要スコア")
    class Meta:
        ordering = ['required_score']
    def __str__(self):
        return self.name

# 1. TopCategory
class TopCategory(models.Model):
    name = models.CharField("大カテゴリ名", max_length=100, unique=True)
    def __str__(self):
        return self.name

# 2. SkillCategory
class SkillCategory(models.Model):
    top_category = models.ForeignKey(TopCategory, on_delete=models.CASCADE, verbose_name="大カテゴリ")
    name = models.CharField("スキルカテゴリ名", max_length=100, unique=True)
    def __str__(self):
        return f"{self.top_category.name} - {self.name}"

# 3. EvaluationItem
class EvaluationItem(models.Model):
    skill_category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, verbose_name="スキルカテゴリ")
    name = models.CharField("評価項目名", max_length=255)
    max_score = models.IntegerField("満点")
    def __str__(self):
        return self.name

# Editor profile
class Editor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="ユーザー")
    total_score = models.IntegerField("合計スコア", default=0)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="現在のランク")
    def __str__(self):
        return self.user.username

    # ★★★ This function has been corrected ★★★
    def update_rank_and_score(self):
        # Find all scores related to this editor through the Evaluation model
        scores = EvaluationItemScore.objects.filter(evaluation__editor=self)
        total = sum(s.score for s in scores)
        self.total_score = total
        
        new_rank = Rank.objects.filter(required_score__lte=self.total_score).order_by('-required_score').first()
        self.rank = new_rank
        self.save()

# Evaluation session model
class Evaluation(models.Model):
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE, verbose_name="評価対象の編集者")
    evaluator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="評価者")
    evaluated_at = models.DateTimeField("評価日", default=timezone.now)
    def __str__(self):
        return f"{self.editor.user.username} - {self.evaluated_at.strftime('%Y-%m-%d')}"

# Individual evaluation score
class EvaluationItemScore(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, verbose_name="評価セッション")
    item = models.ForeignKey(EvaluationItem, on_delete=models.CASCADE, verbose_name="評価項目")
    score = models.IntegerField("スコア", default=0)
    comment = models.TextField("コメント", blank=True)
    def __str__(self):
        # 何も表示しないように空の文字列を返す
        return ""
    

# Signal to automatically update the total score
@receiver(post_save, sender=EvaluationItemScore)
def update_editor_score(sender, instance, **kwargs):
    instance.evaluation.editor.update_rank_and_score()