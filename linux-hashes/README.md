# Crack The Linux Hash

The following hash was extracted from a Linux shadow file.
The password hint was:
>My favorite book from a best-selling children's author

The password policy did not allow uppercase or special characters.
See if you can crack this password.

`eaffabee:$6$uuG1IpIXAidxAXS6$bauftZLlSOUaKw3zgBitEkmhVJTN3QYKMx4BUnJbk.V82AaUaL9uXS7lOYkrhV/oMPpJ8WksInj9F5UxaMGzb1:17645:0:99999:7:::`

## My Solution
The username (`eaffabee`) relates to Eric Affabee, a pseudonym for author R. L. Stine.  
I found a list of his works on [Wikipedia](https://en.wikipedia.org/wiki/R._L._Stine) and the [R. L. Stine Wiki](https://stine.fandom.com/wiki/List_of_R.L._Stine_Books).  
From the list on the R. L. Stine Wiki, I copied everything into Notepad. Could have built a script to scrape it for me, but this was quick enough.  

Because the password policy is stated to not allow uppercase or special characters, I then needed to make all uppercase letters lowercase and remove all spaces.

To do this, I used the provided script:
```python
big_list = []

with open('book.txt', 'r') as booklist:
    for book in booklist:
        big_list.append(book.lower())
        big_list.append(book.replace(' ', '').lower())

with open('book2.txt', 'w') as bookage:
    for book in big_list:
        bookage.write(f'{book}')
```
It's a simple and dirty script for building this specific wordlist, so it's lazily formatted.

This wordlist was then used with hashcat to crack the hash in a dictionary attack.  
`.\hashcat.exe -m 1800 -a 0 --force .\linuxhash.txt .\books.txt`

Running `hashcat` provided the following output:
```commandline
> .\hashcat.exe -m 1800 -a 0 --force .\linuxhash.txt .\books.txt
hashcat (v6.2.6) starting

...

Dictionary cache built:
* Filename..: .\books.txt
* Passwords.: 2141
* Bytes.....: 43939
* Keyspace..: 2141
* Runtime...: 0 secs

...

$6$uuG1IpIXAidxAXS6$bauftZLlSOUaKw3zgBitEkmhVJTN3QYKMx4BUnJbk.V82AaUaL9uXS7lOYkrhV/oMPpJ8WksInj9F5UxaMGzb1:whyiquitzombieschool

...

Started: Tue Apr 25 03:22:10 2023
Stopped: Tue Apr 25 03:22:21 2023
```

Searching my final wordlist, it looks like there is some scrambled text, but I got lucky that the correct password remained intact!

`$6$uuG1IpIXAidxAXS6$bauftZLlSOUaKw3zgBitEkmhVJTN3QYKMx4BUnJbk.V82AaUaL9uXS7lOYkrhV/oMPpJ8WksInj9F5UxaMGzb1:whyiquitzombieschool`
