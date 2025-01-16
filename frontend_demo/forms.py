from django import forms


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder':'Enter your comment','style':'width:100%','class':'form-control', 'data-rule':'required','data-msg':'Please write your comment'}
    ))
