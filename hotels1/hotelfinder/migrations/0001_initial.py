# Generated by Django 2.0.5 on 2018-09-05 19:43

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('hotel_id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular hotel', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.IntegerField()),
                ('star_class', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('price_approx', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('rating_id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this rating', primary_key=True, serialize=False)),
                ('stay_date', models.DateField(blank=True, null=True)),
                ('rating_CLEANLINESS', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('rating_SERVICE', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('rating_LOCATION', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('rating_VALUE', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('rating_OVERALL', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotelfinder.Hotel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]