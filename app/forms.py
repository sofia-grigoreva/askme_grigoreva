from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from app.models import Profile, Question, Tag, Answer
from django.core.files.storage import FileSystemStorage
from django.contrib import auth

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form border',
            'placeholder': 'login',
            'id': 'login'
        }),
        label='Login'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form border',
            'placeholder': 'password',
            'id': 'password'
        }),
        label='Password'
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(LoginForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        data = super().clean()
        data['username'] = data['username'].strip()
        data['password'] = data['password'].strip()

        user = auth.authenticate(
            username=data['username'],
            password=data['password']
        )
        if not(user):
            raise forms.ValidationError("Неверный логин или пароль")
        
        
        return data


class RegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form border',
            'placeholder': 'login',
            'id': 'login'
        }),
        label='Login'
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form border',
            'placeholder': 'email',
            'id': 'email'
        }),
        label='Email'
    )
    nickname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form border',
            'placeholder': 'nickname',
            'id': 'nickname'
        }),
        label='NickName'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form border',
            'placeholder': 'password',
            'id': 'password'
        }),
        label='Password'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form border',
            'placeholder': 'repeat password',
            'id': 'password_confirm'
        }),
        label='Repeat password'
    )
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'avatar-input',
            'id': 'avatar',
            'accept': 'image/*',
        }),
        label='Upload avatar',
        required=False
    )

    class Meta:
        model = User
        fields = ("email", "username", "password")

    def clean(self):
        data = super().clean()

        avatar = self.files.get('avatar')
        if avatar:
            data['avatar'] = avatar

        data['username'] = data['username'].strip()
        data['email'] = data['email'].strip()
        data['nickname'] = data['nickname'].strip()
        data['password'] = data['password'].strip()
        data['password_confirm'] = data['password_confirm'].strip()

        if data['password'] != data['password_confirm']:
            self.add_error('password_confirm', 'Passwords do not match')
        
        if Profile.objects.exist(login=data['username']):
            self.add_error('username', 'Login already exists')

        try:
            validate_email(data['email'])
        except ValidationError:
            self.add_error('email', 'Enter a valid email address')

        return data
    
    def save(self):
        data = self.cleaned_data

        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        profile = Profile.objects.create(
            avatar=data['avatar'] if data['avatar'] else 'avatar.jpg',
            user=user,
            nickname=data['nickname']
        )
        return user


class SettingsForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form border',
            'id': 'login',
            'readonly': 'readonly' 
        }),
        label='Login'
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form border',
            'id': 'email'
        }),
        label='Email'
    )
    nickname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form border',
            'id': 'nickname'
        }),
        label='NickName'
    )
    avatar = forms.CharField(
        widget=forms.FileInput(attrs={
            'class': 'avatar-input',
            'id': 'avatar',
            'accept': 'image/*',
        }),
        label='Avatar',
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SettingsForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            self.fields['nickname'].initial = self.user.profile.nickname
    
    def clean(self):
        data = super().clean()

        avatar = self.files.get('avatar')
        if avatar:
            data['avatar'] = avatar

        data['email'] = data['email'].strip()
        data['nickname'] = data['nickname'].strip()

        try:
            validate_email(data['email'])
        except ValidationError:
            self.add_error('email', 'Enter a valid email address')

        return data
    
    def save(self):
        data = self.cleaned_data
        self.user.email = data['email']
        self.user.save()
        profile = self.user.profile
        profile.nickname = data['nickname']
        print(data['avatar'])
        if data['avatar']:
            profile.avatar = data['avatar']
        profile.save()
        return self.user


class AskForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form flex-fill border',
            'placeholder': 'Enter title here...',
            'id': 'title'
        }),
        label='Title'
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form flex-fill border',
            'placeholder': 'Enter text here...',
            'id': 'text'
        }),
        label='Text'
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form flex-fill border',
            'id': 'tags',
            'size': '6',
            'style': 'height: 100px;'
        }),
        label='Tags'
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AskForm, self).__init__(*args, **kwargs)
        self.fields['tags'].label_from_instance = lambda obj: obj.tag

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['text'] = cleaned_data['text'].strip()
        cleaned_data['title'] = cleaned_data['title'].strip()
        return cleaned_data
    
    def save(self):
        data = self.cleaned_data
        print(data)

        question = Question.objects.create(
            title=data['title'],
            text=data['text'],
            author=self.user,
        )

        question.score.set([])
        question.tags.set(data['tags'])

        return question.id


class AnswerForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form flex-fill border',
            'placeholder': 'Enter your answer here...',
            'id': 'ans',
            'aria-label': 'Search',
            'rows': '1'
        }),
        label=''
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.question = kwargs.pop('question', None)
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['text'] = cleaned_data['text'].strip()
        return cleaned_data
    
    def save(self):
        data = self.cleaned_data
        answer = Answer.objects.create(
            text=data['text'],
            author=self.user,
            question=self.question,
            is_checked=False
        )
        answer.score.set([])