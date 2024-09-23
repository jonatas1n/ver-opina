# Generated by Django 4.2 on 2024-09-15 18:53

from django.db import migrations
from home.models import LandingPage
from wagtail.models import Page, Site


def create_homepage(apps, schema_editor):
    site = Site.objects.all().first()

    actual_home = Page.objects.filter(slug="home").first()
    if actual_home:
        actual_home.slug = "old-home"
        actual_home.path = "00010012"
        actual_home.save()

    home = LandingPage(
        title="Landing Page", slug="home", depth=2, path="00010001", numchild=0
    )
    home.save()

    home_page = Page.objects.filter(slug="home").first()

    site.root_page_id = home_page.id
    site.is_default_site = True
    site.save()


def remove_homepage(apps, schema_editor):
    LandingPage = apps.get_model("home", "LandingPage")
    landing_page = LandingPage.objects.filter(slug="home").first()

    if landing_page:
        landing_page.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_homepage, remove_homepage),
    ]
