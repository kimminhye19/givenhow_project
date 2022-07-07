from django import forms
from .models import Survey


class TripForm(forms.ModelForm):
    def __init(self, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': True
        })

    class Meta:
        model = Survey
        fields = ['id']





