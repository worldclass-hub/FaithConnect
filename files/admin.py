from django.contrib import admin, messages
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.urls import reverse, path
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from django.templatetags.static import static
from django.core.mail import send_mail
from io import BytesIO

# PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

# Word
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from PIL import Image
from docx.oxml import parse_xml  # ✅ Correct import
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


import os
import csv
import io
import csv
import datetime
from calendar import month_name
from collections import defaultdict
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from ckeditor.widgets import CKEditorWidget

from .models import (
    FileUpload, PDFUpload, Gallery, Hymn, Hymn_Content,
    FrenchHymn, YorubaHymn, IgboHymn, HausaHymn, ChineseHymn, GermanHymn,
    NewsletterSubscriber, DailyNewsletter,
    NewUpdate, UserProfile,
    ComingSoonPage, AboutPage, ContactMessage, AutoReplyMessage, PrayerRequest
)























@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    # Ensure the 'file_icon' method is included in list_display
    list_display = ('date', 'time', 'company_location', 'file_icon', 'uploaded_file')

    def file_icon(self, obj):
        """Show a file icon based on the file extension (excluding PDF)"""
        ext = os.path.splitext(obj.uploaded_file.name)[1].lower()  # Get the file extension
        
        # Check for common file types and return appropriate icons
        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
            icon = 'image-icon.png'
        elif ext == '.txt':
            icon = 'text-icon.png'
        elif ext == '.zip':
            icon = 'zip-icon.png'
        else:
            icon = 'default-file-icon.png'  # Fallback for unsupported file types

        # Return the icon HTML, ensure it's being pulled from static path correctly
        icon_url = static(f'login-form/images/{icon}')
        return format_html('<img src="{}" width="30" style="object-fit: contain;" />', icon_url)

    file_icon.short_description = 'File Icon'  # Change column name in the admin panel















@admin.register(PDFUpload)
class PDFUploadAdmin(admin.ModelAdmin):
    list_display = ('company_location', 'info_id', 'pdf_file', 'date', 'time')











class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_display')  # Custom method to display image

    def image_display(self, obj):
        return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.uploaded_file.url)
    image_display.short_description = 'Image'

admin.site.register(Gallery, GalleryAdmin)


















class HymnAdmin(admin.ModelAdmin):
    list_display = ('title', 'hymn_type', 'image', 'description')
    search_fields = ('title', 'description', 'hymn_type')

admin.site.register(Hymn, HymnAdmin)












class ChineseHymnAdmin(admin.ModelAdmin):
    list_display = ('title', 'hymn_type', 'image', 'description')
    search_fields = ('title', 'description', 'hymn_type')

admin.site.register(ChineseHymn, ChineseHymnAdmin)









class GermanHymnAdmin(admin.ModelAdmin):
    list_display = ('title', 'hymn_type', 'image', 'description')
    search_fields = ('title', 'description', 'hymn_type')

admin.site.register(GermanHymn, GermanHymnAdmin)












class FrenchHymnAdmin(admin.ModelAdmin):
    list_display = ('title', 'hymn_type', 'image', 'description')
    search_fields = ('title', 'description', 'hymn_type')

admin.site.register(FrenchHymn, FrenchHymnAdmin)

















class YorubaHymnAdmin(admin.ModelAdmin):
    list_display = ('title', 'hymn_type', 'image', 'description')
    search_fields = ('title', 'description', 'hymn_type')

admin.site.register(YorubaHymn, YorubaHymnAdmin)

















class IgboHymnAdmin(admin.ModelAdmin):
    list_display = ('title', 'hymn_type', 'image', 'description')
    search_fields = ('title', 'description', 'hymn_type')

admin.site.register(IgboHymn, IgboHymnAdmin)

















class HausaHymnAdmin(admin.ModelAdmin):
    list_display = ('title', 'hymn_type', 'image', 'description')
    search_fields = ('title', 'description', 'hymn_type')

admin.site.register(HausaHymn, HausaHymnAdmin)
















@admin.register(Hymn_Content)
class EnglishHymnAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'short_lyrics')
    search_fields = ('lyrics',)

    def short_lyrics(self, obj):
        return (obj.lyrics[:75] + '...') if len(obj.lyrics) > 75 else obj.lyrics
    short_lyrics.short_description = 'Lyrics'


















@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        count = queryset.count()
        # This is just a placeholder action – it doesn't change anything yet
        messages.success(request, f"{count} message(s) marked as resolved.")
    
    mark_as_resolved.short_description = "Mark selected messages as resolved"
















@admin.register(AutoReplyMessage)
class AutoReplyMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message')
    search_fields = ('subject', 'message')



















class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'email', 'history', 'the_man', 'mandate')
    search_fields = ('title', 'phone', 'email')
    list_filter = ('title',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'history', 'more_history', 'the_man', 'mission_statement', 'vision', 'value', 'mandate')
        }),
        ('Contact Information', {
            'fields': ('contact_address', 'phone', 'email')
        }),
        ('Images', {
            'fields': ('image1', 'image2', 'image3')
        }),
    )

    # You can customize the save behavior if necessary (e.g., auto-cleaning or additional logic)
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


admin.site.register(AboutPage, AboutPageAdmin)
















# admin.py

@admin.register(ComingSoonPage)
class ComingSoonPageAdmin(admin.ModelAdmin):
    list_display = ('id', 'note', 'updated_at', 'background_preview')
    readonly_fields = ('background_preview',)

    def background_preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.background_image.url)
        return "No image uploaded"

    background_preview.short_description = "Background Image Preview"
















@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'dob', 'gender', 'phone', 'gmail', 'profile_image_tag')
    list_filter = ('dob',)
    search_fields = ('fullname', 'gmail', 'phone')
    change_list_template = 'files/custom_content_wrapper.html'

    def profile_image_tag(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 6px;" />',
                obj.profile_image.url
            )
        return "-"
    profile_image_tag.short_description = 'Profile Image'

    def changelist_view(self, request, extra_context=None):
        grouped_profiles = defaultdict(list)
        for profile in UserProfile.objects.all():
            month = profile.dob.strftime('%B') if profile.dob else 'Unknown'
            grouped_profiles[month].append(profile)

        months_order = list(month_name)[1:]
        sorted_profiles = {month: grouped_profiles.get(month, []) for month in months_order}

        extra_context = extra_context or {}
        extra_context['months'] = sorted_profiles
        extra_context['title'] = "User Profiles by Month"
        extra_context['app_label'] = 'files'
        extra_context['delete_url'] = self.get_delete_url()

        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('delete/<int:profile_id>/', self.admin_site.admin_view(self.delete_profile), name='delete_profile'),
            path('autocomplete/', self.admin_site.admin_view(self.autocomplete_search), name='userprofile_autocomplete'),
            path('export/csv/', self.admin_site.admin_view(self.export_profiles_csv), name='export_profiles_csv'),
            path('export/pdf/', self.admin_site.admin_view(self.export_profiles_pdf), name='export_profiles_pdf'),
        ]
        return custom_urls + urls

    def get_delete_url(self):
        return '/admin/files/userprofile/delete/'

    def delete_profile(self, request, profile_id):
        try:
            profile = UserProfile.objects.get(pk=profile_id)
            profile.delete()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Profile deleted successfully!'})
            else:
                self.message_user(request, "Profile deleted successfully!")
                return redirect('/admin/files/userprofile/')
        except UserProfile.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Profile not found!'}, status=404)
            else:
                self.message_user(request, "Profile not found!", level="error")
                return redirect('/admin/files/userprofile/')

    def autocomplete_search(self, request):
        query = request.GET.get('q', '')
        results = []

        if query:
            profiles = UserProfile.objects.filter(
                Q(fullname__icontains=query) |
                Q(gmail__icontains=query) |
                Q(phone__icontains=query)
            )
            results = [
                {
                    'id': profile.id,
                    'label': profile.fullname,
                    'month': profile.dob.strftime('%B') if profile.dob else 'Unknown',
                }
                for profile in profiles
            ]
        return JsonResponse(results, safe=False)

    def export_profiles_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="All Users BirthDay Profile.csv"'

        writer = csv.writer(response)
        writer.writerow(['S/N', 'Full Name', 'DOB', 'Gender', 'Phone', 'Gmail', 'Month'])

        for index, profile in enumerate(UserProfile.objects.all().order_by('dob'), start=1):
            month = profile.dob.strftime('%B') if profile.dob else 'Unknown'
            writer.writerow([
                index,
                profile.fullname,
                profile.dob,
                profile.gender,
                profile.phone,
                profile.gmail,
                month
            ])
        return response

    def export_profiles_pdf(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="All Users BirthDay Profile.pdf"'

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        
        # Set PDF document title
        p.setTitle("All User Profiles with DOB")

        width, height = A4

        y = height - 40
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, "All User Profile With D.O.B")
        y -= 30

        p.setFillColor(colors.green)
        p.rect(40, y, width - 80, 20, fill=True)
        p.setFillColor(colors.white)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(45, y + 5, "S/N")
        p.drawString(110, y + 5, "Full Name")
        p.drawString(230, y + 5, "DOB")
        p.drawString(310, y + 5, "Gender")
        p.drawString(400, y + 5, "Phone")
        p.drawString(500, y + 5, "Month")
        y -= 20

        p.setFont("Helvetica", 9)
        row_color = colors.white
        for index, profile in enumerate(UserProfile.objects.all().order_by('dob'), start=1):
            month = profile.dob.strftime('%B') if profile.dob else 'Unknown'

            # Alternating row colors
            if row_color == colors.white:
                row_color = colors.lightgrey
            else:
                row_color = colors.white

            p.setFillColor(row_color)
            p.rect(40, y, width - 80, 20, fill=True)

            p.setFillColor(colors.black)
            p.drawString(45, y + 5, str(index))
            p.drawString(110, y + 5, profile.fullname)
            p.drawString(230, y + 5, str(profile.dob))
            p.drawString(310, y + 5, profile.gender)
            p.drawString(400, y + 5, profile.phone)
            p.drawString(500, y + 5, month)

            y -= 25
            if y < 50:
                p.showPage()
                y = height - 40
                p.setFillColor(colors.green)
                p.rect(40, y, width - 80, 20, fill=True)
                p.setFillColor(colors.white)
                p.setFont("Helvetica-Bold", 10)
                p.drawString(45, y + 5, "S/N")
                p.drawString(110, y + 5, "Full Name")
                p.drawString(230, y + 5, "DOB")
                p.drawString(310, y + 5, "Gender")
                p.drawString(400, y + 5, "Phone")
                p.drawString(500, y + 5, "Month")
                y -= 20

        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response





class NewUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date', 'user')
    search_fields = ('title',)

admin.site.register(NewUpdate, NewUpdateAdmin)














# Custom action to send a newsletter to all subscribers
@admin.action(description="Send selected newsletter to all subscribers")
def send_newsletter_to_all(modeladmin, request, queryset):
    for newsletter in queryset:
        subscribers = NewsletterSubscriber.objects.all()
        for subscriber in subscribers:
            send_mail(
                newsletter.subject,
                newsletter.body,
                'doxcela@gmail.com',  # Sender's email (make sure it matches your settings)
                [subscriber.email],
                fail_silently=False,
            )
    modeladmin.message_user(request, "Newsletter sent successfully.")

# Admin configuration for DailyNewsletter
class DailyNewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date_posted')
    actions = [send_newsletter_to_all]  # Add custom action here

# Registering models in the admin panel
admin.site.register(NewsletterSubscriber)  # To show the list of subscribers
admin.site.register(DailyNewsletter, DailyNewsletterAdmin)  # To show the newsletter list and actions










@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'created_at')
    ordering = ('-created_at',)
    actions = ['export_as_csv', 'export_as_pdf', 'export_as_word']

    def has_add_permission(self, request):
        return False

    # ✅ CSV Export
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="prayer_requests.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Message', 'Created At'])
        for prayer in queryset:
            writer.writerow([prayer.name, prayer.email, prayer.message, prayer.created_at])
        return response
    export_as_csv.short_description = "📤 Export selected to CSV"

    # ✅ PDF Export
    def export_as_pdf(self, request, queryset):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        y = height - 100
        page_number = 1

        logo_path = os.path.join('static', 'login-form', 'images', 'GMMI_LOGO.png')
        watermark_text = "GMMIConnect"

        def draw_header():
            nonlocal y
            try:
                logo = ImageReader(logo_path)
                p.drawImage(logo, 40, height - 80, width=60, height=60, mask='auto')
            except:
                pass
            p.setFont("Helvetica-Bold", 16)
            p.drawString(110, height - 60, "Prayer Requests Report")
            p.setFont("Helvetica", 10)
            p.drawRightString(width - 40, height - 60, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            y = height - 100

        def draw_footer():
            p.setFont("Helvetica-Oblique", 8)
            p.setFillColor(colors.grey)
            p.drawCentredString(width / 2.0, 20, f"Page {page_number}")
            p.saveState()
            p.setFont("Helvetica-Bold", 40)
            p.setFillColorRGB(0.9, 0.9, 0.9)
            p.translate(width / 2, height / 2)
            p.rotate(45)
            p.drawCentredString(0, 0, watermark_text)
            p.restoreState()

        draw_header()
        p.setFont("Helvetica", 11)

        for obj in queryset:
            if y < 100:
                draw_footer()
                p.showPage()
                page_number += 1
                draw_header()
                p.setFont("Helvetica", 11)

            p.setFillColor(colors.black)
            p.drawString(50, y, f"Name: {obj.name}")
            y -= 18
            p.drawString(50, y, f"Email: {obj.email}")
            y -= 18
            p.drawString(50, y, f"Date: {obj.created_at.strftime('%Y-%m-%d %H:%M')}")
            y -= 18
            p.drawString(50, y, "Message:")
            y -= 16

            for line in obj.message.splitlines():
                if y < 80:
                    draw_footer()
                    p.showPage()
                    page_number += 1
                    draw_header()
                    p.setFont("Helvetica", 11)
                p.drawString(70, y, line.strip())
                y -= 14

            y -= 20

        draw_footer()
        p.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf', headers={
            'Content-Disposition': 'attachment; filename="prayer_requests.pdf"'
        })
    export_as_pdf.short_description = "🧾 Export selected to PDF"

    # ✅ Word Export with Watermark + Logo
    def export_as_word(self, request, queryset):
        document = Document()
        section = document.sections[0]
        header = section.header
        header_paragraph = header.paragraphs[0]

        # 🔰 Logo
        logo_path = os.path.join('static', 'login-form', 'images', 'GMMI_LOGO.png')
        if os.path.exists(logo_path):
            run = header_paragraph.add_run()
            run.add_picture(logo_path, width=Inches(1.5))
            header_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # 💧 Watermark using VML XML
        watermark_paragraph = header.add_paragraph()
        watermark_run = watermark_paragraph.add_run()

        shape_xml = r"""
        <w:pict xmlns:v="urn:schemas-microsoft-com:vml"
                xmlns:w="urn:schemas-microsoft-com:office:word"
                xmlns:o="urn:schemas-microsoft-com:office:office">
            <v:shape id="WordArt1" o:spid="_x0000_s1025" type="#_x0000_t136"
                     style="position:absolute; margin-left:0; margin-top:0;
                            width:500pt; height:100pt; z-index:-251654144;
                            mso-wrap-edited:f; rotation:315"
                     fillcolor="#e6e6e6" stroked="f">
                <v:textpath style="font-family:Calibri; font-size:36pt"
                            on="t" string="GMMIConnect"/>
                <v:fill opacity="0.1"/>
            </v:shape>
        </w:pict>
        """
        watermark_element = parse_xml(shape_xml)  # ✅ fixed line
        watermark_run._r.append(watermark_element)

        # 📄 Title
        document.add_paragraph()
        title = document.add_heading("Prayer Requests Report", level=1)
        title.runs[0].font.size = Pt(24)
        title.runs[0].font.name = "Calibri"

        # 🗓️ Date
        date_paragraph = document.add_paragraph()
        date_run = date_paragraph.add_run(f"Date Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        date_run.bold = True
        date_run.font.size = Pt(10)
        date_run.font.name = "Calibri"
        document.add_paragraph()

        for obj in queryset:
            header = document.add_paragraph()
            header_run = header.add_run("🧎🏽 Prayer Request")
            header_run.bold = True
            header_run.font.size = Pt(13)
            header_run.font.name = "Calibri"
            header_run.font.color.rgb = RGBColor(46, 116, 181)

            p1 = document.add_paragraph()
            r1 = p1.add_run(f"Name: {obj.name}")
            r1.bold = True
            r1.font.size = Pt(11)

            p2 = document.add_paragraph()
            r2 = p2.add_run(f"Email: {obj.email}")
            r2.font.size = Pt(11)

            p3 = document.add_paragraph()
            r3 = p3.add_run(f"Date: {obj.created_at.strftime('%Y-%m-%d %H:%M')}")
            r3.font.size = Pt(11)

            document.add_paragraph("Message:", style="Intense Quote")

            for line in obj.message.splitlines():
                msg_paragraph = document.add_paragraph()
                msg_run = msg_paragraph.add_run(line.strip())
                msg_run.italic = True
                msg_run.font.size = Pt(10)
                msg_run.font.color.rgb = RGBColor(100, 100, 100)

            document.add_paragraph("\n")

        buffer = BytesIO()
        document.save(buffer)
        buffer.seek(0)

        return HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            headers={'Content-Disposition': 'attachment; filename="prayer_requests.docx"'}
        )
    export_as_word.short_description = "📝 Export selected to Word (.docx)"







from django.contrib import admin
from .models import WomenMinistryLeader

@admin.register(WomenMinistryLeader)
class WomenMinistryLeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'title']






from .models import MenMinistryLeader

@admin.register(MenMinistryLeader)
class MenMinistryLeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'title']






from .models import YouthMinistryLeader

@admin.register(YouthMinistryLeader)
class YouthMinistryLeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'title']





from .models import EvangelismMinistryLeader

@admin.register(EvangelismMinistryLeader)
class EvangelismMinistryLeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'title']





from .models import WorshipMinistryLeader

@admin.register(WorshipMinistryLeader)
class WorshipMinistryLeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'title']



from .models import ChildrenMinistryPhoto

@admin.register(ChildrenMinistryPhoto)
class ChildrenMinistryPhotoAdmin(admin.ModelAdmin):
    list_display = ['caption', 'image']





from .models import GMSOMSlide

@admin.register(GMSOMSlide)
class GMSOMSlideAdmin(admin.ModelAdmin):
    list_display = ['caption', 'image']






















# from .models import Testimony


# @admin.register(Testimony)
# class TestimonyAdmin(admin.ModelAdmin):
#     list_display = ("name", "quote", "created_at")
#     search_fields = ("name", "quote")
