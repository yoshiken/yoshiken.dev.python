from .converter import convert_articles, convert_unique_pages, cp_static, output_aricles_pages, convert_index_page, convert_feed
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

os.makedirs("docs", exist_ok=True)
env = Environment(
    loader=FileSystemLoader("template"),
    autoescape=select_autoescape()
)
unique_pages = ["about", "format"]
convert_unique_pages(env, unique_pages)
cp_static()
articles = convert_articles()
if articles:
    output_aricles_pages(env, articles)
convert_index_page(env, articles)
convert_feed(env, articles)
