from django import forms
from .models import User, Post
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']

    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already in use")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already in use")
        return username


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'date_of_birth',
                  'job', 'bio', 'photo']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("Username already in use")
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.exclude(id=self.instance.id).filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Username already in use")
        return phone_number


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش')
    )

    author_name = forms.CharField(max_length=250, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    phone = forms.CharField(max_length=11, required=True)
    email = forms.EmailField()
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'tags']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=250, widget=forms.Textarea, required=True)