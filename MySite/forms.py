from django import forms
from MySite.models import UserModel


class NameForm(forms.Form):
    user_name = forms.CharField(label='姓名', max_length=20)


class ContactForm(forms.Form):
    subject = forms.CharField(label='主题', label_suffix=':',widget=forms.TextInput(attrs={
        'style':'width:440px','maxlength':'100'}))
    message = forms.CharField(label='消息', label_suffix=':', widget=forms.Textarea(attrs={
        'cols':'60','rows':'10'}))
    sender = forms.EmailField(label='发送人', help_text='请输入正确的邮箱！', label_suffix=':')
    cc_myself = forms.BooleanField(label='是否抄送自己', label_suffix=':', required=False)


class FileMailForm(forms.Form):
    addresses = forms.CharField(label='收件地址', help_text='多个收件地址请使用逗号“,”分割', label_suffix=':',
                                widget=forms.TextInput(attrs={'style':'width:440px', 'maxlength': '100'}))
    subject = forms.CharField(label='邮件标题', label_suffix=':',widget=forms.TextInput(attrs={
        'style': 'width:440px',
        'maxlength': '100'
    }))
    message = forms.CharField(label='邮件内容', label_suffix=':', widget=forms.Textarea(attrs={
        'cols': '60',
        'rows': '10'
    }))
    file = forms.FileField(label='添加附件', label_suffix=':',required=False)
    cc_myself = forms.BooleanField(label='抄送自己', label_suffix='：', required=False)

class TextEmailForm(FileMailForm):
    file = None



class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = '__all__'
        widgets = {
            'password':forms.PasswordInput()
        }
        labels = {
            'name':'芳名'
        }
        help_texts = {
            'birthday':('日期格式为：2018-12-01')
        }
        error_messages = {
            'name':{'max_length':('名字太长！！')}
        }
        # fields = ['email','name','age','password','ip']
        exclude = ['birthday'] # 排除birthday字段
RegisterForm = forms.modelform_factory(UserModel,fields=('email','age','name'))
RegisterFormSet = forms.formset_factory(FileMailForm, extra=5)