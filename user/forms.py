from django import forms


from django.contrib.auth.models import User


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ('last_login', 'is_superuser', 'is_staff', 'date_joined', 'user_permissions', 'groups', 'password',
                   'username')
