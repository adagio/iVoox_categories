from bs4 import BeautifulSoup

from modules.utils import Utils
from modules.storage import Storage



class Scraper:


    def __init__(self, url):
        self.url = url
        protocol = 'https'
        domain = 'www.ivoox.com'
        self.base_path = protocol + '://' +  domain


    def print_url(self):
        print(self.url)


    def __get_soup(self, text):
        soup = BeautifulSoup(text, features="lxml")
        return soup


    def __get_slug_and_id(self, url):
        # 'audios-' len = 7
        # '_1.html' len = 7
        url = url[7:-7]
        f_pos = url.find('f')
        id = url[f_pos+1:]
        underscore_pos = url.find('_')
        slug = url[0:underscore_pos]
        return slug, id


    def __get_subcategories_from_links(self, links, category_id):
        subcategories = []

        for link in links:
            name = link.getText().strip()
            url = link['href']
            slug, id = self.__get_slug_and_id(url)
            category = {
                'name': name,
                'url': url,
                'slug': slug,
                'id': id,
                'cat_id': category_id
            }
            subcategories.append(category)

        return subcategories


    def __get_categories_from_links(self, links):
        categories = []

        for link in links:
            name = link.getText().strip()
            url = link['href']
            slug, id = self.__get_slug_and_id(url)
            category = {
                'name': name,
                'url': url,
                'slug': slug,
                'id': id
            }
            categories.append(category)

        return categories


    def get_subcategories(self, category):

        print(category['name'])

        url = self.base_path + '/' + category['url']
        content = Utils().get_url_content(url)

        soup = self.__get_soup(content)

        pattern = 'body > div[id=main] div.fill_menu_filters div.child-menu-container div.container ul'
        subcategories_html_block = soup.select(pattern)[0]

        items = subcategories_html_block.select('li a')

        categories = self.__get_subcategories_from_links(items, category['id'])

        return categories


    def get_categories(self):

        #content = Utils().get_url_content(self.url)
        #Storage.save_pickle('storage/content.pkl', content)
        saved_content = Storage.load_pickle('storage/content.pkl')

        soup = self.__get_soup(saved_content)

        pattern = 'body > div[id=main] div.fill_menu_filters div.pills-container div.container ul'
        category_html_block = soup.select(pattern)[0]

        items = category_html_block.select('li a')

        categories = self.__get_categories_from_links(items)

        return categories