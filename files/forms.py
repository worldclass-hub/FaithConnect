from django import forms
from .models import FileUpload, PDFUpload
from ckeditor.fields import RichTextField
from .models import Hymn, FrenchHymn, Hymn_Content
from django import forms

# Forms Lines Of Code for Uploading All Files
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['uploaded_file', 'date', 'time', 'company_location']




class PDFUploadForm(forms.Form):
    company_location = forms.CharField(max_length=255)
    info_id = forms.CharField(max_length=255, required=False)
    pdf_files = forms.FileField(  # Regular FileField (No FileInput widget)
        required=True,
    )
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    # Add an image field to the form (Optional image upload)
    image = forms.ImageField(required=False)  # Optional image upload field




class GalleryUploadForm(forms.Form):
    uploaded_files = forms.FileField(required=False)
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
