from django import forms

class GuestBookingForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=50)
    last_name = forms.CharField(label='Фамилия', max_length=50)
    check_in_date = forms.DateField(label='Дата заезда', widget=forms.DateInput(attrs={'type': 'date'}))
    check_out_date = forms.DateField(label='Дата выезда', widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control' 