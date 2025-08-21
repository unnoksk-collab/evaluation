from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Editor, Rank, EvaluationItemScore, EvaluationItem
from collections import defaultdict

@login_required
def dashboard(request):
    editor = get_object_or_404(Editor, user=request.user)
    
    # --- データ取得・整理 ---
    score_history = EvaluationItemScore.objects.filter(evaluation__editor=editor).select_related(
        'item__skill_category__top_category'
    ).order_by('item__skill_category__top_category', 'item__skill_category', 'id')

    dashboard_data = []
    structured_scores = defaultdict(lambda: defaultdict(list))
    for score in score_history:
        structured_scores[score.item.skill_category.top_category.name][score.item.skill_category.name].append(score)

    all_items = EvaluationItem.objects.select_related('skill_category__top_category').all()
    max_scores_by_top_cat = defaultdict(int)
    for item in all_items:
        max_scores_by_top_cat[item.skill_category.top_category.name] += item.max_score

    user_scores_by_top_cat = defaultdict(int)
    for score in score_history:
        user_scores_by_top_cat[score.item.skill_category.top_category.name] += score.score
    
    for top_cat_name, skills in structured_scores.items():
        user_score = user_scores_by_top_cat.get(top_cat_name, 0)
        max_score = max_scores_by_top_cat.get(top_cat_name, 0)
        percentage = (user_score / max_score) * 100 if max_score > 0 else 0
        
        # ★★★ ここからカテゴリ別バーの色分けロジック ★★★
        category_progress_color = "bg-success" # 80%以上 (緑)
        if percentage < 20:
            category_progress_color = "bg-danger"   # 20%未満 (赤)
        elif percentage < 50:
            category_progress_color = "bg-warning"  # 50%未満 (黄)
        elif percentage < 80:
            category_progress_color = "bg-primary"  # 80%未満 (青)
        # ★★★ ここまで ★★★

        dashboard_data.append({
            "top_category_name": top_cat_name,
            "skills": skills.items(),
            "progress": {
                "user_score": user_score, 
                "max_score": max_score, 
                "percentage": percentage,
                "color": category_progress_color # ★ 色情報を追加
            }
        })

    # --- (総合ランクと進捗の計算部分は変更なし) ---
    # ... (前回の正しいコードをそのままお使いください) ...
    next_rank = Rank.objects.filter(required_score__gt=editor.total_score).order_by('required_score').first()
    next_rank_display = next_rank
    is_fully_maxed = False
    if not next_rank:
        final_target_score = 100
        if editor.total_score >= final_target_score:
            is_fully_maxed = True
        else:
            next_rank_display = {'name': '完全制覇', 'required_score': final_target_score}
    progress_percentage = 0
    points_to_next_rank = 0
    if not is_fully_maxed and next_rank_display:
        current_rank_score = editor.rank.required_score if editor.rank else 0
        required_score = next_rank_display.required_score if isinstance(next_rank_display, Rank) else next_rank_display['required_score']
        score_in_current_rank = editor.total_score - current_rank_score
        next_rank_score_gap = required_score - current_rank_score
        points_to_next_rank = required_score - editor.total_score
        if next_rank_score_gap > 0:
            progress_percentage = (score_in_current_rank / next_rank_score_gap) * 100
    elif is_fully_maxed:
        progress_percentage = 100
    progress_bar_color = "bg-secondary"
    if editor.rank:
        if editor.rank.name == "アソシエイトエディター": progress_bar_color = "bg-primary"
        elif editor.rank.name == "プロエディター": progress_bar_color = "bg-success"
        elif editor.rank.name == "リードエディター": progress_bar_color = "bg-warning"

    context = {
        'editor': editor,
        'dashboard_data': dashboard_data,
        'next_rank_display': next_rank_display,
        'is_fully_maxed': is_fully_maxed,
        'progress_percentage': progress_percentage,
        'points_to_next_rank': points_to_next_rank,
        'progress_bar_color': progress_bar_color,
    }
    
    return render(request, 'ranking/dashboard.html', context)