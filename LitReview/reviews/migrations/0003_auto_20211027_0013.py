# Generated by Django 3.2.8 on 2021-10-26 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20211021_2144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userfollow',
            options={'verbose_name': 'Abonné à un utilisateur', 'verbose_name_plural': 'Abonnés aux utilisateurs'},
        ),
        migrations.AlterField(
            model_name='review',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='reviews.ticket'),
        ),
    ]