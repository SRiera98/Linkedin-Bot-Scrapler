from bs4 import BeautifulSoup
from urllib import request

# Obtenemos el codigo HTML
def get_url(url):
    return request.urlopen(url).read()

# makes the source tree format like
def beautify(url):
    source = get_url(url)
    return BeautifulSoup(source,"html.parser")

def get_total_jobs(beautiful):
    results_context = beautiful.find('span', {'class': 'results-context-header__job-count'}).text

    n_jobs = results_context.replace('+', '').replace(',', '').replace('.', '')
    print(n_jobs)
    return int(n_jobs)

def get_total_jobs_per_page(beautiful):
    results = beautiful.find_all('li', {'class': 'result-card job-result-card result-card--with-hover-state'})
    return len(results)

def get_number_of_pages(n_jobs, n_postings):
    return int(round(n_jobs/float(n_postings)))

def get_urls(search: str)->list:
    bs = beautify(f'https://ar.linkedin.com/jobs/search?keywords={search}&location=Argentina&trk=jobs_jserp_search_button_execute&orig=JSERP&&geoId=100446943'.replace(' ','%20'))
    urls = []
    n_jobs = get_total_jobs(bs)
    n_jobs_per_page = get_total_jobs_per_page(bs)
    n_pages = get_number_of_pages(n_jobs, n_jobs_per_page)
    count = 1
    for i in range(n_pages):
        # define the base url for generic searching
        url = f"http://ar.linkedin.com/jobs/search?keywords={search}&location=Argentina&geoId=100446943&start=nPostings&count=25&trk=jobs_jserp_pagination_1".replace(' ','%20')
        url = url.replace('nPostings',str(25*i))
        count += 1
        urls.append(url)
        print(f"PROCESANDO URL N° {count}\n")
    return urls