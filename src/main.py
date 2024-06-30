import os
from utils import copy_directory
from to_html import generate_pages_recursive


def main():
    script_dir = os.path.dirname(__file__)
    src = os.path.join(script_dir, '..', 'static/')
    dst = os.path.join(script_dir, '..', 'public/')
    copy_directory(src, dst)

    src_index = os.path.join(script_dir, '../content/')
    src_template = os.path.join(script_dir, '../template.html')
    page_dest = os.path.join(script_dir, '../public/')

    generate_pages_recursive(src_index, src_template, page_dest)




if __name__ == "__main__":
    main()
