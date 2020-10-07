from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
import markdown2
import difflib
from . import util
from django.core.files.storage import default_storage

class new_form(forms.Form):
    page_title= forms.CharField(label="Page Title:",widget=forms.TextInput(attrs={'class':'form-control col-md-8 col-lg-8'}))
    page_content= forms.CharField(widget=forms.Textarea(attrs={'class':'form-control col-md-8 col-lg-8', 'rows': 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title_search(request,title):
    randoms_list = [ t for t in util.list_entries()]
    random_title = random.choice(randoms_list)

    try:
        result = util.get_entry(title)
        entry = markdown2.markdown(result)
        return render(request, "encyclopedia/title.html", {
            "title":title.capitalize() , "content": result, "random": random_title,
            "entry":entry
        })
    
    except TypeError:
        return render(request, "encyclopedia/error.html")
    

def search(request):
    search_query = request.GET.get('q','')
    result_list=[]

    if (util.get_entry(search_query) is not None):
        return HttpResponseRedirect(reverse("title_search", kwargs={'title':search_query}))

    else:
        for i in util.list_entries():
            if search_query.lower() in i.lower():
                result_list.append(i)


        return render(request, "encyclopedia/search.html",{
            "entries":result_list,
            "value": search_query
        })


def new_page(request):

    if request.method == "POST":
        form = new_form(request.POST)

        if form.is_valid():
            
            page_title = form.cleaned_data["page_title"]
            page_content = form.cleaned_data["page_content"]

            if(util.get_entry(page_title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(page_title,page_content)

                return HttpResponseRedirect(reverse("title_search", kwargs={'title':page_title}))
            
            else:
                return render(request,"encyclopedia/newpage.html",{
                    "form": form,
                    "exist": True,
                    "entry": page_title
                })
        else:
            return render(request,"encyclopedia/newpage.html",{
                "form": form,
                "exist": False,
            })
    else:
        return render(request,"encyclopedia/newpage.html",{
            "form": new_form(),
            "new": True,
            "exist":False,
        })
def edit_display(request,title):

    if request.method== "POST":
        content= util.get_entry(title)

        form = new_form(initial={'page_title ':title, 'page_content':content})

        return render(request, "encyclopedia/newpage.html",{
            "EditFromDisplay": form,
            "edit": True,
            "title": title,
            "content":content

        })


def edit_submit(request, title):
    
    if request.method == "POST":
        form  = new_form(request.POST)

        if form.is_valid():
            edit_title = form.cleaned_data["page_title"]
            edit_content = form.cleaned_data["page_content"]   

            if edit_title != title:
                filename = f"entries/{title}.md"

                if default_storage.exists(filename):
                    default_storage.delete(filename)

            util.save_entry(edit_title,edit_content)

            new_entry = util.get_entry(edit_title)

            success_alert = "Edited Successfully!"

            return render(request, "encyclopedia/title.html",{
                "edit":True,
                "title": edit_title, 
                "entry":  markdown2.markdown(new_entry),
                "success_alert": success_alert
            })

def random_page(request):

    list_entries = util.list_entries()
    
    random_title = random.choice(list_entries)

    random_content = util.get_entry(random_title)

    return HttpResponseRedirect(reverse("title_search",args=[random_title]))

