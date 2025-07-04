from django import forms
from .models import FileUpload, PDFUpload
from ckeditor.fields import RichTextField
from .models import Hymn, FrenchHymn, Hymn_Content
from django import forms

# ============================
# File Upload Form
# ============================
from django import forms
from .models import FileUpload

class FileUploadForm(forms.ModelForm):
    uploaded_file = forms.FileField(required=False)

    class Meta:
        model = FileUpload
        fields = ['youtube_url', 'date', 'time', 'company_location']

    def clean(self):
        cleaned_data = super().clean()
        uploaded_file = self.files.get('uploaded_file')
        youtube_url = cleaned_data.get('youtube_url')

        if not uploaded_file and not youtube_url:
            raise forms.ValidationError("You must upload a file or provide a YouTube URL.")

# ============================
# PDF Upload Form
# ============================
from django import forms

# ✅ Custom widget
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class PDFUploadForm(forms.Form):
    company_location = forms.CharField(max_length=255)
    info_id = forms.CharField(max_length=255, required=False)
    pdf_files = forms.FileField(
        required=True,
        widget=MultiFileInput(attrs={'multiple': True})
    )
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    image = forms.ImageField(required=False)

# ============================
# Gallery Upload Form
# ============================
class GalleryUploadForm(forms.Form):
    uploaded_files = forms.FileField(
        required=True,
        widget=MultiFileInput(attrs={'multiple': True})
    )
    title = forms.CharField(max_length=255)


class HymnForm(forms.ModelForm):
    class Meta:
        model = Hymn
        fields = ['title', 'image', 'lyrics', 'hymn_type']
        widgets = {
            'lyrics': RichTextField(),  # This ensures CKEditor is used
        }


class FrenchHymnForm(forms.ModelForm):
    class Meta:
        model = FrenchHymn
        fields = ['title', 'image', 'lyrics', 'hymn_type']
        widgets = {
            'lyrics': RichTextField(),  # Ensures CKEditor is used
        }




class EnglishHymnContentForm(forms.ModelForm):
    class Meta:
        model = Hymn_Content
        fields = ['lyrics']  # Include other fields if needed
        widgets = {
            'lyrics': RichTextField(),  # Ensures CKEditor is used
        }



from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['fullname', 'dob', 'profile_image', 'gender', 'phone', 'gmail']





# prayer/forms.py
from django import forms
from .models import PrayerRequest

class PrayerRequestForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['name', 'email', 'message']
