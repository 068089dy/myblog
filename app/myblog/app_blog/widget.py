from django.forms import TextInput


class MyTextInput(TextInput):
    class Media:
        # 为了防止admin表单未保存就干部页面，所以使用save.js
        js = ("js/save.js",)
