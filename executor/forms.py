from django import forms

class CodeExecutionForm(forms.Form):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('c', 'C'),
        ('cpp', 'C++'),
    ]

    code = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}))
    language = forms.ChoiceField(choices=[('python', 'Python'), ('c', 'C'), ('cpp', 'C++')])
    custom_input = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}), required=False, label='Custom Input')
