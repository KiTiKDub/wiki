from django.shortcuts import render
import markdown2
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
from django.http import HttpResponse

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Page Content", widget=forms.Textarea)


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):

    page = util.get_entry(entry)

    if page is None:
        return render(request, "encyclopedia/error.html", {
            "url_request": True
        })
    else:
        content = markdown2.markdown(page)

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

            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/error.html", {
                    "title": title
                })

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

    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))
        else:
            return render(request, "encyclopedia/edit.html", {
                "editForm": form,
                "title": entry
            })

    content = util.get_entry(entry)
    initial_dict = {
        "title": entry,
        "content": content
    }
    editForm = NewPageForm(initial=initial_dict)

    return render(request, "encyclopedia/edit.html", {
        "editForm": editForm,
        "title": entry
    })


def search(request):

    dict = request.GET
    query = dict.get("q")
    content = None
    if query is not None:

        content = util.get_entry(query)

        if content == None:
            search = util.list_entries()

            filtered_list = list(filter(lambda x: all(
                substring in x.lower() for substring in query), search))

            return render(request, "encyclopedia/search.html", {
                "entries": filtered_list,
                "query": query
            })
        else:
            content = markdown2.markdown(content)
            return render(request, "encyclopedia/entries.html", {
                "content": content,
                "title": query
            })
