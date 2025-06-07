from os import listdir, mkdir, path

from block_mdparser import markdown_to_blocks
from md_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.strip("# ")
    raise ValueError("No Title found")


def generate_page(
    basepath: str, content_dir_path: str, template_path: str, dest_dir_path: str
):
    if path.exists(content_dir_path):
        content_dir_list = listdir(content_dir_path)
        for i in content_dir_list:
            new_path = path.join(content_dir_path, i)
            if path.isfile(new_path):
                markdown_file = open(new_path, "r", encoding=None)
                markdown = markdown_file.read()
                markdown_file.close()
                template_file = open(template_path, "r", encoding=None)
                template = template_file.read()
                template_file.close()
                html_path = path.join(dest_dir_path, i).replace(".md", ".html")
                html_file = open(html_path, "x", encoding=None)
                content = markdown_to_html_node(markdown).to_html()
                title = extract_title(markdown)
                html = (
                    template.replace("{{ Title }}", title)
                    .replace("{{ Content }}", content)
                    .replace("src=/", f"src={basepath}")
                    .replace("href=/", f"href={basepath}")
                )
                html_file.write(html)
                html_file.close()
            else:
                new_dest_path = path.join(dest_dir_path, f"{i}/")
                mkdir(new_dest_path)
                generate_page(basepath, new_path, template_path, new_dest_path)
