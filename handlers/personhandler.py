import datetime

import requests
from bs4 import BeautifulSoup


class PersonHandler(object):

    def __init__(
        self,
        page_locale: str
    ):
        self.page_locale = page_locale
        self.url_pattern = "https://pep.org.ua/{0}/person/{1}"

    def handle(
        self,
        person_id: str
    ) -> dict:
        # Fetch website response
        url = self.url_pattern.format(
            self.page_locale,
            person_id
        )
        url_response = requests.get(url)
        url_response_text = url_response.text
        # Parse website sections
        sections = self.handle_sections(url_response_text)
        # Return parsed data
        return sections

    def handle_sections(
        self,
        url_response_text: str
    ) -> dict:
        pass


class PersonHandlerUk(PersonHandler):

    def __init__(
        self
    ):
        page_locale = 'uk'
        super().__init__(page_locale)

    def handle_sections(
        self,
        url_response_text: str
    ) -> dict:
        # Define blank storage
        sections = {}
        # Initialize bs4 object
        soup = BeautifulSoup(
            markup=url_response_text,
            features='html.parser'
        )
        # Handle sections
        sections['header'] = self.handle_header_section(soup)
        sections['body'] = self.handle_body_section(soup)
        # Return parsed sections
        return sections

    def handle_header_section(
        self,
        soup: BeautifulSoup
    ) -> dict:
        storage = {}
        # Last profile change
        header_section = soup.find(class_='profile-page__header')
        time_value = header_section.find(class_='date').find('time').text
        storage['last_modified'] = time_value
        # Return storage
        return storage

    def handle_body_section(
        self,
        soup: BeautifulSoup
    ) -> dict:
        storage = {}
        # Identify section
        body_section = soup.find(class_='profile-page__body')
        # Top section
        storage['top'] = self.handle_top_section(body_section)
        # Scoring section
        storage['scoring'] = self.handle_scoring_section(body_section)
        # Blocks section
        storage['blocks'] = self.handle_blocks_section(body_section)
        # Names section
        storage['names'] = self.handle_names_section(body_section)
        # Return storage
        return storage

    def handle_top_section(
        self,
        body_section
    ) -> dict:
        storage = {}
        # Identify section
        top_section = body_section.find(class_='profile-page__top')
        # Profile image
        storage['profile_image_src'] = top_section.find(class_='profile-image').find('img')['src']
        # Profile name
        storage['profile_name'] = top_section.find(class_='profile-main-info').find('h1').text
        # Other fields table
        for tr_obj in top_section.find('table').findAll('tr'):
            td_objs = tr_obj.findAll('td')
            if td_objs[0].text == 'Категорія':
                storage['category'] = td_objs[1].text
            if td_objs[0].text == 'Остання посада':
                storage['last_position_job_link'] = td_objs[1].find('a')['href']
                storage['last_position_job_name'] = td_objs[1].find('a').find('span').text
                storage['last_position_job_title'] = td_objs[1].findAll('span')[1].text
            if td_objs[0].text == 'Дата народження':
                storage['birth_date__time'] = td_objs[1].find('time').text
                storage['birth_date__meta_content'] = td_objs[1].find('meta')['content']
            if td_objs[0].text == 'Дата звільнення':
                storage['dismissal_date'] = td_objs[1].find('time').text
        # Return storage
        return storage

    def handle_scoring_section(
        self,
        body_section
    ) -> dict:
        storage = {}
        # Scoring section
        scoring_section = body_section.find(class_='scoring')
        # Score
        storage['scoring_score'] = scoring_section.find(class_='scoring__header').find(class_='progressbar').find('span').text
        # Scoring factors
        li_objs = scoring_section.find(class_='scoring__list')
        storage['scoring_factors'] = [
            li_obj.find('p')
            for li_obj in li_objs.findAll('li')
        ]
        # Return storage
        return storage

    def handle_blocks_section(
        self,
        body_section
    ) -> dict:
        storage = {}
        # Blocks section

        # todo: column-left
        # todo: column-right

        # Return storage
        return storage

    def handle_names_section(
        self,
        body_section
    ) -> dict:
        storage = {}
        # Identify section
        names_section = body_section.find(class_='names-section')
        # Alternative names
        p_objects = names_section.find(class_='names-grid').findAll('p')
        storage['alternative_names'] = [
            p_object.text
            for p_object in p_objects
        ]
        # Return storage
        return storage


phu = PersonHandlerUk()
print(
    phu.handle(1)
)

