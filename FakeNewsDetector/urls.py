from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [path("", views.index, name="index"),
               path("Login.html", views.Login, name="Login"),
               path("AdminLogin", views.AdminLogin, name="AdminLogin"),
               path("LoginAdmin", views.LoginAdmin, name="LoginAdmin"),
               path("addnews", views.addnews, name="addnews"),
               path("addnews1", views.addnews1, name="addnews1"),
               path("UploadNews.html", views.UploadNews, name="UploadNews"),
               path("UploadNewsDocument", views.UploadNewsDocument, name="UploadNewsDocument"),
               path("DetectorAlgorithm", views.DetectorAlgorithm, name="DetectorAlgorithm"),
               path("ViewNews", views.ViewNews, name="ViewNews"),
               path("ViewNews1", views.ViewNews1, name="ViewNews1"),
               path("admin", views.admin, name="admin"),
               path("ChngPassword", views.ChngPassword, name="ChngPassword"),
               path("userreg", views.userreg, name="userreg"),
               path("update_news", views.update_news, name="update_news"),
               path("edit_news/<int:id>", views.edit_news, name="edit_news"),
               path('delete/<int:id>', views.delete, name="delete"),

               ]
if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
