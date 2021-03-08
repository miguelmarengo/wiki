import secrets

from django import forms
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.urls import reverse

from . import util
from .forms import NewEntryForm
from markdown2 import Markdown

marked = Markdown()


def edit(request, entry):
    entry_page = util.get_entry(entry)
    if entry_page is None:
        return render(request, 'encyclopedia/nonExistingEntry.html', {'entryTitle': entry})
    else:
        form = NewEntryForm()
        form.fields['title'].initial = entry
        form.fields['title'].widget = forms.HiddenInput()
        form.fields['content'].initial = entry_page
        form.fields["edit"].initial = True
        return render(request, 'encyclopedia/newEntry.html', {'form': form, 'edit': form.fields['edit'].initial,
                                                              'entryTitle': form.fields['title'].initial})


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, entry):
    markdowner = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/nonExistingEntry.html", {'entryTitle': entry})
    else:
        return render(request, "encyclopedia/entry.html",
                      {'entry': markdowner.convert(entryPage), 'entry_title': entry})


def newEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if (util.get_entry(title) is None) or (form.cleaned_data["edit"] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/newEntry.html", {'form': form, 'existing': True, 'entry': title})
        else:
            return render(request, 'encyclopedia/newEntry.html', {'form': form, 'existing': False})
    else:
        return render(request, 'encyclopedia/newEntry.html', {'form': NewEntryForm(), 'existing': False})


def random(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse('entry', kwargs={
        'entry': randomEntry
    }))


def search(request):
    value = request.GET.get('q', '')
    if util.get_entry(value) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value}))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)
        return render(request, 'encyclopedia/index.html', {'entries': subStringEntries, 'search': True, 'value': value})
