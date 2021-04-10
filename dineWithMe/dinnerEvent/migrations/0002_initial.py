# Generated by Django 3.2 on 2021-04-10 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dinnerEvent', '0001_initial'),
        ('userProfile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dinnerevent',
            name='guests',
            field=models.ManyToManyField(related_name='attending', to='userProfile.UserProfile'),
        ),
        migrations.AddField(
            model_name='dinnerevent',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dinnerEvent', to='userProfile.userprofile'),
        ),
        migrations.AddField(
            model_name='dinnercomment',
            name='dinner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='dinnerEvent.dinnerevent'),
        ),
        migrations.AddField(
            model_name='dinnercomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='userProfile.userprofile'),
        ),
        migrations.AlterUniqueTogether(
            name='dinnerpreferences',
            unique_together={('dinner_id', 'preference')},
        ),
    ]
