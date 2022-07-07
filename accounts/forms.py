from django import forms
from .models import Users
from django.contrib.auth.hashers import make_password, check_password


class LoginForm(forms.Form):
    userid = forms.CharField(error_messages={
        'required': '아이디를 입력하세요'}, max_length=30, label="사용자 ID")
    password = forms.CharField(error_messages={
        'required': '비밀번호를 입력하세요'}, widget=forms.PasswordInput, max_length=15, label="비밀번호")

    # 이미 수행되고 있는 값을 clean 하는 메소드
    def clean(self):
        clean_data = super().clean()
        userid = clean_data.get("userid")
        password = clean_data.get("password")
        if userid and password:
            try:
                member = Users.objects.get(userid=userid)
            except Users.DoesNotExist:
                self.add_error('userid', '아이디가 존재하지 않습니다.')
                return
            if not check_password(password, member.password):
                self.add_error('password', '비밀번호가 다릅니다.')
            else:
                self.userid = member.userid



