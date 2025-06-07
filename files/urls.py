from django.urls import path
from django.conf.urls.i18n import set_language

from . import views  # Make sure to import views here

urlpatterns = [
    path('', views.excel_page, name='excel_page'),  # Ensure the path is registered
    path("login/", views.user_login, name="login"),
    path("home/", views.home, name="home"),  # Home page URL
    path('about/', views.about_view, name='about'),  # Ensure the path is registered
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('coming_soon/', views.coming_soon, name='coming_soon'),
    path("pdf_document/", views.pdf_document, name="pdf_document"),  # Home page URL
    path("logout/", views.user_logout, name="logout"),
    path('search-api/', views.search_api, name='search_api'),
    path('search-results/', views.search_results, name='search_results'),
    path('get_file_for_date/<int:year>/<int:month>/<int:day>/', views.get_file_for_date, name='get_file_for_date'),
    path('gallery/', views.upload_image, name='gallery_upload'),
    path('lookbook/', views.lookbook, name='lookbook'),  # Add this line for the LookBook page
    path('hymns/', views.hymn_list, name='hymn_list'),  # List all hymns
    path('hymns/<int:hymn_id>/', views.hymn_detail, name='hymn_detail'),  # View details of a hymn
    
    path('french-hymns/', views.french_hymn_list, name='french_hymn_list'),
    path('french-hymns/<int:hymn_id>/', views.french_hymn_detail, name='french_hymn_detail'),

    path('yoruba-hymns/', views.yoruba_hymn_list, name='yoruba_hymn_list'),
    path('yoruba-hymns/<int:hymn_id>/', views.yoruba_hymn_detail, name='yoruba_hymn_detail'),

    path('igbo-hymns/', views.igbo_hymn_list, name='igbo_hymn_list'),
    path('igbo-hymns/<int:hymn_id>/', views.igbo_hymn_detail, name='igbo_hymn_detail'),

    path('hausa-hymns/', views.hausa_hymn_list, name='hausa_hymn_list'),
    path('hausa-hymns/<int:hymn_id>/', views.hausa_hymn_detail, name='hausa_hymn_detail'),

    # Chinese Hymns
    path('chinese-hymns/', views.chinese_hymn_list, name='chinese_hymn_list'),
    path('chinese-hymns/<int:hymn_id>/', views.chinese_hymn_detail, name='chinese_hymn_detail'),

    # German Hymns
    path('german-hymns/', views.german_hymn_list, name='german_hymn_list'),
    path('german-hymns/<int:hymn_id>/', views.german_hymn_detail, name='german_hymn_detail'),


    path('hymn_content/', views.hymn_content, name='hymn_content'),

    
    path('contact/', views.contact, name='contact'),  # Ensure the path is registered
    path('submit-contact/', views.submit_contact, name='submit_contact'),

    path('never-show-modal/', views.never_show_modal, name='never_show_modal'),
    path('send-newsletter/', views.send_newsletter, name='send_newsletter'),
    path('signup/', views.signup_view, name='signup'),


    path("donate/", views.donation_form, name="donation_form"),
    path("donate/initiate/", views.initiate_donation, name="initiate_donation"),
    path("paystack/verify/", views.verify_payment, name="verify_payment"),
    path("thank-you/", views.thank_you, name="thank_you"),

    path('set-language/', set_language, name='set_language'),  # 👈 use this


]
