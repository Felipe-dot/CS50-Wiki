import random
from django.shortcuts import render, redirect

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
    
    html_content = util.markdown_to_html(content)

    return render(request, "encyclopedia/content.html", {
        "title": title,
        "entry": html_content
    })

def create_new_page(request):
    if request.method == 'POST':
        title = request.POST.get('title').strip()
        content = request.POST.get('content').strip()

        if util.get_entry(title):
            return render(request, "encyclopedia/create_new_page.html", {
                "error": "An entry with this title already exists."
            })

        util.save_entry(title, content)
        return wiki(request,title)

    return render(request, "encyclopedia/create_new_page.html")


def edit_page(request, title):
    if request.method == "POST":
        new_content = request.POST.get('content')
        if new_content is not None:
            util.save_entry(title, new_content)
            return redirect('index')

    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })

def search(request):
    query = request.GET.get('q', '')
    if query:
        entries = util.list_entries()
        matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
        
        exact_match = None
        for entry in entries:
            if entry.lower() == query.lower():
                exact_match = entry
                break
        
        if exact_match:
            return redirect('wiki', title=exact_match)
        
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "entries": matching_entries
        })
    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "entries": []
    })

def random_page(request):
    entries = util.list_entries()
    if entries:
        random_entry = random.choice(entries)
        return redirect('wiki', title=random_entry)
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries available."
        })