from django.db import migrations

SCOPE_TOPICS = [
    # (name, short_name)
    ('Construction Management & Economics', 'Construction Management'),
    ('Structural Engineering & Analysis', 'Structural Engineering'),
    ('Sustainable Building & Green Construction', 'Sustainable Building'),
    ('Project Planning & Scheduling', 'Project Management'),
    ('Building Information Modelling (BIM)', 'BIM & Digital Construction'),
    ('Infrastructure Development & Transport', 'Infrastructure Development'),
    ('Construction Materials & Testing', 'Materials & Methods'),
    ('Health & Safety on Site', 'Health & Safety'),
    ('Smart Technologies in Construction', ''),
    ('Environmental Impact Assessment', ''),
]

REVIEW_STEPS = [
    'Submission Received',
    'Initial Editorial Screening',
    'Double-Blind Peer Review',
    'Author Revision',
    'Final Decision',
    'Publication',
]

GUIDELINE_ITEMS = [
    ('Manuscript Length', '5,000 – 12,000 words (excluding references)'),
    ('Abstract', '150 – 250 words, structured'),
    ('Keywords', '4 – 8 keywords'),
    ('File Format', 'PDF (final submission), Word/LaTeX (revision)'),
    ('Citation Style', 'APA 7th Edition'),
    ('Language', 'English (British or American, consistent)'),
    ('Review Time', 'Approximately 6–10 weeks'),
]


def seed_content(apps, schema_editor):
    ScopeTopic = apps.get_model('website', 'ScopeTopic')
    ReviewStep = apps.get_model('website', 'ReviewStep')
    GuidelineItem = apps.get_model('website', 'GuidelineItem')

    if not ScopeTopic.objects.exists():
        for order, (name, short_name) in enumerate(SCOPE_TOPICS):
            ScopeTopic.objects.create(name=name, short_name=short_name, order=order)

    if not ReviewStep.objects.exists():
        for order, name in enumerate(REVIEW_STEPS):
            ReviewStep.objects.create(name=name, order=order)

    if not GuidelineItem.objects.exists():
        for order, (label, value) in enumerate(GUIDELINE_ITEMS):
            GuidelineItem.objects.create(label=label, value=value, order=order)


def unseed_content(apps, schema_editor):
    apps.get_model('website', 'ScopeTopic').objects.all().delete()
    apps.get_model('website', 'ReviewStep').objects.all().delete()
    apps.get_model('website', 'GuidelineItem').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_guidelineitem_reviewstep_scopetopic_submission_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_content, unseed_content),
    ]
