from django import forms
from .models import Inquiry

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your Email"}),
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject"}),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Message"}),
    )


class NewsletterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your Email"}),
    )

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = "__all__"
        widgets = {
            "courses": forms.CheckboxSelectMultiple
        }