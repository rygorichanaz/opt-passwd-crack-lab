# Crack These Windows Hashes
## Instructions
These password hashes came from a Windows 10 workstation.  
The only thing we know is that the family that owns this computer are HUGE Green Bay Packers fans. 

Use a dictionary attack to crack these passwords.
```commandline
DAD:1000:AAD3B435B51404EEAAD3B435B51404EE:AF0D801A25A35988CF66A69E4472E7B0::
MOM:1001:AAD3B435B51404EEAAD3B435B51404EE:F8D5D26276FD2E5C0C700BBA0C49A308::
LITTLECHARLIE:1002:AAD3B435B51404EEAAD3B435B51404EE:2916DCD0452E91ACA26D3D1D8275D41F::
```

## My Solution
Huge GB Packers fans would definitely make their passwords their favorite players.

My first step was to build a wordlist of the names of every player for the Packers.  
To do this, I wrote the included Python script to scrape the table on the NFL website that contains the names (and stats) of every player on the Green Bay Packers.

```python
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
```
From here, I used the wordlist with `hashcat`.  
`.\hashcat.exe -m 1000 -a 0 windowshashes.txt packers.txt --force`

```commandline
> .\hashcat.exe -m 1000 -a 0 .\windowshashes.txt .\packers.txt --force
hashcat (v6.2.6) starting

...

Dictionary cache hit:
* Filename..: packers.txt
* Passwords.: 272
* Bytes.....: 3872
* Keyspace..: 272

...

af0d801a25a35988cf66a69e4472e7b0:Mason Crosby
f8d5d26276fd2e5c0c700bba0c49a308:Randall Cobb
2916dcd0452e91aca26d3d1d8275d41f:Aaron Rodgers

...

Started: Tue Apr 25 02:57:07 2023
Stopped: Tue Apr 25 02:57:09 2023
```
