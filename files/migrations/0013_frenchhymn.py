# Generated by Django 4.2.20 on 2025-04-13 21:31

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0012_hymn_hymn_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrenchHymn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='french_hymns/images/')),
                ('lyrics', ckeditor.fields.RichTextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('hymn_type', models.CharField(choices=[('morning', 'Matin'), ('evening', 'Soir'), ('the_lords_day', 'Le Jour du Seigneur'), ('praises', 'Louanges'), ('advent', 'Avent'), ('christmas', 'Noël'), ('closing_opening_year', 'Clôture et Ouverture de l’Année'), ('warning_petition_gospel_call', 'Avertissement, Prière et Appel de l’Évangile'), ('lent_repentance', 'Carême et Repentance'), ('palm_sunday', 'Dimanche des Rameaux'), ('suffering_death', 'Souffrance et Mort'), ('resurrection', 'Résurrection'), ('lords_day_after_resurrection', 'Jour du Seigneur après la Résurrection'), ('ascension', 'Ascension'), ('holy_ghost', 'Saint-Esprit'), ('pentecostal_revival', 'Réveil Pentecôtiste'), ('missionary', 'Missionnaire'), ('word_of_god', 'La Parole de Dieu'), ('baptism', 'Baptême'), ('holy_communion', 'Sainte Communion'), ('holy_matrimony', 'Saint Mariage'), ('children_youth', 'Enfants et Jeunesse'), ('prayer', 'Prière'), ('divine_healing', 'Guérison Divine'), ('faith', 'Foi'), ('unity_peace', 'Unité et Paix'), ('time_old_age', 'Temps de Vieillesse'), ('harvest_anniversaries', 'Récolte et Anniversaires'), ('love', 'Amour'), ('guidance_protection', 'Direction et Protection'), ('labour_service', 'Travail et Service'), ('trials_victories', 'Épreuves et Victoires'), ('encouragement', 'Encouragement'), ('building_dedication', 'Bâtiment et Dédicace'), ('servants_for_god', 'Serviteurs de Dieu'), ('farewell', 'Adieu'), ('church_heaven_earth', 'Église sur Terre et au Ciel'), ('various_hymns', 'Divers Cantiques')], default='morning', max_length=50)),
            ],
        ),
    ]
