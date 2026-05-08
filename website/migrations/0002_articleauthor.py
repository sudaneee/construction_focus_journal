from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        # Drop the old implicit M2M table first
        migrations.RunSQL(
            sql='DROP TABLE IF EXISTS website_article_authors;',
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Create the through model table
        migrations.CreateModel(
            name='ArticleAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.author')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('article', 'author')},
            },
        ),
        # Point the M2M field at the new through model (state only — table already exists)
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='article',
                    name='authors',
                    field=models.ManyToManyField(
                        related_name='articles',
                        through='website.ArticleAuthor',
                        to='website.author',
                    ),
                ),
            ],
            database_operations=[],
        ),
    ]
