from django import forms

from .models import Item, LendRequest

class DateWidget(forms.DateInput):
    input_type = 'date'


class LendApproveForm(forms.ModelForm):
    class Meta:
        model = LendRequest
        fields = ('status', 'pickup_date', 'return_date') 
        widgets = {
            'status': forms.Select(attrs=
                {
                'class': 'm-2 shadow menu dropdown-content z-[1] bg-base-100 rounded-box w-32 hidden-label'
                }),
            'pickup_date' : DateWidget,
            'return_date' : DateWidget,
        } 


class LendRequestForm(forms.ModelForm):
    class Meta:
        model = LendRequest
        fields = ('pickup_date', 'return_date') 
        widgets = {
            'pickup_date' : DateWidget,
            'return_date' : DateWidget
        } 
        
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        
        fields = ('category', 'title', 'description', 'value', 'image',)
        label = {'category': "", 'title': "", 'description': "", 'value': "", 'image': "Image"}
        widgets = {
            'category': forms.Select(attrs=
                {
                'class': 'm-2 shadow menu dropdown-content z-[1] bg-base-100 rounded-box w-32 hidden-label'
                }),
            'title': forms.TextInput(attrs=
                {
                'class': 'm-2 input input-bordered input-sm w-1/2 max-w-xs'
                }),
            'description': forms.Textarea(attrs=
                {
                'class': 'textarea textarea-bordered textarea-md w-full max-w-xs',
                'rows': 2,
                'placeholder': 'item description',
                }),
            'value': forms.TextInput(attrs=
                {
                'class': 'm-2 input input-bordered input-sm w-1/4 max-w-xs'
                }),
            'image': forms.FileInput(attrs=
                {
                'class': 'file-input file-input-bordered file-input-sm w-full max-w-xs'
                }),
        }




# class LendRequestForm(forms.Form):
#     pickup_date = forms.DateField(widget=DateWidget)
#     return_date = forms.DateField(widget=DateWidget)
    
#     def __init__(self, *args, **kwargs):
#         super(LendRequestForm, self).__init__(*args, **kwargs)
#         self.fields['pickup_date'].label = "Pickup Date"
#         self.fields['return_date'].label = "Return Date"