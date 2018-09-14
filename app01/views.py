from django.shortcuts import render,HttpResponse
from app01 import models
# Create your views here.


def index2(request):
    error_message = {"user":"","pwd":""}
    if request.method =="POST":
        user = request.POST.get("user")
        pwd = request.POST.get('pwd')
        if len(pwd) < 6:
            error_message["pwd"] = "密码不能少于六位"
        if user == "":
            error_message['user'] = "用户名不能为空"

    return render(request,'index2.html', {"error_message":error_message})

from django import forms
from django.forms import widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    name = forms.CharField(
        #校验规则相关
        label="用户名",
        max_length=16,
        error_messages={
            "required": "用户名不能为空"

        },
        # 控制生成的HTML代码
        widget = widgets.TextInput(attrs={"class": "form-control"})
    )
    pwd = forms.CharField(
        label="密码",
        min_length=6,
        max_length=20,
        widget=widgets.PasswordInput(attrs={"class": "form-control"},render_value=True),
        error_messages={
            "min_length":"密码不能少于6位",
            "max_length": "密码不能大于20位",
            "required":"密码不能为空"

        }
    )
    re_pwd = forms.CharField(
        label="确认密码",
        min_length=6,
        max_length=20,
        widget=widgets.PasswordInput(attrs={"class": "form-control"},render_value=True),
        error_messages={
            "min_length": "密码不能少于6位",
            "max_length": "密码不能大于20位",
            "required": "密码不能为空"

        })

    email = forms.EmailField(
        label="邮箱",
        widget=widgets.EmailInput(attrs={"class":"form-control"}),
        error_messages={
            "required":"邮箱不能为空",
        }
    )
    phone = forms.CharField(
        label="手机",
        widget=widgets.TextInput(attrs={"class":"form-control"}),
        error_messages={
            "required":"手机不能为空",
        },
        validators=[
            RegexValidator(r'^[0-9]+$', '请输入数字'),
            RegexValidator(r'^1[3-9][0-9]{9}$', '请输入正确的手机格式')],
    )
    city = forms.ChoiceField(
        choices=models.City.objects.values_list('id','name'),#动态展示城市
        label="城市",
        widget=widgets.Select
    )

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["city"].widget.choices = models.City.objects.values_list('id','name')

    def clean_name(self):
        value = self.cleaned_data.get("name")

        if "金瓶梅" in value:
            raise ValidationError("不符合社会主义核心价值观")
        return value
        #重写父类的方法
    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd != re_pwd:
            self.add_error("re_pwd",ValidationError("密码不一致"))
            raise ValidationError("密码不一致")
        return self.cleaned_data

    # gender = forms.ChoiceField(
    #     choices=((1,"男"),(2,"女"),(3,"保密")),
    #     label="性别",
    #     initial="3",
    #     widget= forms.widgets.RadioSelect(attrs={"class":"list1"})
    #              )
    # hobby = forms.ChoiceField(
    #     choices=((1,"篮球"),(2,"足球"),(3,"皮球")),
    #     label="爱好",
    #     widget=widgets.Select
    #
    # )
    # hobby2 = forms.MultipleChoiceField(
    #     choices=((1, "篮球"), (2, "足球"), (3, "皮球")),
    #     label="多选select",
    #     initial=[1,3],
    #     widget=widgets.SelectMultiple
    #
    # )
    #
    # rember = forms.ChoiceField(
    #     label="是否记住密码",
    #     initial="checked",
    #     widget = widgets.CheckboxInput
    # )
    #
    # rember2 = forms.MultipleChoiceField(
    #     choices=((1, "篮球"), (2, "足球"), (3, "皮球")),
    #     label="多选check",
    #     initial=[1, 3],
    #     widget=widgets.CheckboxSelectMultiple(attrs={"class":"list1"})
    # )


def login(request):
    form_obj = LoginForm()
    print(form_obj.fields)
    print(form_obj.fields['name'])
    if request.method == "POST":
        form_obj = LoginForm(request.POST)
        print("===========")
        print(form_obj.is_valid())
        if form_obj.is_valid():
            # 校验通过，保持在form_obj.cleaner_data
            print(form_obj.cleaned_data)

            del form_obj.cleaned_data["re_pwd"] #删除数据库中不存在的值
            models.UserInfo.objects.create(**form_obj.cleaned_data)
            # 第二种方法获取username 和 pwd的值
            # username = form_obj.cleaned_data.get("username")
            # pwd = form_obj.cleaned_data.get("pwd")
            # user = models.UserInfo()
            # user.name = username
            # user.pwd = pwd
            # user.save()
            return HttpResponse("注册成功")
        print(form_obj.errors)
        print("***************")
        # print(form_obj.errors["__all__"])
        # print(form_obj.errors["__all__"][0])
    return render(request, "index.html", {"form_obj":form_obj})




