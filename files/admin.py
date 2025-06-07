from django.contrib import admin, messages
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.urls import reverse, path
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from django.templatetags.static import static
from django.core.mail import send_mail

import os
import csv
import io
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
    ComingSoonPage, AboutPage, ContactMessage, AutoReplyMessage
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
