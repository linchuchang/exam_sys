from django import forms

class UserForm(forms.Form):
    email = forms.CharField(label="邮箱", max_length=128, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class Register_Student_Form(forms.Form):
    SEX = (('male', '男'), ('female', '女'))
    GRADE = (('one', '大一'), ('two', '大二'), ('three', '大三'), ('four', '大四'))

    student_number = forms.CharField(label="学号", max_length=8, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱", max_length=128, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    grade = forms.ChoiceField(label="年级", choices=GRADE)
    sex = forms.ChoiceField(label="性别", choices=SEX)
    name = forms.CharField(label="姓名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    major = forms.CharField(label="专业名称", max_length=128, widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class Register_Teacher_Form(forms.Form):
    SEX = (('male', '男'), ('female', '女'))
    GRADE = (('one', '大一'), ('two', '大二'), ('three', '大三'), ('four', '大四'))

    Teacher_number = forms.CharField(label="教工号", max_length=8, widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label="姓名", max_length=32, widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(label="邮箱", max_length=128, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label="性别", choices=SEX)
    password1 = forms.CharField(label="密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


