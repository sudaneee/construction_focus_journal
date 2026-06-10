import os
import shutil

from django.conf import settings
from django.db import migrations


def seed_logo(apps, schema_editor):
    SiteSettings = apps.get_model('website', 'SiteSettings')

    source = os.path.join(settings.BASE_DIR, 'cfj_logo.jpeg')
    if not os.path.exists(source):
        SiteSettings.objects.get_or_create(pk=1)
        return

    dest_dir = os.path.join(settings.MEDIA_ROOT, 'site')
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, 'cfj_logo.jpeg')
    if not os.path.exists(dest):
        shutil.copyfile(source, dest)

    obj, _ = SiteSettings.objects.get_or_create(pk=1)
    obj.logo.name = 'site/cfj_logo.jpeg'
    obj.save()


def unseed_logo(apps, schema_editor):
    SiteSettings = apps.get_model('website', 'SiteSettings')
    SiteSettings.objects.filter(pk=1).update(logo='')


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_sitesettings'),
    ]

    operations = [
        migrations.RunPython(seed_logo, unseed_logo),
    ]
