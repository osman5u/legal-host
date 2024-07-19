from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import User, Case, Document, Notification
from django import forms
from .models import Document
from django import forms
from .models import Case


from .models import Document, Case, User

from django import forms
from .models import Document, Case, User

class UploadDocumentForm(forms.ModelForm):
    case = forms.ModelChoiceField(queryset=Case.objects.all(), required=True)

    class Meta:
        model = Document
        fields = ['file', 'case']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['case'].queryset = Case.objects.filter(client=self.user)

    def save(self, commit=True):
        document = super().save(commit=False)
        document.uploaded_by = self.user
        document.lawyer = self.cleaned_data['case'].lawyer
        if commit:
            document.save()
        return document
class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture']


# the new code added

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description', 'due_date']



class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message', 'read']



class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'case', 'lawyer', 'uploaded_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['case'].queryset = Case.objects.all()
        self.fields['lawyer'].queryset = User.objects.filter(lawyer_cases__isnull=False).distinct()




class CaseUpdateForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


# CORRECT UPLOAD FORM

class UploadDocumentForm(forms.ModelForm):
    case = forms.ModelChoiceField(
        queryset=Case.objects.filter(client=None, status='pending'),
        label='Select Case',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    file = forms.FileField(
        label='Upload File',
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = Document
        fields = ['case', 'file']

    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client
        self.fields['case'].queryset = Case.objects.filter(client=client, status='pending')

    def save(self, commit=True):
        document = super().save(commit=False)
        document.lawyer = self.cleaned_data['case'].lawyer
        document.uploaded_by = self.client
        if commit:
            document.save()
        return document
