import requests
import re
from bs4 import BeautifulSoup
import sqlite3
import time
import urllib3
import ssl


class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session


def fetch_and_parse(url):
    response = get_legacy_session().get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Make a dictionary to store the data
    data = {}
    # Extract the title
    data['title'] = soup.title.text
    # Extract Course Code and Name
    # Extract Course Code and Name
    data['course_code'] = soup.find('th', text='Course Code').find_next_sibling('td').text if soup.find('th', text='Course Code') else None
    data['course_name'] = soup.find('th', text='Course').find_next_sibling('td').text if soup.find('th', text='Course') else None
    data['term'] = soup.find('th', text='Term').find_next_sibling('td').text if soup.find('th', text='Term') else None
    data['level'] = soup.find('th', text='Level').find_next_sibling('td').text if soup.find('th', text='Level') else None
    data['location'] = soup.find('th', text='Location/s').find_next_sibling('td').text if soup.find('th', text='Location/s') else None
    data['units'] = soup.find('th', text='Units').find_next_sibling('td').text if soup.find('th', text='Units') else None
    data['contact'] = soup.find('th', text='Contact').find_next_sibling('td').text if soup.find('th', text='Contact') else None
    data['course_description'] = soup.find('th', text='Course Description').find_next_sibling('td').text if soup.find('th', text='Course Description') else None
    data['prerequisites'] = soup.find('th', text='Prerequisites').find_next_sibling('td').text if soup.find('th', text='Prerequisites') else None
    data['incompatible'] = soup.find('th', text='Incompatible').find_next_sibling('td').text if soup.find('th', text='Incompatible') else None
    data['issumed_knowledge'] = soup.find('th', text='Assumed Knowledge').find_next_sibling('td').text if soup.find('th', text='Assumed Knowledge') else None


    return data


def fetch_and_parse_links(url):
    response = get_legacy_session().get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    extracted_links = [link['href'] for link in links if 'href' in link.attrs]
    print('Found ' + str(len(extracted_links)) + ' links.')
    return extracted_links

def filter_links(links):
    # Updated pattern to exclude links with a year at the end
    pattern = re.compile(r'/course-outlines/\d+/\d+/sem-\d+/$')
    return [r'http://www.adelaide.edu.au' + link for link in links if pattern.match(link)]

# URLs to scrape
urls_to_scrape = [
    'http://www.adelaide.edu.au/course-outlines/ug/',
    'http://www.adelaide.edu.au/course-outlines/pgcw/'
]

# SQLite database connection
conn = sqlite3.connect('university_courses.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    course_code TEXT,
    course_name TEXT,
    level TEXT,
    term TEXT,
    location TEXT,
    units TEXT,
    contact TEXT,
    course_description TEXT,
    prerequisites TEXT,
    incompatible TEXT,
    assumed_knowledge TEXT
)
""")

all_links = []
for url in urls_to_scrape:
    print('Scraping URL: ' + url)
    links = fetch_and_parse_links(url)
    all_links.extend(links)
# print(all_links[:100])
filtered_links = filter_links(all_links)
print('Found ' + str(len(filtered_links)) + ' links to scrape.')



for url in filtered_links[:]:
    data = fetch_and_parse(url)  # Define this function to parse course details
    # Insert data into database
    # Example: cursor.execute("INSERT INTO courses (title) VALUES (?)", (data['title'],))
    # conn.commit()
    cursor.execute("INSERT INTO courses (title, course_code, course_name, term, level, location, units, contact, course_description, prerequisites, incompatible, assumed_knowledge) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
               (data.get('title', None), 
                data.get('course_code', None), 
                data.get('course_name', None), 
                data.get('term', None), 
                data.get('level', None),
                data.get('location', None), 
                data.get('units', None), 
                data.get('contact', None), 
                data.get('course_description', None), 
                data.get('prerequisites', None), 
                data.get('Incompatible', None), 
                data.get('assumed_knowledge', None)))    
    conn.commit()

    # print(data)
    print('Scraped URL: ' + url)
    # time.sleep(2)

conn.close()
