
import os
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, datetime
from ckeditor.fields import RichTextField




class FileUpload(models.Model):
    file_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    company_location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.company_location} - {self.date} {self.time}"

    def file_extension(self):
        """Returns the file extension from file_url even with query params"""
        if self.file_url:
            path = self.file_url.split('?')[0]
            _, ext = os.path.splitext(path)
            return ext.lower().strip()
        return ''




        







class PDFUpload(models.Model):
    company_location = models.CharField(max_length=255)
    info_id = models.CharField(max_length=255, blank=True, null=True)
    
    # This holds the public URL from Supabase
    pdf_url = models.URLField(null=True)
    
    # Optional cover image
    image_url = models.URLField(
        blank=True,
        null=True,
        default='https://cdn-icons-png.flaticon.com/512/337/337946.png'
    )

    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    def __str__(self):
        return f"{self.company_location} - {self.info_id} - {self.pdf_url}"

    def file_extension(self):
        if self.pdf_url:
            return os.path.splitext(self.pdf_url.split('?')[0])[1].lower()
        return ''


# ✅ Validator if ever needed in a FileField or custom form field
def validate_pdf(value):
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")









class Gallery(models.Model):
    image_url = models.URLField(null=True)  # Supabase image URL
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title






class Hymn(models.Model):
    HYMN_TYPE_CHOICES = [
        ('morning', 'Morning'),
        ('evening', 'Evening'),
        ("the_lords_day", "The Lord's Day"),
        ('praises', 'Praises'),
        ('advent', 'Advent'),
        ('christmas', 'Christmas'),
        ('closing_opening_year', 'Closing and Opening of the Year'),
        ('warning_petition_gospel_call', 'Warning, Petition and Gospel Call'),
        ('lent_repentance', 'Lent and Repentance'),
        ('palm_sunday', 'Palm Sunday'),
        ('suffering_death', 'Suffering and Death'),
        ('resurrection', 'Resurrection'),
        ('lords_day_after_resurrection', "Lord's Day after Resurrection"),
        ('ascension', 'Ascension'),
        ('holy_ghost', 'Holy Ghost'),
        ('pentecostal_revival', 'Pentecostal Revival'),
        ('missionary', 'Missionary'),
        ('word_of_god', 'The Word of God'),
        ('baptism', 'Baptism'),
        ('holy_communion', 'Holy Communion'),
        ('holy_matrimony', 'Holy Matrimony'),
        ('children_youth', 'Children and Youth'),
        ('prayer', 'Prayer'),
        ('divine_healing', 'Divine Healing'),
        ('faith', 'Faith'),
        ('unity_peace', 'Unity and Peace'),
        ('time_old_age', 'Time of Old Age'),
        ('harvest_anniversaries', 'Harvest and Anniversaries'),
        ('love', 'Love'),
        ('guidance_protection', 'Guidance and Protection'),
        ('labour_service', 'Labour and Service'),
        ('trials_victories', 'Trials and Victories'),
        ('encouragement', 'Encouragement'),
        ('building_dedication', 'Building and Dedication'),
        ('servants_for_god', 'Servants for God'),
        ('farewell', 'Farewell'),
        ('church_heaven_earth', 'The Church in Heaven and Earth'),
        ('various_hymns', 'Various Hymns'),
    ]

    title = models.CharField(max_length=255)
    hymn_type = models.CharField(max_length=50, choices=HYMN_TYPE_CHOICES, default='morning')
    description = models.TextField(blank=True, null=True)
    lyrics = RichTextField()

    def __str__(self):
        return self.title




class FrenchHymn(models.Model):
    HYMN_TYPE_CHOICES = [
        ('morning', 'Matin'),
        ('evening', 'Soir'),
        ("the_lords_day", "Le Jour du Seigneur"),
        ('praises', 'Louanges'),
        ('advent', 'Avent'),
        ('christmas', 'Noël'),
        ('closing_opening_year', 'Clôture et Ouverture de l’Année'),
        ('warning_petition_gospel_call', 'Avertissement, Prière et Appel de l’Évangile'),
        ('lent_repentance', 'Carême et Repentance'),
        ('palm_sunday', 'Dimanche des Rameaux'),
        ('suffering_death', 'Souffrance et Mort'),
        ('resurrection', 'Résurrection'),
        ('lords_day_after_resurrection', "Jour du Seigneur après la Résurrection"),
        ('ascension', 'Ascension'),
        ('holy_ghost', 'Saint-Esprit'),
        ('pentecostal_revival', 'Réveil Pentecôtiste'),
        ('missionary', 'Missionnaire'),
        ('word_of_god', 'La Parole de Dieu'),
        ('baptism', 'Baptême'),
        ('holy_communion', 'Sainte Communion'),
        ('holy_matrimony', 'Saint Mariage'),
        ('children_youth', 'Enfants et Jeunesse'),
        ('prayer', 'Prière'),
        ('divine_healing', 'Guérison Divine'),
        ('faith', 'Foi'),
        ('unity_peace', 'Unité et Paix'),
        ('time_old_age', 'Temps de Vieillesse'),
        ('harvest_anniversaries', 'Récolte et Anniversaires'),
        ('love', 'Amour'),
        ('guidance_protection', 'Direction et Protection'),
        ('labour_service', 'Travail et Service'),
        ('trials_victories', 'Épreuves et Victoires'),
        ('encouragement', 'Encouragement'),
        ('building_dedication', 'Bâtiment et Dédicace'),
        ('servants_for_god', 'Serviteurs de Dieu'),
        ('farewell', 'Adieu'),
        ('church_heaven_earth', 'Église sur Terre et au Ciel'),
        ('various_hymns', 'Divers Cantiques'),
    ]

    title = models.CharField(max_length=255)
    hymn_type = models.CharField(max_length=50, choices=HYMN_TYPE_CHOICES, default='morning')
    description = models.TextField(blank=True, null=True)
    lyrics = RichTextField( null=True)

    def __str__(self):
        return self.title



class YorubaHymn(models.Model):
    HYMN_TYPE_CHOICES = [
        ('morning', 'Owuro'),
        ('evening', 'Irole'),
        ('the_lords_day', "Ojo Oluwa"),
        ('praises', 'Orin Iyin'),
        ('advent', 'Adifenti'),
        ('christmas', 'Keresimesi'),
        ('closing_opening_year', 'Ipade Odun Tuntun'),
        ('warning_petition_gospel_call', 'Ikilọ, Ibere ati Ipe Ihinrere'),
        ('lent_repentance', 'Akoko Iwẹ̀wẹ̀ ati Ironupiwada'),
        ('palm_sunday', 'Ojobo Ọpẹ'),
        ('suffering_death', 'Irora ati Iku'),
        ('resurrection', 'Ajinde'),
        ('lords_day_after_resurrection', 'Ọjọ Oluwa lẹ́yìn Ajinde'),
        ('ascension', 'Gíga sọdọ Ọlọrun'),
        ('holy_ghost', 'Ẹmí Mímọ́'),
        ('pentecostal_revival', 'Ìsọdọtun Pentikọsti'),
        ('missionary', 'Ìrànṣẹ́ Ọlọ́run'),
        ('word_of_god', 'Ọ̀rọ̀ Ọlọ́run'),
        ('baptism', 'Ìbaptisi'),
        ('holy_communion', 'Ajọpọ Mímọ́'),
        ('holy_matrimony', 'Ìgbéyàwó Mímọ́'),
        ('children_youth', 'Ọmọde ati Ọdọ́'),
        ('prayer', 'Àdúrà'),
        ('divine_healing', 'Ìwòsàn Ọlọ́run'),
        ('faith', 'Ìgbàgbọ́'),
        ('unity_peace', 'Ìṣọ̀kan àti Aláàfíà'),
        ('time_old_age', 'Àkókò Arugbo'),
        ('harvest_anniversaries', 'Ikore àti Ayẹyẹ ọdún'),
        ('love', 'Ìfẹ́'),
        ('guidance_protection', 'Ìtọ́sọ́nà àti Àbò'),
        ('labour_service', 'Iṣẹ́ àti Ìránṣẹ́'),
        ('trials_victories', 'Ìdánwò àti Ìṣegun'),
        ('encouragement', 'Ìtìlẹ́yìn'),
        ('building_dedication', 'Ìtajà ati Ìyàsímímọ́'),
        ('servants_for_god', 'Ìrànṣẹ́ fún Ọlọ́run'),
        ('farewell', 'Ìkíni Ọ̀fẹ́'),
        ('church_heaven_earth', 'Ìjọ lórí Ilẹ̀ àti lórí Ọ̀run'),
        ('various_hymns', 'Orin orisirisi'),
    ]

    title = models.CharField(max_length=255)
    hymn_type = models.CharField(max_length=100, choices=HYMN_TYPE_CHOICES)
    description = models.TextField(blank=True)
    lyrics = RichTextField( null=True)


    def __str__(self):
        return self.title



class IgboHymn(models.Model):
    HYMN_TYPE_CHOICES = [
        ('morning', 'Ụtụtụ'),
        ('evening', 'Mgbede'),
        ('the_lords_day', "Ụbọchị nke Onyenwe anyị"),
        ('praises', 'Abụ Otuto'),
        ('advent', 'Mbata Kraịst'),
        ('christmas', 'Krismas'),
        ('closing_opening_year', 'Mmechi na Mmeghe Afọ Ọhụrụ'),
        ('warning_petition_gospel_call', 'Ịdọ Aka ná Ntị, Arịrịọ na Oku Nke Oziọma'),
        ('lent_repentance', 'Ubochi ịlụnụ Mmehie (Lent) na Nloghachi'),
        ('palm_sunday', 'Ụka Ụkwụ Ọma (Palm Sunday)'),
        ('suffering_death', 'Ịrụ Uju na Onwu'),
        ('resurrection', 'Nbilite n’Ọnwụ'),
        ('lords_day_after_resurrection', 'Ụbọchị Onyenwe anyị Mgbe Nbilite n’Ọnwụ'),
        ('ascension', 'Ịrị Eluigwe'),
        ('holy_ghost', 'Mmụọ Nsọ'),
        ('pentecostal_revival', 'Mmemme Pentecost'),
        ('missionary', 'Ozi Kraịst'),
        ('word_of_god', 'Okwu Chineke'),
        ('baptism', 'Baptizim'),
        ('holy_communion', 'Nri Nsọ'),
        ('holy_matrimony', 'Alụmdi na Nwunye Nsọ'),
        ('children_youth', 'Ụmụaka na Ụmụaka Ntorobịa'),
        ('prayer', 'Ekpere'),
        ('divine_healing', 'Ngọzi Ọgwụsite N’aka Chineke'),
        ('faith', 'Ok believe (Nkwenye/Okwe Nke Kraịst)'),
        ('unity_peace', 'Udo na Nzukọ'),
        ('time_old_age', 'Oge Ọgụgụ Ndụ'),
        ('harvest_anniversaries', 'Mmepụta na Emume'),
        ('love', 'Ihụnanya'),
        ('guidance_protection', 'Ntuziaka na Nchedo'),
        ('labour_service', 'Ọrụ aka na Ọrụ Nsọ'),
        ('trials_victories', 'Nnwale na Mmeri'),
        ('encouragement', 'Nkwalite Obi'),
        ('building_dedication', 'Inye Ụlọ Nsọ Ọma'),
        ('servants_for_god', 'Oru Ndị Kraịst'),
        ('farewell', 'Ịkpọpụ Ọfọ'),
        ('church_heaven_earth', 'Ụka N’eluigwe na Ụwa'),
        ('various_hymns', 'Abụ Dị iche iche'),
    ]

    title = models.CharField(max_length=255)
    hymn_type = models.CharField(max_length=100, choices=HYMN_TYPE_CHOICES)
    description = models.TextField(blank=True)
    lyrics = RichTextField( null=True)

    def __str__(self):
        return self.title




class HausaHymn(models.Model):
    HYMN_TYPES = [
        ('morning', 'Safe'),
        ('evening', 'Yamma'),
        ('the_lords_day', 'Ranar Ubangiji'),
        ('praises', 'Yabo'),
        ('advent', 'Zuƙowa'),
        ('christmas', 'Kirsimeti'),
        ('closing_opening_year', 'Rufe da Buɗe Sabuwar Shekara'),
        ('warning_petition_gospel_call', 'Gargaɗi, Roƙo da Kiran Bishara'),
        ('lent_repentance', 'Azumi da Tuba'),
        ('palm_sunday', 'Lahadin Ganye'),
        ('suffering_death', 'Wahala da Mutuwa'),
        ('resurrection', 'Tashi daga Matattu'),
        ('lords_day_after_resurrection', 'Ranar Ubangiji bayan Tashi'),
        ('ascension', 'Haɗuwa Sama'),
        ('holy_ghost', 'Ruhu Mai Tsarki'),
        ('pentecostal_revival', 'Sabuntawa Pentikosti'),
        ('missionary', 'Ayyukan Mishan'),
        ('word_of_god', 'Kalmar Allah'),
        ('baptism', 'Baftisma'),
        ('holy_communion', 'Tarayyar Mai Tsarki'),
        ('holy_matrimony', 'Aure Mai Tsarki'),
        ('children_youth', 'Yara da Matasa'),
        ('prayer', 'Addu’a'),
        ('divine_healing', 'Warkarwa daga Allah'),
        ('faith', 'Bangaskiya'),
        ('unity_peace', 'Haɗin kai da Salama'),
        ('time_old_age', 'Lokacin Tsofanci'),
        ('harvest_anniversaries', 'Girbi da Tunawa'),
        ('love', 'Soyayya'),
        ('guidance_protection', 'Jagora da Kariya'),
        ('labour_service', 'Aiki da Hidima'),
        ('trials_victories', 'Jarabawa da Nasara'),
        ('encouragement', 'Karfi da Gwiwa'),
        ('building_dedication', 'Gina da Kaddamarwa'),
        ('servants_for_god', 'Bayin Allah'),
        ('farewell', 'Ban Kwana'),
        ('church_heaven_earth', 'Ikilisiya a Sama da Duniya'),
        ('various_hymns', 'Waƙoƙin Daban-daban'),
    ]

    title = models.CharField(max_length=255)
    hymn_type = models.CharField(max_length=50, choices=HYMN_TYPES)
    description = models.TextField(blank=True)
    lyrics = RichTextField( null=True)

    def __str__(self):
        return self.title



class ChineseHymn(models.Model):
    HYMN_TYPE_CHOICES = [
        ('morning', '清晨'),
        ('evening', '傍晚'),
        ('the_lords_day', '主日'),
        ('praises', '赞美诗'),
        ('advent', '降临节'),
        ('christmas', '圣诞节'),
        ('closing_opening_year', '年终与年初'),
        ('warning_petition_gospel_call', '警告、祈求与福音呼召'),
        ('lent_repentance', '四旬期与悔改'),
        ('palm_sunday', '棕枝主日'),
        ('suffering_death', '受难与死亡'),
        ('resurrection', '复活'),
        ('lords_day_after_resurrection', '复活后的主日'),
        ('ascension', '升天'),
        ('holy_ghost', '圣灵'),
        ('pentecostal_revival', '五旬节复兴'),
        ('missionary', '宣教'),
        ('word_of_god', '神的话语'),
        ('baptism', '洗礼'),
        ('holy_communion', '圣餐'),
        ('holy_matrimony', '圣婚'),
        ('children_youth', '儿童与青年'),
        ('prayer', '祷告'),
        ('divine_healing', '神圣医治'),
        ('faith', '信心'),
        ('unity_peace', '合一与和平'),
        ('time_old_age', '晚年'),
        ('harvest_anniversaries', '收获与周年庆'),
        ('love', '爱'),
        ('guidance_protection', '引导与保护'),
        ('labour_service', '劳作与事奉'),
        ('trials_victories', '试炼与得胜'),
        ('encouragement', '鼓励'),
        ('building_dedication', '建筑奉献'),
        ('servants_for_god', '神的仆人'),
        ('farewell', '告别'),
        ('church_heaven_earth', '地上与天上的教会'),
        ('various_hymns', '各类赞美诗'),
    ]

    title = models.CharField(max_length=255)
    hymn_type = models.CharField(max_length=100, choices=HYMN_TYPE_CHOICES)
    description = models.TextField(blank=True)
    lyrics = RichTextField(null=True)

    def __str__(self):
        return self.title




class GermanHymn(models.Model):
    HYMN_TYPE_CHOICES = [
        ('morning', 'Morgen'),
        ('evening', 'Abend'),
        ('the_lords_day', 'Tag des Herrn'),
        ('praises', 'Loblieder'),
        ('advent', 'Advent'),
        ('christmas', 'Weihnachten'),
        ('closing_opening_year', 'Jahresabschluss und -beginn'),
        ('warning_petition_gospel_call', 'Warnung, Bitte und Evangelium'),
        ('lent_repentance', 'Fastenzeit und Buße'),
        ('palm_sunday', 'Palmsonntag'),
        ('suffering_death', 'Leiden und Tod'),
        ('resurrection', 'Auferstehung'),
        ('lords_day_after_resurrection', 'Sonntag nach der Auferstehung'),
        ('ascension', 'Himmelfahrt'),
        ('holy_ghost', 'Heiliger Geist'),
        ('pentecostal_revival', 'Pfingstliche Erweckung'),
        ('missionary', 'Mission'),
        ('word_of_god', 'Gottes Wort'),
        ('baptism', 'Taufe'),
        ('holy_communion', 'Heiliges Abendmahl'),
        ('holy_matrimony', 'Heilige Ehe'),
        ('children_youth', 'Kinder und Jugendliche'),
        ('prayer', 'Gebet'),
        ('divine_healing', 'Göttliche Heilung'),
        ('faith', 'Glaube'),
        ('unity_peace', 'Einheit und Frieden'),
        ('time_old_age', 'Alter'),
        ('harvest_anniversaries', 'Ernte und Jubiläen'),
        ('love', 'Liebe'),
        ('guidance_protection', 'Führung und Schutz'),
        ('labour_service', 'Arbeit und Dienst'),
        ('trials_victories', 'Prüfungen und Siege'),
        ('encouragement', 'Ermutigung'),
        ('building_dedication', 'Einweihung von Gebäuden'),
        ('servants_for_god', 'Diener Gottes'),
        ('farewell', 'Abschied'),
        ('church_heaven_earth', 'Kirche im Himmel und auf Erden'),
        ('various_hymns', 'Verschiedene Lieder'),
    ]

    title = models.CharField(max_length=255)
    hymn_type = models.CharField(max_length=100, choices=HYMN_TYPE_CHOICES)
    description = models.TextField(blank=True)
    lyrics = RichTextField(null=True)

    def __str__(self):
        return self.title




class Hymn_Content(models.Model):
    lyrics = RichTextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the hymn is created
    
    def __str__(self):
        return f"Hymn created on {self.created_at}"
    





# models.py
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    image = models.ImageField(upload_to='contact_images/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"





class AutoReplyMessage(models.Model):
    subject = models.CharField(max_length=255, default="We received your message")
    message = models.TextField(default="Hi {name},\n\nThanks for contacting us. We'll get back to you shortly.\n\n- Admin")
    
    def __str__(self):
        return f"Auto-reply for contact form"





class AboutPage(models.Model):
    title = models.CharField(max_length=255, default="About Us")

    history = models.TextField(blank=True)
    more_history = RichTextField(blank=True)
    the_man = RichTextField(blank=True)
    mission_statement = RichTextField(blank=True)
    vision = RichTextField(blank=True)
    value = RichTextField(blank=True)
    mandate = RichTextField(blank=True)

    contact_address = RichTextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    image1_url = models.URLField(blank=True, null=True)  # ✅ only one image now

    def clean(self):
        if self.history:
            word_count = len(self.history.strip().split())
            if word_count > 50:
                raise ValidationError({'history': f'History can only contain up to 50 words. Currently: {word_count} words.'})

    def __str__(self):
        return self.title








# models.py
from django.db import models

class ComingSoonPage(models.Model):
    background_image_url = models.URLField(blank=True, null=True)  # changed to URLField
    note = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.note










from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255,  null=True)
    dob = models.DateField( null=True)
    profile_image = models.ImageField(upload_to='profile_images/')
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    phone = models.CharField(max_length=20)
    gmail = models.EmailField(blank=True, null=True)  # Optional Gmail field

    def __str__(self):
        return self.fullname






from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class NewUpdate(models.Model):
    title = models.CharField(max_length=100)
    image_url = models.URLField(blank=True, null=True, help_text="Optional – paste image URL (e.g., Firebase link)")
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()

    def __str__(self):
        return self.title





from django.db import models

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    has_closed_modal = models.BooleanField(default=False)  # 🆕 Add this line


    def __str__(self):
        return self.email






class DailyNewsletter(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject




from django.db import models

class Donation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    opay_reference = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - ₦{self.amount} - {self.status}"
    








# models.py
class PrayerRequest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)  # 👈 New field
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prayer from {self.name}"




from django.db import models

class WomenMinistryLeader(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='leaders/women/')  # this goes to MEDIA folder

    class Meta:
        verbose_name = "Women Ministry Leader"
        verbose_name_plural = "Women Ministry Leaders"

    def __str__(self):
        return self.name





class MenMinistryLeader(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='leaders/men/')

    class Meta:
        verbose_name = "Men Ministry Leader"
        verbose_name_plural = "Men Ministry Leaders"

    def __str__(self):
        return self.name



class YouthMinistryLeader(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='leaders/youth/')

    class Meta:
        verbose_name = "Youth Ministry Leader"
        verbose_name_plural = "Youth Ministry Leaders"

    def __str__(self):
        return self.name




class EvangelismMinistryLeader(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='leaders/evangelism/')

    class Meta:
        verbose_name = "Evangelism Ministry Leader"
        verbose_name_plural = "Evangelism Ministry Leaders"

    def __str__(self):
        return self.name





class WorshipMinistryLeader(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='leaders/worship/')

    class Meta:
        verbose_name = "Worship Ministry Leader"
        verbose_name_plural = "Worship Ministry Leaders"

    def __str__(self):
        return self.name



from django.db import models

class ChildrenMinistryRegistration(models.Model):
    AGE_GROUP_CHOICES = [
        ('toddlers', 'Toddlers (0–3 yrs)'),
        ('preschool', 'Preschool (4–5 yrs)'),
        ('kids', 'Kids (6–9 yrs)'),
        ('preteens', 'Pre-teens (10–12 yrs)'),
    ]

    parent_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    child_name = models.CharField(max_length=100)
    age_group = models.CharField(max_length=20, choices=AGE_GROUP_CHOICES)
    message = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.child_name} ({self.parent_name})"







class GMSOMSlide(models.Model):
    image_url = models.URLField("Image URL", blank=True, null=True)
    caption = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "GMSOM Slide Image"
        verbose_name_plural = "GMSOM Slide Images"

    def __str__(self):
        return self.caption or f"Slide {self.id}"



# class Testimony(models.Model):
#     emoji = models.CharField(max_length=5, default="🔥")
#     quote = models.TextField()
#     name = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} - {self.quote[:30]}"






from django.db import models


class SchoolOfMinistryRegistration(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    marital_status = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    state_city = models.CharField(max_length=50)
    occupation = models.CharField(max_length=100, blank=True)
    church = models.CharField(max_length=100, blank=True)
    born_again = models.CharField(max_length=10)
    holy_ghost = models.CharField(max_length=10)
    reason = models.TextField()
    photo = models.ImageField(upload_to='registrations/photos/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
