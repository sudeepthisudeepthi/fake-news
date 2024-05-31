from django import forms
from .models import Admin, User, News


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = "__all__"


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ["date_time"]
