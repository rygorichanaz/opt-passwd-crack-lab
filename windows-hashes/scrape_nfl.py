import requests
from bs4 import BeautifulSoup


def scrape(webpage):
    r = requests.get(webpage)
    soup = BeautifulSoup(r.content, "html.parser")
    name_list = []
    
    # Find the roster table
    find_tbody = soup.find('tbody')
    # Names are located within 'a' tags
    tag = find_tbody.findNext('a')

    for i in find_tbody.findAllNext('a'):
        # If the <a> tag contents are blank, we've reached the end of the roster.
        if tag.contents[0] == ' ':
            print('\nFound all names...\nQuitting.')
            exit()

        # Take the contents of the <a> tag and save it to name
        name = str(tag.contents[0])
        # Add name variations to list
        name_list.append(name)  # name as provided
        name_list.append(name.replace(" ", ""))  # remove spaces between first and last
        name_list.append(name.lower())  # convert upper to lowercase
        name_list.append(name.replace(" ", "").lower())  # do both of the above

        # Print current tag to terminal       
        print(tag.contents[0])
        # Iterate to the next <a> tag
        tag = tag.findNext('a')

    # Write names to 'packers.txt' file
    with open('packers.txt', 'w') as packer_text:
        for player in name_list:
            packer_text.write(f'{player}')

            
if __name__ == "__main__":
    scrape('https://www.nfl.com/teams/green-bay-packers/roster')
