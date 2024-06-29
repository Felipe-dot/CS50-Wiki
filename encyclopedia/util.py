import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
    

def markdown_to_html(markdown_text):
    markdown_text = re.sub(r'^(#{1,6})\s*(.*)', lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>', markdown_text, flags=re.MULTILINE)

    markdown_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', markdown_text)

    markdown_text = re.sub(r'^[*-]\s+(.*)', r'<li>\1</li>', markdown_text, flags=re.MULTILINE)

    markdown_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', markdown_text)

    paragraphs = markdown_text.split('\n\n')
    html_paragraphs = []
    for para in paragraphs:
        if not re.match(r'^<.*>$', para.strip()):
            para = f'<p>{para}</p>'
        html_paragraphs.append(para)
    markdown_text = '\n\n'.join(html_paragraphs)

    markdown_text = re.sub(r'(<li>.*?</li>\n?)+', lambda m: f'<ul>{m.group(0)}</ul>', markdown_text, flags=re.DOTALL)

    markdown_text = re.sub(r'</li>\n<li>', '</li><li>', markdown_text)

    return markdown_text