from bs4 import BeautifulSoup
from urllib import request
import os

def get_url(url):
    """
    Obtenemos el html de la URL mediante la request
    :param url: Template a parsear
    :return: el string del temlate
    """
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
    """
    Nos permite encontrar cuantos trabajos hay como resultado para una búsqueda en particular.
    """
    results_context = beautiful.find('span', {'class': 'results-context-header__job-count'}).text

    n_jobs = results_context.replace('+', '').replace(',', '').replace('.', '')
    return int(n_jobs)


def get_total_jobs_aux(search: str, location_data: tuple) -> int:
    """
    Metodo auxiliar de get_total_jobs para usarlo en la Spider Class.
    """
    bs = get_bs_object(
        f'https://ar.linkedin.com/jobs/search?keywords={search}&location={location_data[0]}&trk=jobs_jserp_search_button_execute&orig=JSERP&&geoId={location_data[1]}'.replace(
            ' ', '%20'))
    results_context = bs.find('span', {'class': 'results-context-header__job-count'}).text

    n_jobs = results_context.replace('+', '').replace(',', '').replace('.', '')
    return int(n_jobs)


def get_total_jobs_per_page(beautiful) -> int:
    """Nos permite establecer cuantos resultados se muestran por página."""
    results = beautiful.find_all('li', {'class': 'result-card job-result-card result-card--with-hover-state'})
    return len(results)


def get_number_of_pages(n_jobs, n_postings) -> int:
    """Nos permite tener un estimativo de cuantas páginas se van a renderizar"""
    return int(round(n_jobs / float(n_postings)))


def get_urls(search: str, location_data: tuple) -> list:
    """Obtenemos una lista con todas las URL de los trabajos a scrapear"""
    bs = get_bs_object(
        f'https://ar.linkedin.com/jobs/search?keywords={search}&location={location_data[0]}&trk=jobs_jserp_search_button_execute&orig=JSERP&&geoId={location_data[1]}'.replace(
            ' ', '%20'))
    urls = []
    n_jobs = get_total_jobs(bs)
    n_jobs_per_page = get_total_jobs_per_page(bs)
    n_pages = get_number_of_pages(n_jobs, n_jobs_per_page)
    for i in range(n_pages):
        # Definimos la lista de URLs
        url = f"http://ar.linkedin.com/jobs/search?keywords={search}&location={location_data[0]}&geoId={location_data[1]}&start=nPostings&count=25&trk=jobs_jserp_pagination_1".replace(' ', '%20')
        url = url.replace('nPostings', str(25 * i))
        urls.append(url)
    return urls
