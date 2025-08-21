from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0001_initial'),
    ]

    operations = [
    ]
from django.db import migrations

INITIAL_DATA = {
    "編集スキル":{
        "カット編集スキル": [
        ("基本的な素材の選択と繋ぎができる。", 2),
        ("編集点が丁寧で、視聴者が見やすい自然な繋がりを意識できている。", 3),
        ("画の選び方、画の動きが効果的。", 3),
        ("カットのペースが動画の内容や目的に合致している。", 2),
    ],
    "テロップ・字幕作成スキル": [
        ("誤字脱字がなく、正確な情報が記載されている。", 3),
        ("フォント、サイズ、色、配置が適切で、動画の雰囲気に合っている。", 3),
        ("表示されるタイミングや長さが適切で、視聴者が読みやすい。", 2),
        ("テロップのデザインが動画全体のクオリティを高めている。", 2),
    ],
    "音響編集・MAスキル": [
        ("BGM・SEの適切な選定と音量調整ができる", 4),
        ("ノイズ除去、音質調整など、クリアな音声を維持できる", 3),
        ("視聴体験を高めるための音響演出を提案・実行できる", 3),
    ],
        "色調補正・グレーディングスキル": [
        ("適切なホワイトバランス、露出調整ができる", 4),
        ("動画の雰囲気に合わせた統一感のある色調補正ができる", 3),
        ("視聴者の感情に訴えかけるようなグレーディングができる", 3),
    ],
        "モーショングラフィック・VFXスキル": [
        ("基本的な図形やテキストアニメーションを作成できる", 4),
        ("After Effectsなどを使用し、複雑なアニメーションやエフェクトを作成できる", 3),
        ("動画の目的達成に寄与する、クリエイティブなモーショングラフィックを提案・実装できる", 3),
    ]},
    
    "制作進行・品質管理":{
        "納期厳守率": [
        ("常に納期を厳守している。やむを得ない遅延の場合も、事前に連絡・相談し、適切な対応をとっている。\
(補足: 納期厳守ができていない場合は減点方式、または基準点以下となる形で評価します。1回遅延で-3点)", 10),
    ],
        "クライアント/ディレクターとのコミュニケーション": [
        ("指示内容を正確に理解し、疑問点があれば速やかに確認できる", 4),
        ("進捗状況を定期的に報告し、円滑なコミュニケーションを心がけている", 3),
        ("修正指示に対して的確かつ迅速に対応できる", 3),
    ],
        "制作物の品質": [
        ("誤字脱字、音飛び、画質劣化などのミスがない", 3),
        ("チーム内で定めた品質基準（例: 画角、テロップのフォント・サイズ、BGMの音量など）を遵守している", 3),
        ("視聴者の視点に立ち、より良い動画にするための提案を積極的に行い、品質向上に貢献している", 4),
    ]},
    "貢献度・プロ意識":{
        "自主性・向上心": [
        ("常に自身のスキルアップに努め、新しい表現方法や技術を習得しようとしている", 10),
        ("与えられたタスクだけでなく、自ら課題を見つけて改善提案を行う",10)
    ]},
    
    # ... 他のスキルカテゴリも同様に追加 ...
}


def load_initial_data(apps, schema_editor):
    TopCategory = apps.get_model('ranking', 'TopCategory')
    SkillCategory = apps.get_model('ranking', 'SkillCategory')
    EvaluationItem = apps.get_model('ranking', 'EvaluationItem')

    for top_cat_name, skills in INITIAL_DATA.items():
        top_category, _ = TopCategory.objects.get_or_create(name=top_cat_name)
        for skill_cat_name, items in skills.items():
            skill_category, _ = SkillCategory.objects.get_or_create(
                top_category=top_category,
                name=skill_cat_name
            )
            for item_name, max_score in items:
                EvaluationItem.objects.get_or_create(
                    skill_category=skill_category,
                    name=item_name,
                    defaults={'max_score': max_score}
                )

class Migration(migrations.Migration):
    dependencies = [
        ('ranking', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(load_initial_data),
    ]