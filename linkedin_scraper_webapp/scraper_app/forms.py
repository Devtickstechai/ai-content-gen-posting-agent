from django import forms

class ScrapeForm(forms.Form):
    keyword = forms.CharField(label='Keyword', max_length=100)
    max_posts = forms.IntegerField(label='Max Posts')
    username = forms.CharField(label='LinkedIn Username', max_length=100)
    password = forms.CharField(label='LinkedIn Password', widget=forms.PasswordInput)
    post_category = forms.ChoiceField(
        label='Post Category',
        choices=[
            ('educational', 'Educational'),
            ('informative', 'Informative'),
            ('announcement', 'Announcement'),
            ('inspirational', 'Inspirational'),
        ],
        required=True
    )

