import gzip
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup

def extract_login_pages(warc_file_path, output_file_path):
    login_pages = []
    count = 0
    # Open the WARC file
    with open(warc_file_path, 'rb') as stream:
        for record in ArchiveIterator(stream):
            try:
                if record.rec_type == 'response':
                    # Get the URL of the page
                    url = record.rec_headers.get_header('WARC-Target-URI')
                    
                    # Extract the content and check if it's gzipped
                    html = record.content_stream().read()
                    
                    # Try decompressing the content
                    try:
                        html = gzip.decompress(html).decode('utf-8', errors='ignore')
                    except OSError:
                        # If not gzipped, decode directly
                        html = html.decode('utf-8', errors='ignore')

                    # Parse the HTML content
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Search for forms with common login indicators
                    forms = soup.find_all('form')
                    for form in forms:
                        if form.find('input', {'type': 'password'}):
                            print("found")
                            login_pages.append(url)
                            count += 1
                            break
                # Increment the counter
                if count >= 10000:
                    break  # Stop processing after 10,000 entries
            except Exception as e:
                # Log the error or print it if needed and continue
                print(f"Error processing record: {e}")
                continue
                
    # Write the URLs to the output file
    with open(output_file_path, 'w') as output_file:
        for url in login_pages:
            output_file.write(url + '\n')

# Example usage
warc_file_path = 'PATH'
output_file_path = 'login_pages.txt'
extract_login_pages(warc_file_path, output_file_path)

print(f"URLs of login pages have been written to {output_file_path}")
