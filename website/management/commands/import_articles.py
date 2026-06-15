import json
import shutil
from datetime import date, timedelta
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from website.models import Article, ArticleAuthor, Author, Issue, Volume

SOURCE_DIR = Path(r"C:\Users\ismai\Downloads\cfjournal")
IMPORT_DIR = Path(settings.BASE_DIR) / "import_data"

YEARS = [2021, 2022, 2023, 2024]

FEATURED_2024_ORDERS = {1, 2, 3}


class Command(BaseCommand):
    help = "Delete dummy journal data and import real articles from import_data/*.json"

    def handle(self, *args, **options):
        self.clear_existing_data()

        for year in YEARS:
            volume_number = year - 2020
            volume = Volume.objects.create(volume_number=volume_number, year=year)
            issue = Issue.objects.create(
                volume=volume,
                issue_number=1,
                publication_date=date(year, 12, 31),
            )

            data = json.loads((IMPORT_DIR / f"{year}.json").read_text(encoding="utf-8"))

            for entry in data:
                self.import_article(volume, issue, year, entry)

        self.stdout.write(self.style.SUCCESS("Import complete."))

    def clear_existing_data(self):
        Article.objects.all().delete()
        Author.objects.all().delete()
        Issue.objects.all().delete()
        Volume.objects.all().delete()

        for subdir in ("pdfs", "covers"):
            folder = Path(settings.MEDIA_ROOT) / subdir
            if folder.exists():
                for f in folder.iterdir():
                    if f.is_file():
                        f.unlink()

        self.stdout.write("Cleared existing dummy data.")

    def import_article(self, volume, issue, year, entry):
        order = entry["order"]
        publication_date = date(year, 12, 31) - timedelta(days=order - 1)

        title_slug = slugify(entry["title"])[:60]
        dest_filename = f"v{volume.volume_number}-{order:02d}-{title_slug}.pdf"
        src_pdf = SOURCE_DIR / str(year) / entry["source_file"]
        dest_pdf = Path(settings.MEDIA_ROOT) / "pdfs" / dest_filename
        shutil.copy(src_pdf, dest_pdf)

        article = Article(
            title=entry["title"],
            abstract=entry["abstract"],
            keywords=entry["keywords"],
            volume=volume,
            issue=issue,
            pdf_file=f"pdfs/{dest_filename}",
            publication_date=publication_date,
            doi=entry["doi"],
            is_featured=(year == 2024 and order in FEATURED_2024_ORDERS),
        )
        article.save()

        for position, author_data in enumerate(entry["authors"], start=1):
            author, created = Author.objects.get_or_create(
                full_name=author_data["full_name"],
                defaults={
                    "affiliation": author_data["affiliation"],
                    "email": author_data["email"],
                },
            )
            ArticleAuthor.objects.create(article=article, author=author, order=position)

        self.stdout.write(f"  Imported: {article.title}")
