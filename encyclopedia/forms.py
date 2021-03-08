from django import forms


class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class': 'my_text_input', 'placeholder': 'Search'}))


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title",
                            widget=forms.TextInput(attrs={'class': 'form-control col-md-6 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-6 col-lg-8', 'rows': 8}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)
