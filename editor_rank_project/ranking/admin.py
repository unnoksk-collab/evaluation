from django.contrib import admin
from django import forms
from .models import (
    Rank, Editor, TopCategory, SkillCategory,
    EvaluationItem, EvaluationItemScore, Evaluation
)

class EvaluationItemScoreForm(forms.ModelForm):
    class Meta:
        model = EvaluationItemScore
        fields = '__all__'
    def clean_score(self):
        score = self.cleaned_data.get('score')
        item = self.cleaned_data.get('item')
        if score is not None and item and (score > item.max_score or score < 0):
            raise forms.ValidationError(f"スコアは0〜{item.max_score}点で入力してください。")
        return score

class EvaluationItemScoreInline(admin.TabularInline):
    model = EvaluationItemScore
    form = EvaluationItemScoreForm
    fields = ('get_item_name', 'get_item_max_score', 'score', 'comment')
    readonly_fields = ('get_item_name', 'get_item_max_score')
    extra = 0
    can_delete = False

    def get_item_name(self, obj):
        return obj.item.name
    get_item_name.short_description = '評価項目'
    
    def get_item_max_score(self, obj):
        return obj.item.max_score
    get_item_max_score.short_description = '満点'

    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return True

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    inlines = [EvaluationItemScoreInline]
    list_display = ('editor', 'evaluator', 'evaluated_at')
    autocomplete_fields = ['editor']
    
    def response_add(self, request, obj, post_url_continue=None):
        items = EvaluationItem.objects.all()
        for item in items:
            EvaluationItemScore.objects.get_or_create(
                evaluation=obj, 
                item=item,
                defaults={'score': 0}
            )
        return super().response_add(request, obj, post_url_continue)

@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    search_fields = ['user__username']

admin.site.register(Rank)
admin.site.register(TopCategory)
admin.site.register(SkillCategory)
admin.site.register(EvaluationItem)