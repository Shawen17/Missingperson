
from django.contrib import admin
from django.urls import path,include
from  django.conf import settings
from django.conf.urls.static import static
from missing import views
# from django.conf.urls import url
from django.views.static import serve
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('signup/',views.signupuser, name='signupuser'),
    path('login/',views.loginuser, name='loginuser'),
    path('logout/',views.logoutuser, name='logoutuser'),
    path('missingperson/',views.missingperson, name='missingperson'),
    path('found/',views.foundperson, name='foundperson'),
    path('profile/edit', views.edit_profile, name='account_update'),
    #missing
    path('create/',views.createmissing,name='createmissing'),
    path('missing/<int:missing_id>/found',views.found, name= 'found'),
    path('missing/<int:missing_id>/view',views.viewmissing, name= 'viewmissing'),
    path('missing/<int:missing_id>/delete',views.deletemissing, name= 'deletemissing'),
    path('account/',views.user_account, name= 'user_account'),
    path('blog/', include('Blog.urls'), name='blog'),
    path('accounts/',include('allauth.urls')),
    path('social-oauth/',include('social_django.urls'),name='social'),
    path('core/',include('core.urls'),name='core'),
    path('policy/',views.policy,name='policy'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('terms/',views.terms,name='terms'),

]


urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)