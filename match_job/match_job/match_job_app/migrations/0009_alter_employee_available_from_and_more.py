# Generated by Django 4.2.1 on 2023-05-18 18:01

from django.db import migrations, models
import django.db.models.deletion
import match_job_app.models


class Migration(migrations.Migration):
    dependencies = [
        ("match_job_app", "0008_employee_profile_pic_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="available_from",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="employee",
            name="available_to",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="employee",
            name="name",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="employee",
            name="profile_pic",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=match_job_app.models.employee_directory_path,
            ),
        ),
        migrations.AlterField(
            model_name="employeejob",
            name="job_name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="employeejob",
            name="work_from",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="employeejob",
            name="work_to",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="employeelanguage",
            name="language_name",
            field=models.CharField(
                choices=[
                    ("Polski", "Polski"),
                    ("Angielski", "Angielski"),
                    ("Hiszpański", "Hiszpański"),
                    ("Niemiecki", "Niemiecki"),
                    ("Francuski", "Francuski"),
                    ("Włoski", "Włoski"),
                    ("Portugalski", "Portugalski"),
                    ("Holenderski", "Holenderski"),
                    ("Rosyjski", "Rosyjski"),
                    ("Chiński", "Chiński"),
                    ("Japoński", "Japoński"),
                    ("Koreański", "Koreański"),
                    ("Arabski", "Arabski"),
                    ("Turecki", "Turecki"),
                    ("Grecki", "Grecki"),
                    ("Szwedzki", "Szwedzki"),
                    ("Norweski", "Norweski"),
                    ("Duński", "Duński"),
                    ("Finski", "Finski"),
                    ("Islandzki", "Islandzki"),
                    ("Słowacki", "Słowacki"),
                    ("Czeski", "Czeski"),
                    ("Słoweński", "Słoweński"),
                    ("Węgierski", "Węgierski"),
                    ("Rumuński", "Rumuński"),
                    ("Bułgarski", "Bułgarski"),
                    ("Ukraiński", "Ukraiński"),
                    ("Litewski", "Litewski"),
                    ("Łotewski", "Łotewski"),
                    ("Estoński", "Estoński"),
                    ("Białoruski", "Białoruski"),
                    ("Chorwacki", "Chorwacki"),
                    ("Serbski", "Serbski"),
                    ("Macedoński", "Macedoński"),
                    ("Albański", "Albański"),
                    ("Szwajcarski", "Szwajcarski"),
                    ("Irlandzki", "Irlandzki"),
                    ("Szkocki", "Szkocki"),
                    ("Walijski", "Walijski"),
                    ("Angielski amerykański", "Angielski amerykański"),
                    ("Kanadyjski", "Kanadyjski"),
                    ("Meksykański", "Meksykański"),
                    ("Brazylijski", "Brazylijski"),
                    ("Argentyński", "Argentyński"),
                    ("Chiński tradycyjny", "Chiński tradycyjny"),
                    ("Chiński uproszczony", "Chiński uproszczony"),
                    ("Japoński tradycyjny", "Japoński tradycyjny"),
                    ("Japoński uproszczony", "Japoński uproszczony"),
                ],
                default="pl",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="employeelanguage",
            name="level",
            field=models.CharField(
                choices=[
                    ("Master", "Master"),
                    ("Fluent", "Fluent"),
                    ("Advanced", "Advanced"),
                    ("Intermediate", "Intermediate"),
                    ("Beginner", "Beginner"),
                ],
                default="MASTER",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="employer",
            name="name",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.CreateModel(
            name="EmployeeJobTarget",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "target_name",
                    models.CharField(
                        choices=[
                            ("Nauczyciel", "Nauczyciel"),
                            ("Lekarz", "Lekarz"),
                            ("Inżynier", "Inzynier"),
                            ("Prawnik", "Prawnik"),
                            ("Sprzedawca", "Sprzedawca"),
                            ("Programista", "Programista"),
                            ("Księgowy", "Ksiegowy"),
                            ("Projektant graficzny", "Projektant graficzny"),
                            ("Pilot", "Pilot"),
                            ("Architekt", "Architekt"),
                            ("Polityk", "Polityk"),
                            ("Dziennikarz", "Dziennikarz"),
                            ("Psycholog", "Psycholog"),
                            ("Chemik", "Chemik"),
                            ("Fizjoterapeuta", "Fizjoterapeuta"),
                            ("Fotograf", "Fotograf"),
                            ("Instruktor fitness", "Instruktor fitness"),
                            ("Mechanik samochodowy", "Mechanik samochodowy"),
                            ("Projektant mody", "Projektant mody"),
                            ("Kucharz", "Kucharz"),
                            ("Ogrodnik", "Ogrodnik"),
                            ("Elektryk", "Elektryk"),
                            ("Muzyk", "Muzyk"),
                            ("Tłumacz", "Tlumacz"),
                            ("Hydraulik", "Hydraulik"),
                            ("Kierowca ciężarówki", "Kierowca ciezarowki"),
                            ("Geolog", "Geolog"),
                            ("Projektant wnętrz", "Projektant wnetrz"),
                            ("Strażak", "Strazak"),
                            ("Bibliotekarz", "Bibliotekarz"),
                            ("Weterynarz", "Weterynarz"),
                            ("Trener personalny", "Trener personalny"),
                            ("Aktor", "Aktor"),
                            (
                                "Projektant gier komputerowych",
                                "Projektant gier komputerowych",
                            ),
                            ("Farmaceuta", "Farmaceuta"),
                            ("Projektant dźwięku", "Projektant dzwieku"),
                            ("Doradca finansowy", "Doradca finansowy"),
                            ("Barista", "Barista"),
                            ("Właściciel restauracji", "Wlasciciel restauracji"),
                            ("Lotnik", "Lotnik"),
                            ("Projektant produktu", "Projektant produktu"),
                            ("Copywriter", "Copywriter"),
                            ("Tancerz", "Tancerz"),
                            ("Doradca zawodowy", "Doradca zawodowy"),
                            ("Grafik komputerowy", "Grafik komputerowy"),
                            ("Analityk danych", "Analityk danych"),
                            ("Stewardessa", "Stewardessa"),
                            ("Animator", "Animator"),
                            ("Fotoreporter", "Fotoreporter"),
                            ("Pracownik socjalny", "Pracownik socjalny"),
                            ("Geodeta", "Geodeta"),
                            ("Notariusz", "Notariusz"),
                            ("Filmowiec", "Filmowiec"),
                            ("Mechanik lotniczy", "Mechanik lotniczy"),
                        ],
                        default="Nauczyciel",
                        max_length=50,
                    ),
                ),
                (
                    "target_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="target",
                        to="match_job_app.employee",
                    ),
                ),
            ],
        ),
    ]
