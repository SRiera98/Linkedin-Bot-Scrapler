from bs4 import BeautifulSoup
from urllib import request
import os

# Obtenemos el codigo HTML
def get_url(url):
    html = None
    try:
        html = request.urlopen(url).read()
    except:
        print("Nothing found!")
        os._exit(1)
    return html

def get_bs_object(url):
    source = get_url(url)
    return BeautifulSoup(source, "html.parser")


def get_total_jobs(beautiful) -> int:
    results_context = beautiful.find('span', {'class': 'results-context-header__job-count'}).text

    n_jobs = results_context.replace('+', '').replace(',', '').replace('.', '')
    return int(n_jobs)


def get_total_jobs_aux(search: str) -> int:
    bs = get_bs_object(
        f'https://ar.linkedin.com/jobs/search?keywords={search}&location=Argentina&trk=jobs_jserp_search_button_execute&orig=JSERP&&geoId=100446943'.replace(
            ' ', '%20'))
    results_context = bs.find('span', {'class': 'results-context-header__job-count'}).text

    n_jobs = results_context.replace('+', '').replace(',', '').replace('.', '')
    return int(n_jobs)


def get_total_jobs_per_page(beautiful) -> int:
    results = beautiful.find_all('li', {'class': 'result-card job-result-card result-card--with-hover-state'})
    return len(results)


def get_number_of_pages(n_jobs, n_postings) -> int:
    return int(round(n_jobs / float(n_postings)))


def get_urls(search: str) -> list:
    bs = get_bs_object(
        f'https://ar.linkedin.com/jobs/search?keywords={search}&location=Argentina&trk=jobs_jserp_search_button_execute&orig=JSERP&&geoId=100446943'.replace(
            ' ', '%20'))
    urls = []
    n_jobs = get_total_jobs(bs)
    n_jobs_per_page = get_total_jobs_per_page(bs)
    n_pages = get_number_of_pages(n_jobs, n_jobs_per_page)
    for i in range(n_pages):
        # define the base url for generic searching
        url = f"http://ar.linkedin.com/jobs/search?keywords={search}&location=Argentina&geoId=100446943&start=nPostings&count=25&trk=jobs_jserp_pagination_1".replace(' ', '%20')
        url = url.replace('nPostings', str(25 * i))
        urls.append(url)
    return urls
