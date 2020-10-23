"""studiopal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("registration.backends.simple.urls")),
    path(
        "studiopal/add_comment/<int:video_pk>/", views.add_comment, name="add_comment"
    ),
    path("studiopal/landing_page/", views.landing_page, name="landing_page"),
    path(
        "studiopal/<int:user_pk>/add_studio_info/",
        views.add_studio_info,
        name="add_studio_info",
    ),
    path("studiopal/<int:user_pk>/", views.studio_detail, name="studio_detail"),
    path("studiopal/video_upload/", views.video_upload, name="video_upload"),
    path(
        "studiopal/video_detail/<int:video_pk>/",
        views.video_detail,
        name="video_detail",
    ),
    path("studiopal/user_detail/<int:user_pk>/", views.user_detail, name="user_detail"),
    path("", views.landing_page, name="landing_page"),
    path("studiopal/about/", views.about, name="about"),
    path(
        "studiopal/search_results/",
        views.search_instructors_videos,
        name="search_results",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = (
        [
            path("__debug__/", include(debug_toolbar.urls)),
            # For django versions before 2.0:
            # url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
        + urlpatterns
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
