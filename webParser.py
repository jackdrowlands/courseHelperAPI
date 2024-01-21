import requests  # Used for HTTP requests
import re  # Regular expression library for pattern matching
from bs4 import BeautifulSoup  # Parsing HTML/XML documents
import sqlite3  # SQLite database library
import time  # Time access and conversions
import urllib3  # HTTP client for Python
import ssl  # SSL/TLS library for secure connections

# Custom HTTP Adapter Class
class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    """
    A custom transport adapter for Requests. 
    This allows for custom SSL context to be used with the requests library.
    """
    def __init__(self, ssl_context=None, **kwargs):
        """
        Initialize the adapter with an optional SSL context.
        """
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        """
        Initializes the pool manager with the specified SSL context.
        """
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)

# Session Creation for Legacy Support
def get_legacy_session():
    """
    Creates and returns a requests session with legacy server connect options.
    """
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session

# Fetch and Parse HTML Content
def fetch_and_parse(url):
    """
    Fetches the webpage at the given URL and parses it using BeautifulSoup.
    Extracts various course details and returns them in a dictionary.
    """
    response = get_legacy_session().get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extracting various course details
    data = {
        'title': soup.title.text if soup.title else None,
        # Similar pattern repeated for other course details
        # ...
    }

    return data

# Fetch and Parse Links from a Page
def fetch_and_parse_links(url):
    """
    Fetches the webpage at the given URL and extracts all hyperlinks.
    Returns a list of extracted links.
    """
    response = get_legacy_session().get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    extracted_links = [link['href'] for link in links if 'href' in link.attrs]
    print('Found ' + str(len(extracted_links)) + ' links.')
    return extracted_links

# Filter Relevant Links
def filter_links(links):
    """
    Filters the provided list of links based on a predefined pattern.
    Returns a list of filtered links.
    """
    # Regular expression pattern for filtering course outline links
    pattern = re.compile(r'/course-outlines/\d+/\d+/sem-\d+/$')
    return [r'http://www.adelaide.edu.au' + link for link in links if pattern.match(link)]

# Main Script Execution
# URLs to scrape
urls_to_scrape = [
    'http://www.adelaide.edu.au/course-outlines/ug/',
    'http://www.adelaide.edu.au/course-outlines/pgcw/'
]

# Establish SQLite Database Connection
conn = sqlite3.connect('university_courses.db')
cursor = conn.cursor()
# Create table for storing course data
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

# Scrape and Store Course Data
all_links = []
for url in urls_to_scrape:
    print('Scraping URL: ' + url)
    links = fetch_and_parse_links(url)
    all_links.extend(links)

filtered_links = filter_links(all_links)
print('Found ' + str(len(filtered_links)) + ' links to scrape.')

for url in filtered_links[:]:
    data = fetch_and_parse(url)
    # Inserting scraped data into the database
    cursor.execute("INSERT INTO courses (...) VALUES (...)", 
                   (data.get('title', None), ...))
    conn.commit()
    print('Scraped URL: ' + url)

# Close the database connection
conn.close()
