from django.shortcuts import render
import markdown2
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random

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

    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form,
                "new": True
            })

    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm(),
        "new": True
    })

def randompage(request):
    list = util.list_entries()
    new = random.choice(list)

    return HttpResponseRedirect(reverse("entry", kwargs={'entry': new}))

def edit(request, entry):
    content = util.get_entry(entry)
    initial_dict = {
        "title": entry,
        "content": content
    }
    editForm = NewPageForm(initial=initial_dict)

    return render(request, "encyclopedia/newpage.html", {
        "editForm": editForm
    })
