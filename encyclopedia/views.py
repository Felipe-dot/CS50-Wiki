import markdown2
from django.http import HttpResponse
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request,title):
    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/error.html", {
             "message": "The requested page was not found."
        })
    
    html_content = markdown2.markdown(content)

    return render(request, "encyclopedia/content.html", {
        "title": title,
        "entry": html_content
    })

def createNewPage(request):
    if request.method == 'POST':
        title = request.POST.get('title').strip()
        content = request.POST.get('content').strip()

        if util.get_entry(title):
            return render(request, "encyclopedia/createNewPage.html", {
                "error": "An entry with this title already exists."
            })

        util.save_entry(title, content)
        return wiki(request,title)

    return render(request, "encyclopedia/createNewPage.html")