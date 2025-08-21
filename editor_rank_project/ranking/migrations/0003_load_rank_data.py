from django.db import migrations

# 登録したいランクの定義
RANKS = [
    {"name": "アソシエイトエディター", "score": 0},
    {"name": "プロエディター", "score": 60},
    {"name": "リードエディター", "score": 85},
]

def load_ranks(apps, schema_editor):
    Rank = apps.get_model('ranking', 'Rank')
    for rank_data in RANKS:
        Rank.objects.get_or_create(
            name=rank_data["name"],
            defaults={'required_score': rank_data["score"]}
        )

class Migration(migrations.Migration):
    dependencies = [
        ('ranking', '0002_load_initial_data'), # 直前のマイグレーションファイル名
    ]
    operations = [
        migrations.RunPython(load_ranks),
    ]