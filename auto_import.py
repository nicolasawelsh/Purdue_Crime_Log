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
    
    filtered_li = []
    for item in raw_li:
        if len(item) >= 4:
            if 'REPORTED' in item[3]:
                if '<p>' in item: item.remove('<p>')
                if '</p>' in item: item.remove('</p>')
                if ' <br/>' in item: item.remove(' <br/>')
                if ' <br/>' in item: item.remove(' <br/>')

                x = item[-1].split(".\xa0")
                item.pop(-1)
                for i in x:
                    item.append(i)
                if 'CAD' in item[0]:
                    item[0] = item[0].replace("CAD# ","")
                    item[0] = item[0].replace("-","")

                filtered_li.append(item)
                print(item)

if __name__ == '__main__':
    main()