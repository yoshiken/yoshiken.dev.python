from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import markdown
import shutil
import glob
import re
from datetime import datetime


def convert_index_page(env, articles) -> None:
    template = env.get_template("index/base.j2")
    with open("docs/index.html", mode='w') as f:
        f.write(template.render({'articles': articles}))


def convert_unique_pages(env, unique_pages) -> None:
    for page in unique_pages:
        body = convert_pages("content/" + page + ".md")
        template = env.get_template("about/base.j2")
        with open("docs/" + page + ".html", mode='w') as f:
            f.write(template.render({'body': body}))


def cp_static() -> None:
    shutil.copytree("./template/static", "./docs", dirs_exist_ok=True)


def convert_articles() -> list:
    articles_list = glob.glob("./content/articles/*")
    articles = []
    for article in articles_list:
        articles.append(convert_pages(article))
    sorted_articles = sorted(articles, key=lambda x: x['date'], reverse=True)
    return sorted_articles


def convert_pages(path) -> dict:
    tmp_txt = ""
    body = {}
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("Title:"):
                body['title'] = re.sub('^Title: ', "", line).replace('\n', '')
                continue
            if line.startswith("Date:"):
                date_str = re.sub('^Date: ', "", line).replace('\n', '')
                body['date'] = datetime.strptime(date_str + '+09:00', '%Y-%m-%d %H:%M:%S%z')
                continue
            if line.startswith("Summary:"):
                body['summary'] = re.sub('^Summary: ', "", line).replace('\n', '')
                continue
            if line.startswith("Category:"):
                body['category'] = re.sub('^Category: ', "", line).replace('\n', '')
                continue
            tmp_txt += line
        body['text'] = md.convert(tmp_txt)
        body['output_file_name'] = os.path.splitext(os.path.basename(path))[0]
        body['link'] = "https://yoshiken.dev" "/articles/" + body['output_file_name']
    return body


def output_aricles_pages(env, articles) -> None:
    output_dir = "docs/articles/"
    os.makedirs(output_dir, exist_ok=True)
    template = env.get_template("articles/base.j2")
    for article in articles:
        with open(output_dir + article['output_file_name'] + ".html", mode='w') as f:
            f.write(template.render({'article': article}))


def convert_feed(env, articles) -> None:
    template = env.get_template("feed/base.j2")
    feed = {}
    feed['updated'] = articles[0]['date']
    with open("docs/feed.xml", mode='w') as f:
        f.write(template.render({'articles': articles, 'feed': feed}))


if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    md = markdown.Markdown(extensions=['extra', 'tables', 'fenced_code', 'abbr'])
    env = Environment(
        loader=FileSystemLoader("template"),
        autoescape=select_autoescape()
    )
    unique_pages = ["about", "format"]
    convert_unique_pages(env, unique_pages)
    cp_static()
    articles = convert_articles()
    output_aricles_pages(env, articles)
    convert_index_page(env, articles)
    convert_feed(env, articles)
