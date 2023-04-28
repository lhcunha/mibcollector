import argparse
import csv
import re
import requests
from bs4 import BeautifulSoup
import os
import time

parser = argparse.ArgumentParser(description='Process a text file')
parser.add_argument('-f', '--file', type=str, help='Please, specify the input file')
args = parser.parse_args()

# creates the output file
with open('output.csv', 'w', newline='') as output_file:
    # creates the writer object to write in the output file
    writer = csv.writer(output_file)
    # writes the columns headers
    writer.writerow(['OID', 'OID Alias', 'MIB'])

    if args.file:
        # opens the input file
        with open(args.file, 'r') as f:
            count = 0
            for line in f:
                count = count + 1
                # removes whitespaces
                oid = line.strip()
                print(f'{count}: Processing the oid {oid}')
                while True:
                    try:
                        # queries the web address of the specific oid
                        response = requests.post(f'http://www.circitor.fr/Mibs/Search.php?string={oid}&how=1&where=2')
                        # parses the webpage's html
                        soup = BeautifulSoup(response.content, 'html.parser')
                        break
                    except requests.exceptions.RequestException as e:
                        print(f'Connection error: {e}')
                        print(f'Trying again in 5 seconds...')
                        time.sleep(5)  
                        continue  # Try the connection again
                # find all links in the html
                links = soup.find_all('a', href=re.compile(r'Html/'))
                if links:
                    link_for_mib = str(links[0])
                    match = re.match(r'<a href="Html/(.*).php">', link_for_mib)
                    if match:
                        link_for_mib_2 = match.group(1)
                    else:
                        print("Invalid Link for MIB.")
                else:
                    print("Couldn't process the OID.")
                    print("Registering on the output file...")
                    writer.writerow([oid, "NOT FOUND", "NOT FOUND"])

                    continue
                mib_name = link_for_mib_2[2:]   
                alias_raw = str(links[1])
                alias_parse = BeautifulSoup(alias_raw, 'html.parser')
                a_tag = alias_parse.find('a')
                alias = a_tag.string
                
                mib_url = f'https://circitor.fr/Mibs/Mib/{link_for_mib_2}.mib'

                while True:
                    try:
                        mib_page = requests.get(mib_url)
                        break
                    except requests.exceptions.RequestException as e:
                        print(f'Connection error: {e}')
                        print(f'Trying again in 5 seconds...')
                        time.sleep(5)  
                        continue  
                # verifies if the connection was succeeded
                if mib_page.status_code == 200:
                    # stores the page content in the variable
                    mib_page_content = mib_page.content
                    # saves the content in a mib file
                    with open(f'mib_files/{mib_name}.mib', 'wb') as mib_file:
                        mib_file.write(mib_page_content)
                else:
                    print(f'It wasnt possible to store the MIB {mib_name}')

                writer.writerow([oid, alias, mib_name])

                print(f'OID processed with success. Alias: {alias}, MIB name: {mib_name} ')
                    
    else:
        print('Input file not specified.')
