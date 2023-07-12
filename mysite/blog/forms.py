from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    #for create form from model, must be specified in Meta class, 
    # model for which to build form
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']