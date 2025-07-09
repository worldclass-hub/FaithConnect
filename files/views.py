from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.models import User
from email.mime.image import MIMEImage
from urllib.parse import urlparse, parse_qs
from django.conf import settings

from datetime import date, datetime
import os
import re
import uuid
import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from .upload_to_supabase import upload_file_to_supabase
from .supabase_client import supabase  # assuming it's inside 'files' app


# prayer/views.py

from .forms import FileUploadForm, PDFUploadForm, GalleryUploadForm, UserProfileForm, PrayerRequestForm
from .models import (
    FileUpload, PDFUpload, Gallery, Hymn, FrenchHymn, HausaHymn, IgboHymn, YorubaHymn,
    ChineseHymn, GermanHymn, Hymn_Content, AboutPage, ContactMessage, AutoReplyMessage, ComingSoonPage,
    UserProfile, NewUpdate, NewsletterSubscriber, DailyNewsletter, Donation
)
from .models import NewUpdate  # import both models

def welcome_view(request):
    updates = NewUpdate.objects.all().order_by('-upload_date')
    # testimonies = Testimony.objects.all()

    return render(request, 'files/welcome.html', {
        'updates': updates,
        # 'testimonies': testimonies,
    })





def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("excel_page")  # Redirect to home page after login
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "files/login.html")



def coming_soon(request):
    return render(request, "files/coming_soon.html")




















def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        # ✅ Create and login the user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        login(request, user)  # ✅ Log the user in

        messages.success(request, "Account created and logged in successfully!")
        return redirect('excel_page')

    return render(request, 'files/signup.html')


















from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from .upload_to_supabase import upload_file_to_supabase
from .models import FileUpload
import os

@login_required
def home(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            uploaded_file = request.FILES.get("uploaded_file")
            youtube_url = form.cleaned_data.get("youtube_url")
            temp_path = None
            supabase_url = None

            # ✅ Handle file upload
            if uploaded_file:
                print(f"🎯 File selected: {uploaded_file.name}")
                try:
                    # Save temporarily
                    temp_path = f"/tmp/{uploaded_file.name}"
                    with open(temp_path, "wb+") as temp_file:
                        for chunk in uploaded_file.chunks():
                            temp_file.write(chunk)

                    # Upload to Supabase
                    supabase_url = upload_file_to_supabase(temp_path, "user-uploads")
                    print("✅ Supabase URL:", supabase_url)

                    if supabase_url:
                        instance.file_url = supabase_url
                    else:
                        print("❌ Upload failed.")

                except Exception as e:
                    print("❌ Upload error:", e)

                finally:
                    # Always clean up
                    if temp_path and os.path.exists(temp_path):
                        os.remove(temp_path)
                    else:
                        print(f"⚠️ Temp file missing or already removed: {temp_path}")

            # ✅ Manual validation
            if not instance.file_url and not youtube_url:
                form.add_error(None, "You must upload a file or provide a YouTube URL.")
                print("❌ No file or YouTube URL provided")
                return render(request, "files/home.html", {"form": form})

            # ✅ Block PDF
            try:
                if instance.file_url and instance.file_extension() == '.pdf':
                    form.add_error(None, "PDF files are not allowed.")
                    print("❌ PDF is not allowed")
                    return render(request, "files/home.html", {"form": form})
            except Exception as e:
                print("⚠️ Could not check file extension:", e)

            # ✅ Save instance
            instance.youtube_url = youtube_url
            instance.save()
            print("✅ File saved successfully!")
            return redirect("excel_page")
        else:
            print("❌ FORM IS NOT VALID")
            print(form.errors)
    else:
        form = FileUploadForm()

    return render(request, "files/home.html", {"form": form})

















from .upload_to_supabase import upload_file_to_supabase

def excel_page(request):
    # Allowed extensions
    allowed_image_exts = ['.jpg', '.jpeg', '.png', '.gif']
    allowed_video_exts = ['.mp4', '.webm', '.ogg']
    allowed_audio_exts = ['.mp3', '.wav', '.aac']
    allowed_doc_exts = ['.doc', '.docx']
    allowed_ppt_exts = ['.ppt', '.pptx']
    allowed_excel_exts = ['.xls', '.xlsx']
    allowed_zip_exts = ['.zip', '.rar']

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # --- Profile update ---
        if request.FILES.get('profile_image'):
            # ... (your profile update code unchanged)
            pass

        # --- Newsletter subscription ---
        if request.POST.get('email'):
            # ... (your newsletter code unchanged)
            pass

        # --- File or YouTube upload ---
        uploaded_file = request.FILES.get('uploaded_file')
        youtube_url = request.POST.get('youtube_url', '').strip()
        date = request.POST.get('date')
        time = request.POST.get('time')
        company_location = request.POST.get('company_location')

        if not (date and time and company_location):
            return JsonResponse({'status': 'error', 'message': 'Date, time, and company location are required.'})
        if not uploaded_file and not youtube_url:
            return JsonResponse({'status': 'error', 'message': 'Please upload a file or provide a YouTube video URL.'})

        try:
            parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
            parsed_time = datetime.strptime(time, '%H:%M').time()
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid date or time format.'})

        file_url = None
        if uploaded_file:
            try:
                temp_path = f"/tmp/{uploaded_file.name}"
                with open(temp_path, "wb+") as temp_file:
                    for chunk in uploaded_file.chunks():
                        temp_file.write(chunk)

                print("🎯 Uploading:", uploaded_file.name)
                file_url = upload_file_to_supabase(temp_path, "user-uploads")
                os.remove(temp_path)
                print("✅ Uploaded. Supabase URL:", file_url)

            except Exception as e:
                print("❌ Upload error:", e)
                return JsonResponse({'status': 'error', 'message': f"Upload failed: {str(e)}"})

        FileUpload.objects.create(
            file_url=file_url,
            youtube_url=youtube_url if youtube_url else None,
            date=parsed_date,
            time=parsed_time,
            company_location=company_location
        )

        return JsonResponse({'status': 'success', 'message': 'File or video uploaded successfully.'})

    # GET method
    files = FileUpload.objects.all().order_by('-date', '-time')
    selected_date = request.GET.get('date')
    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d')
        files = files.filter(date=selected_date.date())

    user_has_profile = False
    if request.user.is_authenticated:
        user_has_profile = UserProfile.objects.filter(user=request.user).exists()

    updates = NewUpdate.objects.all().order_by('-upload_date')

    return render(request, 'files/excel_page.html', {
        'files': files,
        'user_has_profile': user_has_profile,
        'updates': updates,
        'allowed_image_exts': allowed_image_exts,
        'allowed_video_exts': allowed_video_exts,
        'allowed_audio_exts': allowed_audio_exts,
        'allowed_doc_exts': allowed_doc_exts,
        'allowed_ppt_exts': allowed_ppt_exts,
        'allowed_excel_exts': allowed_excel_exts,
        'allowed_zip_exts': allowed_zip_exts,
    })



@csrf_exempt
def never_show_modal(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email')
        if email:
            NewsletterSubscriber.objects.filter(email=email).update(has_closed_modal=True)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

















from .upload_to_supabase import upload_file_to_supabase

@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('pdf_files')
        image = request.FILES.get('image', None)

        if form.is_valid():
            for file in files:
                if file.name.endswith('.pdf'):
                    temp_path = f"/tmp/{file.name}"
                    with open(temp_path, "wb+") as temp_file:
                        for chunk in file.chunks():
                            temp_file.write(chunk)

                    # Upload PDF to Supabase and get public URL
                    supabase_url = upload_file_to_supabase(temp_path, "user-uploads")

                    # Upload image to Supabase too (optional)
                    image_url = None
                    if image:
                        image_path = f"/tmp/{image.name}"
                        with open(image_path, "wb+") as img_file:
                            for chunk in image.chunks():
                                img_file.write(chunk)
                        image_url = upload_file_to_supabase(image_path, "user-uploads")
                        os.remove(image_path)

                    PDFUpload.objects.create(
                        company_location=form.cleaned_data['company_location'],
                        info_id=form.cleaned_data.get('info_id', ''),
                        pdf_file=supabase_url,
                        date=form.cleaned_data['date'],
                        time=form.cleaned_data['time'],
                        image=image_url or 'login-form/images/pdf_pics.png'
                    )

                    os.remove(temp_path)

            return redirect('pdf_document')
    else:
        form = PDFUploadForm()

    return render(request, 'files/upload_pdf.html', {'form': form})












def pdf_document(request):
    # Handle AJAX profile form submission
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            if UserProfile.objects.filter(user=request.user).exists():
                return JsonResponse({'status': 'error', 'message': "Profile already exists."}, status=400)

            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': "You must be logged in."}, status=400)

    # Fetch all PDFs
    pdf_list = PDFUpload.objects.all().order_by('-id')
    selected_date = request.GET.get('date', None)
    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d')
        pdf_list = pdf_list.filter(date=selected_date.date())

    paginator = Paginator(pdf_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recent_pdfs = PDFUpload.objects.all().order_by('-id')[:5]

    user_has_profile = False
    if request.user.is_authenticated:
        user_has_profile = UserProfile.objects.filter(user=request.user).exists()

    # ✅ Fetch all updates to show in the modal
    updates = NewUpdate.objects.all().order_by('-upload_date')

    return render(request, "files/pdf_document.html", {
        'page_obj': page_obj,
        'recent_pdfs': recent_pdfs,
        'user_has_profile': user_has_profile,
        'updates': updates,  # Pass the updates to the template
    })



def user_logout(request):
    logout(request)
    return redirect("login")

















def extract_youtube_id(url):
    try:
        parsed_url = urlparse(url)
        netloc = parsed_url.netloc.lower()

        if 'youtube.com' in netloc:
            if parsed_url.path.startswith('/shorts/'):
                return parsed_url.path.split('/')[2]
            else:
                query = parse_qs(parsed_url.query)
                return query.get('v', [None])[0]
        elif 'youtu.be' in netloc:
            return parsed_url.path.lstrip('/')
    except Exception:
        return None
    return None

def get_file_for_date(request, year, month, day):
    selected_date = date(year, month, day)
    files = FileUpload.objects.filter(date=selected_date).order_by('-date', '-time')
    pdf_files = PDFUpload.objects.filter(date=selected_date).order_by('-date', '-time')
    all_files = list(files) + list(pdf_files)

    file_data = []
    for file in all_files:
        file_url = ''
        youtube_id = None
        youtube_url = None
        file_extension = ''

        if isinstance(file, FileUpload):
            if file.file_url:
                file_url = file.file_url
                ext = file.file_extension()
                file_extension = ext.lstrip(".") if ext else ''
            elif file.youtube_url:
                youtube_url = file.youtube_url
                youtube_id = extract_youtube_id(youtube_url)
                file_extension = 'youtube'
        else:  # PDFUpload
            file_url = file.pdf_file.url if file.pdf_file else ''
            file_extension = file_url.split('.')[-1].lower().lstrip(".")

        # Safely get image/info_id if they exist
        image_url = file.image.url if hasattr(file, 'image') and file.image else None
        info_id = getattr(file, 'info_id', None)

        file_data.append({
            "file_url": file_url,
            "file_extension": file_extension,
            "company_location": file.company_location,
            "date": file.date.strftime("%Y-%m-%d"),
            "time": file.time.strftime("%I:%M %p"),
            "image_url": image_url,
            "info_id": info_id or "No Info ID",
            "youtube_url": youtube_url,
            "youtube_id": youtube_id,
        })

    return JsonResponse({"files": file_data}) if file_data else JsonResponse({"message": "No file on this selected day."})















@login_required
def upload_image(request):
    if request.method == 'POST':
        form = GalleryUploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            files = request.FILES.getlist('uploaded_files')

            for file in files:
                temp_path = f"/tmp/{file.name}"
                with open(temp_path, "wb+") as temp_file:
                    for chunk in file.chunks():
                        temp_file.write(chunk)

                image_url = upload_file_to_supabase(temp_path, "user-uploads")

                Gallery.objects.create(
                    title=title,
                    uploaded_file=image_url
                )

                os.remove(temp_path)

            return redirect('lookbook')
    else:
        form = GalleryUploadForm()

    return render(request, 'files/gallery_upload.html', {'form': form})



















@login_required
def lookbook(request):
    # Fetch all images from the Gallery model and order them by the most recent
    gallery_images = Gallery.objects.all().order_by('-id')
    
    # Pagination: show 7 images per page
    paginator = Paginator(gallery_images, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ✅ Fetch all NewUpdate records for the modal
    updates = NewUpdate.objects.all().order_by('-upload_date')

    return render(request, 'files/lookbook.html', {
        'page_obj': page_obj,
        'updates': updates,  # Pass updates to template
    })






















# views.py
def hymn_list(request):
    hymns = Hymn.objects.all()
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/hymn_list.html', {'hymns': hymns, 'updates': updates})


def hymn_detail(request, hymn_id):
    hymn = Hymn.objects.get(id=hymn_id)
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/hymn_detail.html', {'hymn': hymn, 'updates': updates})


def french_hymn_list(request):
    hymns = FrenchHymn.objects.all()
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/french_hymn_list.html', {'hymns': hymns, 'updates': updates})


def french_hymn_detail(request, hymn_id):
    hymn = FrenchHymn.objects.get(id=hymn_id)
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/french_hymn_detail.html', {'hymn': hymn, 'updates': updates})


def yoruba_hymn_list(request):
    hymns = YorubaHymn.objects.all()
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/yoruba_hymn_list.html', {'hymns': hymns, 'updates': updates})


def yoruba_hymn_detail(request, hymn_id):
    hymn = YorubaHymn.objects.get(id=hymn_id)
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/yoruba_hymn_detail.html', {'hymn': hymn, 'updates': updates})


def igbo_hymn_list(request):
    hymns = IgboHymn.objects.all()
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/igbo_hymn_list.html', {'hymns': hymns, 'updates': updates})


def igbo_hymn_detail(request, hymn_id):
    hymn = IgboHymn.objects.get(id=hymn_id)
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/igbo_hymn_detail.html', {'hymn': hymn, 'updates': updates})


def hausa_hymn_list(request):
    hymns = HausaHymn.objects.all()
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/hausa_hymn_list.html', {'hymns': hymns, 'updates': updates})


def hausa_hymn_detail(request, hymn_id):
    hymn = HausaHymn.objects.get(id=hymn_id)
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/hausa_hymn_detail.html', {'hymn': hymn, 'updates': updates})



def hymn_content(request):
    hymns = Hymn_Content.objects.all()
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/hymn_content.html', {'hymns': hymns, 'updates': updates})



# Chinese Hymn Views
def chinese_hymn_list(request):
    hymns = ChineseHymn.objects.all()
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/chinese_hymn_list.html', {'hymns': hymns, 'updates': updates})

def chinese_hymn_detail(request, hymn_id):
    hymn = ChineseHymn.objects.get(id=hymn_id)
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/chinese_hymn_detail.html', {'hymn': hymn, 'updates': updates})


# German Hymn Views
def german_hymn_list(request):
    hymns = GermanHymn.objects.all()
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/german_hymn_list.html', {'hymns': hymns, 'updates': updates})

def german_hymn_detail(request, hymn_id):
    hymn = GermanHymn.objects.get(id=hymn_id)
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/german_hymn_detail.html', {'hymn': hymn, 'updates': updates})



















def contact(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email')
        name = 'Subscriber'

        # Try to get user's name if logged in
        if request.user.is_authenticated:
            profile = UserProfile.objects.filter(user=request.user).first()
            if profile and profile.fullname:
                name = profile.fullname
            elif request.user.get_full_name():
                name = request.user.get_full_name()
            elif request.user.username:
                name = request.user.username

        if email:
            if NewsletterSubscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Email already subscribed.', 'email': email})

            NewsletterSubscriber.objects.create(email=email)

            subject = "Thanks for subscribing to our newsletter!"
            text_body = (
                f"Hi {name},\n\n"
                "Thanks for subscribing to our newsletter! "
                "You’re now part of our community and will be the first to receive the latest updates, exclusive content, and special offers.\n\n"
                "We’re excited to have you with us!"
            )
            html_body = text_body.replace('\n', '<br>')

            html_email = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; background: #ffffff; border-radius: 10px; padding: 30px; border: 1px solid #eee;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="https://i.imgur.com/yEFgd2V.png" alt="Admin Logo" style="height: 60px;">
                </div>
                <h2 style="color: #1d3557;">Hello {name},</h2>
                <p style="font-size: 16px; color: #333;">{html_body}</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://gmmi.up.railway.app" style="background: #1d3557; color: white; text-decoration: none; padding: 12px 25px; border-radius: 30px; font-weight: bold;">
                        Visit Our Website
                    </a>
                </div>
                <hr style="border: none; border-top: 1px solid #eee;">
                <div style="text-align: center; margin-top: 20px;">
                    <p style="color: #888; font-size: 14px;">Stay connected with us</p>
                    <div>
                        <a href="https://facebook.com/yourpage" style="margin: 0 5px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" alt="Facebook" style="height: 24px;">
                        </a>
                        <a href="https://twitter.com/yourpage" style="margin: 0 5px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" alt="Twitter" style="height: 24px;">
                        </a>
                        <a href="https://instagram.com/yourpage" style="margin: 0 5px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" alt="Instagram" style="height: 24px;">
                        </a>
                        <a href="https://wa.me/2349057147497?text=Hi%2C%20I%20am%20contacting%20you%20from%20Doxcela" target="_blank" style="margin: 0 5px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" alt="WhatsApp" style="height: 24px;">
                        </a>
                    </div>
                    <p style="color: #aaa; font-size: 12px; margin-top: 10px;">&copy; {datetime.now().year} Doxcela. All rights reserved.</p>
                </div>
            </div>
            """

            # Send the email
            reply_email = EmailMultiAlternatives(subject, text_body, 'doxcela@gmail.com', [email])
            reply_email.attach_alternative(html_email, "text/html")
            reply_email.send()

            return JsonResponse({'status': 'success', 'show_modal': True, 'email': email})

        return JsonResponse({'status': 'error', 'message': 'Email required.'})

    # GET method
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/contact.html', {'updates': updates})


@csrf_exempt
def never_show_modal(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email')
        if email:
            NewsletterSubscriber.objects.filter(email=email).update(has_closed_modal=True)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


















def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        image = request.FILES.get('image')

        # Save to database
        contact = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
            image=image
        )

        # Format message
        formatted_message = message.replace('\n', '<br>')

        image_html = ""
        if image:
            image_html = '''
                <img src="cid:user_image" 
                     style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover; margin-right: 10px; margin-top: 20px;">
            '''

        html_content = f"""
        <div style="font-family: Arial, sans-serif;">
            <h2 style="color: #1d3557;">New Contact Message</h2>
            <div style="display: flex; align-items: center;">
                {image_html}
                <div>
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Phone:</strong> {phone}</p>
                </div>
            </div>
            <br>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Message:</strong><br>{formatted_message}</p>
        </div>
        """

        subject_line = f"New Contact Message: {subject}"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [settings.ADMIN_EMAIL]

        email_message = EmailMultiAlternatives(subject_line, '', from_email, to_email)
        email_message.attach_alternative(html_content, "text/html")

        # 🛠 Attach image to email
        if image:
            image.open()
            img = MIMEImage(image.read(), _subtype=image.content_type.split('/')[-1])
            img.add_header('Content-ID', '<user_image>')
            img.add_header('Content-Disposition', 'inline', filename=image.name)
            email_message.attach(img)

        email_message.send()

        # Auto-reply
        auto_reply = AutoReplyMessage.objects.first()
        if auto_reply:
            reply_subject = auto_reply.subject
            reply_body = auto_reply.message.format(name=name)
        else:
            reply_subject = "Thanks for contacting us"
            reply_body = f"Hi {name},\n\nThanks for reaching out. We'll get back to you shortly.\n\nCheers!"

        # Replace new lines with <br> in the auto-reply message
        reply_body_html = reply_body.replace('\n', '<br>')

        reply_html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; background: #ffffff; border-radius: 10px; padding: 30px; border: 1px solid #eee;">
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="https://i.imgur.com/yEFgd2V.png" alt="Admin Logo" style="height: 60px;">
            </div>
            <h2 style="color: #1d3557;">Hello {name},</h2>
            <p style="font-size: 16px; color: #333;">
                {reply_body_html}
            </p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://gmmi.up.railway.app" style="background: #1d3557; color: white; text-decoration: none; padding: 12px 25px; border-radius: 30px; font-weight: bold;">
                    Visit Our Website
                </a>
            </div>
            <hr style="border: none; border-top: 1px solid #eee;">
            <div style="text-align: center; margin-top: 20px;">
                <p style="color: #888; font-size: 14px;">Stay connected with us</p>
                <div>
                    <a href="https://facebook.com/yourpage" style="margin: 0 5px;">
                        <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" alt="Facebook" style="height: 24px;">
                    </a>
                    <a href="https://twitter.com/yourpage" style="margin: 0 5px;">
                        <img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" alt="Twitter" style="height: 24px;">
                    </a>
                    <a href="https://instagram.com/yourpage" style="margin: 0 5px;">
                        <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" alt="Instagram" style="height: 24px;">
                    </a>
                   <a href="https://wa.me/2349057147497?text=Hi%2C%20I%20am%20contacting%20you%20from%20Doxcela" target="_blank" style="margin: 0 5px;">
                        <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" alt="WhatsApp" style="height: 24px;">
                    </a>


                </div>
                <p style="color: #aaa; font-size: 12px; margin-top: 10px;">&copy; {datetime.now().year} Doxcela. All rights reserved.</p>
            </div>
        </div>
        """

        # Send auto-reply email
        reply_email = EmailMultiAlternatives(reply_subject, reply_body, from_email, [email])
        reply_email.attach_alternative(reply_html, "text/html")
        reply_email.send()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'}, status=400)


















def about_view(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email')
        name = 'Subscriber'

        # Try to get user's name if logged in
        if request.user.is_authenticated:
            if request.user.get_full_name():
                name = request.user.get_full_name()
            elif request.user.username:
                name = request.user.username

        if email:
            if NewsletterSubscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Email already subscribed.', 'email': email})

            NewsletterSubscriber.objects.create(email=email)

            # Compose email content
            reply_subject = "Thanks for subscribing to our newsletter!"
            reply_body = (
                "Thanks for subscribing to our newsletter! "
                "You’re now part of our community and will be the first to receive the latest updates, exclusive content, and special offers.\n\n"
                "We’re excited to have you with us!"
            )
            reply_body_html = reply_body.replace('\n', '<br>')

            # Build HTML email body
            reply_html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; background: #ffffff; border-radius: 10px; padding: 30px; border: 1px solid #eee;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="https://i.imgur.com/yEFgd2V.png" alt="Admin Logo" style="height: 60px;">
                </div>
                <h2 style="color: #1d3557;">Hello {name},</h2>
                <p style="font-size: 16px; color: #333;">{reply_body_html}</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://gmmi.up.railway.app" style="background: #1d3557; color: white; text-decoration: none; padding: 12px 25px; border-radius: 30px; font-weight: bold;">
                        Visit Our Website
                    </a>
                </div>
                <hr style="border: none; border-top: 1px solid #eee;">
                <div style="text-align: center; margin-top: 20px;">
                    <p style="color: #888; font-size: 14px;">Stay connected with us</p>
                    <div>
                        <a href="https://facebook.com/yourpage" style="margin: 0 5px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" alt="Facebook" style="height: 24px;">
                        </a>
                        <a href="https://twitter.com/yourpage" style="margin: 0 5px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" alt="Twitter" style="height: 24px;">
                        </a>
                        <a href="https://instagram.com/yourpage" style="margin: 0 5px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" alt="Instagram" style="height: 24px;">
                        </a>
                        <a href="https://wa.me/2349057147497?text=Hi%2C%20I%20am%20contacting%20you%20from%20Doxcela" target="_blank" style="margin: 0 5px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" alt="WhatsApp" style="height: 24px;">
                        </a>
                    </div>
                    <p style="color: #aaa; font-size: 12px; margin-top: 10px;">&copy; {datetime.now().year} Doxcela. All rights reserved.</p>
                </div>
            </div>
            """

            # Send the email
            email_msg = EmailMultiAlternatives(reply_subject, reply_body, 'doxcela@gmail.com', [email])
            email_msg.attach_alternative(reply_html, "text/html")
            email_msg.send()

            return JsonResponse({'status': 'success', 'show_modal': True, 'email': email})

        return JsonResponse({'status': 'error', 'message': 'Email required.'})

    # GET method
    about = AboutPage.objects.first()
    updates = NewUpdate.objects.all().order_by('-upload_date')
    return render(request, 'files/about.html', {
        'about': about,
        'updates': updates
    })


@csrf_exempt
def never_show_modal(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email')
        if email:
            NewsletterSubscriber.objects.filter(email=email).update(has_closed_modal=True)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

















def coming_soon(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email')
        name = 'Subscriber'

        # Try to get user's name if logged in
        if request.user.is_authenticated:
            profile = UserProfile.objects.filter(user=request.user).first()
            if profile and profile.fullname:
                name = profile.fullname
            elif request.user.get_full_name():
                name = request.user.get_full_name()
            elif request.user.username:
                name = request.user.username

        if email:
            if NewsletterSubscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Email already subscribed.', 'email': email})

            NewsletterSubscriber.objects.create(email=email)

            # Prepare email content
            subject = "Thanks for subscribing to our newsletter!"
            text_body = (
                "Thanks for subscribing to our newsletter! "
                "You’re now part of our community and will be the first to receive the latest updates, exclusive content, and special offers.\n\n"
                "We’re excited to have you with us!"
            )
            html_body = text_body.replace('\n', '<br>')

            # Build the HTML email body
            html_email = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; background: #ffffff; border-radius: 10px; padding: 30px; border: 1px solid #eee;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="https://i.imgur.com/yEFgd2V.png" alt="Admin Logo" style="height: 60px;">
                </div>
                <h2 style="color: #1d3557;">Hello {name},</h2>
                <p style="font-size: 16px; color: #333;">{html_body}</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://gmmi.up.railway.app" style="background: #1d3557; color: white; text-decoration: none; padding: 12px 25px; border-radius: 30px; font-weight: bold;">
                        Visit Our Website
                    </a>
                </div>
                <hr style="border: none; border-top: 1px solid #eee;">
                <div style="text-align: center; margin-top: 20px;">
                    <p style="color: #888; font-size: 14px;">Stay connected with us</p>
                    <div>
                        <a href="https://facebook.com/yourpage" style="margin: 0 5px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" alt="Facebook" style="height: 24px;">
                        </a>
                        <a href="https://twitter.com/yourpage" style="margin: 0 5px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" alt="Twitter" style="height: 24px;">
                        </a>
                        <a href="https://instagram.com/yourpage" style="margin: 0 5px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" alt="Instagram" style="height: 24px;">
                        </a>
                        <a href="https://wa.me/2349057147497?text=Hi%2C%20I%20am%20contacting%20you%20from%20Doxcela" target="_blank" style="margin: 0 5px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" alt="WhatsApp" style="height: 24px;">
                        </a>
                    </div>
                    <p style="color: #aaa; font-size: 12px; margin-top: 10px;">&copy; {datetime.now().year} Doxcela. All rights reserved.</p>
                </div>
            </div>
            """

            # Send the email
            email_msg = EmailMultiAlternatives(subject, text_body, 'doxcela@gmail.com', [email])
            email_msg.attach_alternative(html_email, "text/html")
            email_msg.send()

            return JsonResponse({'status': 'success', 'show_modal': True, 'email': email})

        return JsonResponse({'status': 'error', 'message': 'Email required.'})

    # GET method
    page = ComingSoonPage.objects.last()
    return render(request, 'files/coming_soon.html', {'page': page})


@csrf_exempt
def never_show_modal(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email')
        if email:
            NewsletterSubscriber.objects.filter(email=email).update(has_closed_modal=True)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

















# --- SEARCH BOYS ---
def search_api(request):
    query = request.GET.get('q', '').strip()
    results = []

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            if UserProfile.objects.filter(user=request.user).exists():
                return JsonResponse({'status': 'error', 'message': "Profile already exists."}, status=400)

            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': "You must be logged in."}, status=400)

    if query:
        pdf_results = PDFUpload.objects.filter(
            Q(company_location__icontains=query) |
            Q(info_id__icontains=query) |
            Q(date__icontains=query)
        )

        file_results = FileUpload.objects.filter(
            Q(company_location__icontains=query) |
            Q(date__icontains=query) |
            Q(youtube_url__icontains=query)
        )

        hymn_models = [Hymn, HausaHymn, IgboHymn, YorubaHymn, FrenchHymn, ChineseHymn, GermanHymn]
        for model in hymn_models:
            hymn_results = model.objects.filter(
                Q(title__icontains=query) |
                Q(lyrics__icontains=query) |
                Q(description__icontains=query)
            )
            for hymn in hymn_results:
                results.append({
                    "id": hymn.id,
                    "title": hymn.title or "No Title",
                    "description": hymn.description[:100] + "..." if hymn.description else "",
                    "language": model.__name__.replace('Hymn', '') or 'English',
                    "url": f"/search-results/?q={query}&id={hymn.id}&language={model.__name__.replace('Hymn','').lower()}#hymn-{hymn.id}"
                })

        for pdf in pdf_results:
            results.append({
                "id": pdf.id,
                "name": pdf.pdf_file.name,
                "company_location": pdf.company_location,
                "url": f"/search-results/?q={query}#file-{pdf.id}"
            })

        for file in file_results:
            title = file.company_location or "File"
            results.append({
                "id": file.id,
                "name": title,
                "company_location": file.company_location,
                "youtube_url": file.youtube_url,
                "url": f"/search-results/?q={query}#file-{file.id}"
            })

    user_has_profile = request.user.is_authenticated and UserProfile.objects.filter(user=request.user).exists()
    updates = list(NewUpdate.objects.all().order_by('-upload_date').values('id', 'title', 'upload_date'))

    return JsonResponse({
        "results": results,
        "user_has_profile": user_has_profile,
        "updates": updates
    })


def search_results(request):
    query = request.GET.get('q', '').strip()
    highlight_id = request.GET.get('id')
    highlight_language = request.GET.get('language')

    pdf_results = PDFUpload.objects.filter(
        Q(company_location__icontains=query) |
        Q(info_id__icontains=query) |
        Q(date__icontains=query)
    ) if query else PDFUpload.objects.none()

    file_results = FileUpload.objects.filter(
        Q(company_location__icontains=query) |
        Q(date__icontains=query) |
        Q(youtube_url__icontains=query)
    ) if query else FileUpload.objects.none()

    hymn_models = {
        'english': Hymn,
        'hausa': HausaHymn,
        'igbo': IgboHymn,
        'yoruba': YorubaHymn,
        'french': FrenchHymn,
        'chinese': ChineseHymn,
        'german': GermanHymn,
    }

    highlighted_hymns = None
    if highlight_id and highlight_language in hymn_models:
        highlighted_hymns = hymn_models[highlight_language].objects.filter(id=highlight_id)

    user_has_profile = request.user.is_authenticated and UserProfile.objects.filter(user=request.user).exists()

    pdf_results_with_images = []
    for pdf in pdf_results:
        image_url = pdf.image.url if pdf.image else static('login-form/images/PDF_image.jpeg')
        pdf_results_with_images.append({
            "id": pdf.id,
            "name": pdf.pdf_file.name,
            "company_location": pdf.company_location,
            "url": f"/pdf-view/{pdf.id}/",
            "image": image_url,
            "pdf_file": pdf.pdf_file,
            "date": pdf.date,
            "time": pdf.time,
            "info_id": pdf.info_id
        })

    recent_files = FileUpload.objects.order_by('-date')[:6]
    recent_pdfs = PDFUpload.objects.order_by('-date', '-time')[:6]
    updates = NewUpdate.objects.all().order_by('-upload_date')

    return render(request, "files/search_results.html", {
        "query": query,
        "pdf_results": pdf_results_with_images,
        "file_results": file_results,
        "highlighted_hymns": highlighted_hymns,
        "highlight_language": highlight_language,
        "recent_files": recent_files,
        "recent_pdfs": recent_pdfs,
        "user_has_profile": user_has_profile,
        "updates": updates
    })















@login_required
def send_newsletter(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        # Find all image URLs in the body from the media folder
        image_matches = re.findall(r'src="(/media/[^"]+)"', body)
        attached_images = {}

        for image_url in image_matches:
            image_filename = os.path.basename(image_url)
            image_cid = image_filename  # This will be the Content-ID
            image_path_relative = image_url.replace('/media/', '')  # Remove /media/ from URL
            full_image_path = os.path.join(settings.MEDIA_ROOT, image_path_relative)

            # Replace <img src="..."> with CID and add width & height styling
            pattern = f'src="{image_url}"'
            replacement = f'src="cid:{image_cid}" style="width:600px; height:300px;"'
            body = body.replace(pattern, replacement)

            # Only attach the image if the file actually exists
            if os.path.exists(full_image_path):
                attached_images[image_cid] = full_image_path

        # Send to all newsletter subscribers
        subscribers = NewsletterSubscriber.objects.all()

        for subscriber in subscribers:
            email = EmailMultiAlternatives(
                subject=subject,
                body='This is the fallback plain text version.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email],
            )
            email.attach_alternative(body, "text/html")

            # Attach images as inline MIMEImage
            for cid, path in attached_images.items():
                with open(path, 'rb') as img_file:
                    mime_img = MIMEImage(img_file.read())
                    mime_img.add_header('Content-ID', f'<{cid}>')
                    mime_img.add_header('Content-Disposition', 'inline', filename=cid)
                    email.attach(mime_img)

            email.send(fail_silently=False)

        # Save newsletter record
        DailyNewsletter.objects.create(subject=subject, body=body)

        # Redirect to the same page with a success flag
        return redirect('/send-newsletter/?sent=true')

    # GET request: Render the page with all subscribers
    subscribers = NewsletterSubscriber.objects.all()
    return render(request, 'files/send_newsletter.html', {'subscribers': subscribers})













import uuid
import requests
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Donation

def donation_form(request):
    return render(request, "files/donation_form.html")

def initiate_donation(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        amount = request.POST.get("amount")
        phone = request.POST.get("phone", "")

        try:
            amount_float = float(amount)
            if amount_float < 100:
                return render(request, "files/error.html", {"message": "Minimum donation is ₦100"})
        except:
            return render(request, "files/error.html", {"message": "Invalid amount"})

        reference = f"PAYSTACK-{uuid.uuid4().hex[:10].upper()}"

        Donation.objects.create(
            name=name,
            email=email,
            phone=phone,
            amount=amount_float,
            reference=reference,
            status="pending"
        )

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        callback_url = f"{settings.PAYSTACK_CALLBACK_URL}/paystack/verify/"
        return_url = f"{settings.PAYSTACK_CALLBACK_URL}/thank-you/?ref={reference}"

        payload = {
            "email": email,
            "amount": int(amount_float * 100),
            "reference": reference,
            "callback_url": callback_url,
            "return_url": return_url,
        }

        response = requests.post("https://api.paystack.co/transaction/initialize", json=payload, headers=headers)
        data = response.json()

        if data.get("status"):
            auth_url = data["data"]["authorization_url"]
            return redirect(auth_url)
        else:
            return render(request, "files/error.html", {"message": "Paystack Error: Unable to initiate payment"})

    return redirect("donation_form")

@csrf_exempt
def verify_payment(request):
    reference = request.GET.get("reference")
    if not reference:
        return render(request, "files/error.html", {"message": "No reference provided for verification."})

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(url, headers=headers)
    data = response.json()

    if data.get("status") and data["data"]["status"] == "success":
        try:
            donation = Donation.objects.get(reference=reference)
            donation.status = "paid"
            donation.save()
        except Donation.DoesNotExist:
            pass
        return redirect(f"/thank-you/?ref={reference}")
    else:
        return render(request, "files/error.html", {"message": "Payment verification failed."})

def thank_you(request):
    ref = request.GET.get("ref")
    donation = None
    if ref:
        try:
            donation = Donation.objects.get(reference=ref)
        except Donation.DoesNotExist:
            donation = None

    return render(request, "files/thank_you.html", {"donation": donation})







from .models import ChildrenMinistryPhoto

def children_ministry(request):
    photos = ChildrenMinistryPhoto.objects.all()
    return render(request, 'files/children_ministry.html', {'photos': photos})






from django.shortcuts import render
from .models import WomenMinistryLeader

def women_ministry(request):
    leaders = WomenMinistryLeader.objects.all()
    return render(request, 'files/women_ministry.html', {'leaders': leaders})





from .models import EvangelismMinistryLeader

def evangelism_ministry(request):
    leaders = EvangelismMinistryLeader.objects.all()
    return render(request, 'files/evangelism_ministry.html', {'leaders': leaders})






from .models import YouthMinistryLeader

def youth_ministry(request):
    leaders = YouthMinistryLeader.objects.all()
    return render(request, 'files/youth_ministry.html', {'leaders': leaders})







from .models import MenMinistryLeader

def men_ministry(request):
    leaders = MenMinistryLeader.objects.all()
    return render(request, 'files/men_ministry.html', {'leaders': leaders})







from .models import GMSOMSlide

def overview(request):
    slides = GMSOMSlide.objects.all()
    return render(request, 'files/overview.html', {'slides': slides})








def prayer_request_view(request):
    if request.method == 'POST':
        form = PrayerRequestForm(request.POST)
        if form.is_valid():
            prayer = form.save()

            # Send confirmation email
            send_mail(
                subject="🙏 Your Prayer Request Was Received",
                message=(
                    f"Dear {prayer.name},\n\n"
                    f"Thank you for your prayer request:\n\n"
                    f"\"{prayer.message}\"\n\n"
                    f"We are standing with you in faith!\n\n"
                    f"Blessings,\nGMMIConnect Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[prayer.email],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'invalid'}, status=405)






# def testimony_view(request):
#     testimonies = Testimony.objects.all().order_by('-created_at')
#     return render(request, 'files/testimony.html', {'testimonies': testimonies})
