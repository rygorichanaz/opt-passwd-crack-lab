big_list = []

with open('book.txt', 'r') as booklist:
    for book in booklist:
        big_list.append(book.lower())
        big_list.append(book.replace(' ', '').lower())

with open('book2.txt', 'w') as bookage:
    for book in big_list:
        bookage.write(f'{book}')
