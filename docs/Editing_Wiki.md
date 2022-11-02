# Guide on Editing the Wiki Page

---

## Setting up Environment

Install the programs listed below:

- [Python](https://www.python.org/downloads/)
    - MAKE SURE TO SELECT "ADD PYTHON TO PATH" 
- [VS Code](https://code.visualstudio.com/Download)

Installing mkdocs and the material theme for mkdocs
```
    pip install mkdocs
    pip install mkdocs-material
```

Clone the Wiki Repo

```
    git clone {WIKI_LINK}
```

Compile the Site by running: 

```
    mkdocs serve
```

If everything is setup correctly, a local website should be created <a href="http://127.0.0.1:8000/Automated-Learning-Assistant/" target="_blank">here</a>.

## Writing Docs

Mkdocs is written in a language called Markdown (.md)
To access a Markdown Cheat Sheet, click <a href="https://www.markdownguide.org/cheat-sheet/" target="_blank">here</a>.

To create a new page, create a new .md file. Then, open up mkdocs.yml and add the page to the nav section, where needed.
 
Adding a new page: 
```
    nav:
        - 'New Page': new_page.md'
```

Adding a new page under a tab: 
```
    nav:
        - 'Tab': 
            - 'New Page': new_page.md'
```

If the page is not added to the nav, it will not show up on the site. 

## Pushing the Docs 

No special actions have to be taken when pushing the docs. 
Make sure to push to the main branch, and from there, Github Workflows will compile and put the website up. 