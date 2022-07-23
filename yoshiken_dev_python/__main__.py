from .converter import convert_articles, convert_unique_pages, cp_static, output_aricles_pages, convert_index_page, convert_feed
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='input content dir', type=str, default='./content')
parser.add_argument('--output', help='output dir', type=str, default='./docs')
parser.add_argument('--template', help='template dir', type=str, default='./template')
args = parser.parse_args()

os.makedirs(args.output, exist_ok=True)
env = Environment(
    loader=FileSystemLoader("template"),
    autoescape=select_autoescape()
)
unique_pages = ["about", "format"]
convert_unique_pages(env, args, unique_pages)
cp_static(args)
articles = convert_articles(args)
if articles:
    output_aricles_pages(env, args, articles)
convert_index_page(env, args, articles)
convert_feed(env, args, articles)
