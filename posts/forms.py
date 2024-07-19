from tinymce.widgets import TinyMCE

from django import forms

from posts.models import Post

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={"rows": 80, "cols": 30}))
    
    class Meta:
        model = Post
        fields = "__all__"


class PostForm(forms.ModelForm):
    pass