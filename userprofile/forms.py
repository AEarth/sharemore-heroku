from django import forms

from .models import Userprofile


class UserprofileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ('summary', 'full_text', 'image', 'social_url','location_name', 'lat', 'lon')
        widgets = {
            'summary': forms.TextInput(attrs=
                {
                'class': 'm-3 input input-bordered input-sm w-full max-w-xs',
                'placeholder': 'Your tagline',
                }),            
            'full_text': forms.Textarea(attrs=
                {
                'class': 'textarea textarea-bordered textarea-md w-full max-w-xs',
                'rows': 3,
                'placeholder': 'Tell us more about yourself',
                'label': 'Bio:'
                }),
            'image': forms.FileInput(attrs=
                {
                'class': 'm-2 file-input file-input-bordered file-input-sm w-full max-w-xs',
                }),
            'social_url': forms.URLInput(attrs=
                {
                'class': 'm-2 input input-bordered input-sm w-full max-w-xs',
                'placeholder': 'your social media profile url',
                }),
        }