# Generated by Django 4.1.4 on 2022-12-20 18:07

from django.db import migrations
import shop.watch_shop.managers


class Migration(migrations.Migration):

    dependencies = [
        ('watch_shop', '0003_alter_watchshopuser_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='watchshopuser',
            managers=[
                ('objects', shop.watch_shop.managers.WatchShopUserManager()),
            ],
        ),
    ]
