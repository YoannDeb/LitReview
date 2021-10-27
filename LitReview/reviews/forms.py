from django import forms


RATINGS = [('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)]


class TicketResponseForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    headline = forms.CharField(label='Titre', max_length=128, widget=forms.TextInput(attrs={'size': '60'}))
    rating = forms.ChoiceField(label='Note', widget=forms.RadioSelect, choices=RATINGS)
    body = forms.CharField(label='Commentaire', max_length=8192, required=False, widget=forms.Textarea(attrs={'rows': '10', 'cols': '60'}))


class TicketCreationForm(forms.Form):
    pass


class ReviewCreationForm(forms.Form):
    pass
