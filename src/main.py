from markdown_blocks import markdown_to_html_node
from textnode import TextNode, TextType
from pathlib import Path
import shutil
import sys
import os

def copy_files(source, destination):
    # Check destination exists
    if os.path.exists(destination):
        # Remove contents
        shutil.rmtree(destination)

    # Create the destination
    os.makedirs(destination)

    # Copy contents from source to destination
    entries = os.listdir(source)
    for entry in entries:
        source_path = os.path.join(source, entry)
        dest_path = os.path.join(destination, entry)

        if os.path.isdir(source_path):
            copy_files(source_path, dest_path)
        else:
            print(f"Copying {source_path} to {dest_path}")
            shutil.copy(source_path, dest_path)

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.lstrip().startswith("# "):
            text = line.lstrip()[2:].strip()
            return text
    raise Exception("No header in file")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as from_file:
        from_content = from_file.read()
    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    html_string = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)

    final_template = (
        template_content.replace("{{ Title }}", title)
        .replace("{{ Content }}", html_string)
        .replace('href="/', 'href="{basepath}')
        .replace('src="/', 'src="{basepath}')
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as write_file:
        write_file.write(final_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # Get all entries in the current directory
    entries = os.listdir(dir_path_content)
    
    for entry in entries:
        source_path = os.path.join(dir_path_content, entry)
        
        # Calculate the relative path from content directory
        rel_path = os.path.relpath(source_path, dir_path_content)
        # Create corresponding path in destination
        dest_path = os.path.join(dest_dir_path, rel_path)
        
        if os.path.isfile(source_path) and source_path.endswith('.md'):
            # Change extension from .md to .html
            dest_html_path = os.path.splitext(dest_path)[0] + '.html'
            # Generate the HTML page
            generate_page(source_path, template_path, dest_html_path, basepath)
        elif os.path.isdir(source_path):
            # Ensure the directory exists in destination
            os.makedirs(dest_path, exist_ok=True)
            # Recursively process this subdirectory
            generate_pages_recursive(source_path, template_path, dest_path, basepath)


def main():
    source = "/Users/rob/Dev/Boot.dev/static-site/static"
    destination = "/Users/rob/Dev/Boot.dev/static-site/docs"
    dir_path_content = "/Users/rob/Dev/Boot.dev/static-site/content"
    template_path = "/Users/rob/Dev/Boot.dev/static-site/template.html"
    dest_dir_path = "/Users/rob/Dev/Boot.dev/static-site/docs"
    basepath = sys.argv[1] if len(sys.argv) >= 2 else "/"
    
    copy_files(source, destination)
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath)

if __name__ == "__main__":
    main()
