from django import forms
from django_fsm import FSMField

from .models import Item, LendRequest, WorkflowState


class DateWidget(forms.DateInput):
    input_type = 'date'
    
class WorkflowWidget(forms.Select):
    input_type = 'select',
    #choices = LendRequest.workflow_state.choices(),
    #class = 'm-2 shadow menu dropdown-content z-[1] bg-base-100 rounded-box w-32 hidden-label'


def get_available_fsm_transitions(instance, field_name):
    # Get the FSMField instance on the model
    fsm_field = instance._meta.get_field(field_name)
    current_state = getattr(instance, field_name)
    
    # Get the list of available transitions based on source state
    transitions = [
        transition for transition in fsm_field.get_all_transitions(instance.__class__)
        if transition.source == current_state
    ]
    
    return transitions

CHOICES = WorkflowState.CHOICES

def get_choices():
    return [CHOICES[0], CHOICES[1]]

def get_status_choices():
    return [('p', 'Pending'),('d', 'Denied')]

class LendApproveForm(forms.ModelForm):
    class Meta:
        model = LendRequest
        fields = ('status', 'workflow_state', 'pickup_date', 'return_date') 
        widgets = {
            'status': forms.HiddenInput(),
            'workflow_state': forms.Select(attrs=
                {
                'class': 'm-2 shadow menu dropdown-content z-[1] bg-base-100 rounded-box w-32 hidden-label'
                }),
            'pickup_date' : DateWidget,
            'return_date' : DateWidget,
        }
        
    def __init__(self, *args, **kwargs):
        super(LendApproveForm, self).__init__(*args, **kwargs)
        self.fields['status'] = forms.ChoiceField(choices=get_status_choices())

    
        instance = kwargs.get('instance')
        if instance:
            # Get available transitions for the current state
            available_transitions = instance.get_available_workflow_state_transitions()
            limited_choices = [(t.target, t.target) for t in available_transitions]
            
            # Update the field's choices
            self.fields['workflow_state'] = forms.ChoiceField(choices=limited_choices)

            
class LendStatusUpdateForm(forms.ModelForm):

    class Meta:
        model = LendRequest
        fields = ('workflow_state',) 
        widgets = {
            'workflow_state': forms.Select(attrs=
                {
                'class': 'm-2 shadow menu dropdown-content z-[1] bg-base-100 rounded-box w-32 hidden-label'
                }),
        }
        
    def __init__(self, *args, **kwargs):
        super(LendStatusUpdateForm, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            # Get available transitions for the current state
            available_transitions = instance.get_available_workflow_state_transitions()
            limited_choices = [(t.target, t.target) for t in available_transitions]
            
            # Update the field's choices
            self.fields['workflow_state'] = forms.ChoiceField(choices=limited_choices)
            


# def __init__(self, *args, **kwargs):
#     self.user = kwargs.pop('user', None)
#     super(AddMovementForm, self).__init__(*args, **kwargs)
#     if not self.user.is_staff:
#         limited_choices = [(choice[0], choice[1]) for choice in STATUS_CHOICES if choice[0] == 8 or choice[0] == 20]
#         self.fields['status'] = forms.ChoiceField(choices=limited_choices)])

            
# def __init__(self, *args, **kwargs):
#     super(LendApproveForm, self).__init__(*args, **kwargs)
#     instance = kwargs.get('instance', None)
#     if instance:
#         # Get available transitions for the current state
#         available_transitions = instance.get_available_workflow_state_transitions()
        
#         # Update the field's choices
#         self.fields['workflow_state'].choices = [(t.target, t.target) for t in available_transitions]



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
        
        fields = ('category', 'title', 'description', 'value', 'image', 'location_name')
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
            'location_name': forms.TextInput(attrs=
                {
                'class': 'm-2 input input-bordered input-sm w-1/2 max-w-xs'
                }),
        }




# class LendRequestForm(forms.Form):
#     pickup_date = forms.DateField(widget=DateWidget)
#     return_date = forms.DateField(widget=DateWidget)
    
#     def __init__(self, *args, **kwargs):
#         super(LendRequestForm, self).__init__(*args, **kwargs)
#         self.fields['pickup_date'].label = "Pickup Date"
#         self.fields['return_date'].label = "Return Date"