from tkinter import Entry
from django.shortcuts import render
import markdown
import html
from . import util
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random

def convert_md_to_html(title):
    # Assuming you have a function 'get_entry' that retrieves the content of the Markdown file
    content = util.get_entry(title)
    
    # Initialize the Markdown converter with extensions
    markdowner = markdown.Markdown(extensions=['extra', 'smarty'])

    if content is None:
        return None
    else:
        # Use html.escape() to properly handle special characters
        # This will escape special characters so they are displayed as-is in HTML
        escaped_content = html.escape(content)
        
        # Use the Markdown converter to convert the escaped content to HTML
        html_content = markdowner.convert(escaped_content)
        
        return html_content


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content is None:
        return render(request, "encyclopedia/error.html",{
            "message": "This entry is inexistent"
        }) #if the request don't exist show error page
    else: 
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)  # Fix the variable name here
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "entry": entry_search,  # Use the correct variable name here
                "content": html_content
            })
        else:
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
              "recommendation": recommendation
             })


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })
        
def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content

        })

def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        new_content = request.POST['content']
        util.save_entry(title, new_content)  # You need to replace 'content' with 'new_content'
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

import random  # Import the random module

# ...

def rand(request):
    allEntries = util.list_entries()
    # Choose a random entry from the list of all entries
    rand_entry = random.choice(allEntries)
    # Convert the content of the random entry to HTML
    html_content = convert_md_to_html(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "content": html_content
    })
