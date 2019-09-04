# Generated by Django 2.2.3 on 2019-07-15 09:36

import apps.db_data.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
        ("db_data", "0013_officer_officer_since"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventCategory",
            fields=[
                (
                    "id",
                    models.CharField(max_length=16, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name="Officership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("blurb", models.CharField(max_length=255)),
                ("office_hours", models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                        to_field="username",
                    ),
                ),
                (
                    "photo1",
                    models.ImageField(
                        default="images/officers/cardigan.jpg",
                        max_length=255,
                        upload_to=apps.db_data.models.person_photo_path,
                    ),
                ),
                (
                    "photo2",
                    models.ImageField(
                        blank=True,
                        max_length=255,
                        upload_to=apps.db_data.models.person_photo_path_alt,
                    ),
                ),
                (
                    "video2",
                    models.FileField(
                        blank=True,
                        max_length=255,
                        upload_to=apps.db_data.models.person_photo_path_alt,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PolitburoMembership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="db_data.Person"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Semester",
            fields=[
                (
                    "id",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("current", models.BooleanField()),
                ("name", models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name="UcbClass",
            fields=[
                (
                    "id",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                )
            ],
        ),
        migrations.RemoveField(model_name="event", name="enabled"),
        migrations.RemoveField(model_name="officer", name="blurb"),
        migrations.RemoveField(model_name="officer", name="enabled"),
        migrations.RemoveField(model_name="officer", name="first_name"),
        migrations.RemoveField(model_name="officer", name="last_name"),
        migrations.RemoveField(model_name="officer", name="office_hours"),
        migrations.RemoveField(model_name="officer", name="photo1"),
        migrations.RemoveField(model_name="officer", name="photo2"),
        migrations.RemoveField(model_name="officer", name="tutor_subjects"),
        migrations.RemoveField(model_name="politburo", name="officer"),
        migrations.RemoveField(model_name="sponsor", name="current"),
        migrations.RemoveField(model_name="sponsor", name="description"),
        migrations.AlterField(
            model_name="event", name="link", field=models.URLField(blank=True)
        ),
        migrations.CreateModel(
            name="Sponsorship",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.CharField(max_length=255)),
                (
                    "semester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="db_data.Semester",
                    ),
                ),
                (
                    "sponsor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="db_data.Sponsor",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="semester",
            name="events",
            field=models.ManyToManyField(blank=True, to="db_data.Event"),
        ),
        migrations.AddField(
            model_name="semester",
            name="officers",
            field=models.ManyToManyField(
                blank=True, through="db_data.Officership", to="db_data.Officer"
            ),
        ),
        migrations.AddField(
            model_name="semester",
            name="politburo",
            field=models.ManyToManyField(
                through="db_data.PolitburoMembership", to="db_data.Politburo"
            ),
        ),
        migrations.AddField(
            model_name="semester",
            name="sponsors",
            field=models.ManyToManyField(
                through="db_data.Sponsorship", to="db_data.Sponsor"
            ),
        ),
        migrations.AddField(
            model_name="politburomembership",
            name="politburo",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="db_data.Politburo"
            ),
        ),
        migrations.AddField(
            model_name="politburomembership",
            name="semester",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="db_data.Semester"
            ),
        ),
        migrations.AddField(
            model_name="officership",
            name="officer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="db_data.Officer"
            ),
        ),
        migrations.AddField(
            model_name="officership",
            name="semester",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="db_data.Semester"
            ),
        ),
        migrations.AddField(
            model_name="officership",
            name="tutor_subjects",
            field=models.ManyToManyField(blank=True, to="db_data.UcbClass"),
        ),
        migrations.AddField(
            model_name="event",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="db_data.EventCategory",
            ),
        ),
        migrations.AddField(
            model_name="officer",
            name="person",
            field=models.OneToOneField(
                default="pnunez",
                on_delete=django.db.models.deletion.PROTECT,
                to="db_data.Person",
            ),
            preserve_default=False,
        ),
    ]
