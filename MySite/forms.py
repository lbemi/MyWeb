from django import forms


class NameForm(forms.Form):
    user_name = forms.CharField(label='姓名', max_length=20)