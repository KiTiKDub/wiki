from django.shortcuts import render
import markdown2
from django import forms

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Page Content", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):

    content = markdown2.markdown(util.get_entry(entry))

    return render(request, "encyclopedia/entries.html", {
        "content": content,
        "title": entry
    })


def newpage(request):
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })
