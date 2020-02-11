import requests
from bs4 import BeautifulSoup

def main():
    # Purdue Police Department 'Daily Crime Log'
    page = requests.get('https://www.purdue.edu/ehps/police/assistance/stats/statsdaily.html')
    #print("result code: " + str(web_url.getcode()))
    #data = web_url.read()
    soup = BeautifulSoup(page.text, 'html.parser')
    soup_text = soup.find_all("p")

    raw_li = []
    for item in soup_text:
        i = item.prettify()
        raw_li.append(i.splitlines())
    
    li = []
    for item in raw_li:
        if len(item) == 7:
            handle_inconsistency(item)
        

def handle_inconsistency(li):
    # Likely incomprehenisble if doesn't include 'REPORTED'
    if 'REPORTED' in li[3]:
        # Remove HTML tags
        if '<p>' in li: li.remove('<p>')
        if '</p>' in li: li.remove('</p>')
        while ' <br/>' in li:
            li.remove(' <br/>')

        # Handle inconsistencies in ind: 0
        if 'CAD' in li[0]:
            li[0] = li[0].replace("CAD", "")
            li[0] = li[0].replace("#", "")
            li[0] = li[0].replace(" ", "")
            li[0] = li[0].replace("-", "")
        if 'CSA' in li[0]:
            li[0] = -1

        # Convert CAD# str to int
        li[0] = int(li[0])

        # Temporarily remove description
        descr = li[-1]
        li.pop(-1)

        # Handle inconsistencies in ind: 1
        li[1] = li[1].replace("REPORTED", "")
        li[1] = li[1].replace(" ", "")
        if 'DATE' in li[1]:
            li[1] = li[1].replace("DATE", "")

        x = li[1].split(",")
        li.pop(1)
        for i in x:
            li.append(i)

        if len(li) == 3:
            li.append(descr) # Add description back on
            li.append(li)
            print(li)

#def handle_description(li):

if __name__ == '__main__':
    main()