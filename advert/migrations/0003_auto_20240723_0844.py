# Generated by Django 5.0.7 on 2024-07-23 08:44

from django.db import migrations, connection


def create_increment_views_function(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute("""
        CREATE OR REPLACE FUNCTION increment_advert_views(advert_uuid UUID) RETURNS void AS $$
        BEGIN
            UPDATE advert_advert SET views = views + 1 WHERE uuid = advert_uuid;
        END;
        $$ LANGUAGE plpgsql;
        """)


def drop_increment_views_function(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute("DROP FUNCTION IF EXISTS increment_advert_views(UUID);")


class Migration(migrations.Migration):

    dependencies = [
        ('advert', '0002_auto_20240721_1124'),
    ]

    operations = [
        migrations.RunPython(create_increment_views_function, reverse_code=drop_increment_views_function),
    ]
