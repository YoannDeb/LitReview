from django import forms


RATINGS = [('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)]


class TicketResponseForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    headline = forms.CharField(label='Titre', max_length=128, widget=forms.TextInput(attrs={'size': '60'}))
    rating = forms.ChoiceField(label='Note', widget=forms.RadioSelect, choices=RATINGS)
    body = forms.CharField(label='Commentaire', max_length=8192, required=False, widget=forms.Textarea(attrs={'rows': '10', 'cols': '60'}))


class TicketCreationForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    title = forms.CharField(label='Titre', max_length=128, widget=forms.TextInput(attrs={'size': '60'}))
    description = forms.CharField(label='Description', max_length=2048, required=False, widget=forms.Textarea(attrs={'rows': '10', 'cols': '60'}))
    image = forms.ImageField(label='Image', required=False)


class ReviewCreationForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    title = forms.CharField(label='Titre', max_length=128, widget=forms.TextInput(attrs={'size': '60'}))
    description = forms.CharField(label='Description', max_length=2048, required=False, widget=forms.Textarea(attrs={'rows': '10', 'cols': '60'}))
    image = forms.ImageField(label='Image', required=False)
    headline = forms.CharField(label='Titre', max_length=128, widget=forms.TextInput(attrs={'size': '60'}))
    rating = forms.ChoiceField(label='Note', widget=forms.RadioSelect, choices=RATINGS)
    body = forms.CharField(label='Commentaire', max_length=8192, required=False,
                           widget=forms.Textarea(attrs={'rows': '10', 'cols': '60'}))


class UserSearchForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    username_searched = forms.CharField(label='', max_length=150, widget=forms.TextInput(attrs={'size': '60'}))
