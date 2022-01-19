from django import forms
from django.contrib.auth.models import User
from app.models import Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={"placeholder": "Enter your username here..."}),
                               error_messages={'required': 'Input login'})
    password = forms.CharField(max_length=20,
                               widget=forms.PasswordInput(attrs={"placeholder": "Enter your password here..."}),
                               error_messages={'required': 'Input password'})


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={"placeholder": "Enter your username here..."}),
                               error_messages={'required': 'Input login'})
    password = forms.CharField(max_length=20,
                               widget=forms.PasswordInput(attrs={"placeholder": "Enter your password here..."}),
                               error_messages={'required': 'Input password'})
    confirm_password = forms.CharField(max_length=20,
                                       widget=forms.PasswordInput(attrs={"placeholder": "Confirm your password here..."}),
                                       error_messages={'required': 'Confirm password'})
    profile_pic = forms.ImageField(required=False,
                                   widget=forms.FileInput(attrs={"id": "user-avatar"}))

    def clean_username(self):
        cleaned_data = super(SignupForm, self).clean()
        if User.objects.filter(username=cleaned_data["username"]).exists():
            raise forms.ValidationError("This login has already exist")
        return cleaned_data["username"]

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data["password"]
        confirm_password = cleaned_data["confirm_password"]
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords dont match")
        return cleaned_data


class EditForm(forms.Form):
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={"placeholder": "Enter your username here..."}),
                               error_messages={'required': 'Input login'})
    profile_pic = forms.ImageField(required=False,
                                   widget=forms.FileInput(attrs={"id": "user-avatar"}))


class AskForm(forms.ModelForm):
    tags = forms.CharField(max_length=250, label="Теги",
                           widget=forms.TextInput(attrs={"placeholder": "Enter the tags here"}))

    class Meta:
        model = Question
        fields = ["name", "text"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter the title here"}),
            "text": forms.Textarea(attrs={"placeholder": "Enter the text here"}),
        }

    def clean(self):
        cleaned_data = super(AskForm, self).clean()
        if len(cleaned_data["tags"].split()) > 7:
            raise forms.ValidationError("You can't add more than 7 tags")
        return cleaned_data


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["text"]
        widgets = {"text": forms.Textarea(attrs={"placeholder": "Enter your answer here..."})}