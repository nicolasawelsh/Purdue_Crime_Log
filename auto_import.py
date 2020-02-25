import requests
import csv
from bs4 import BeautifulSoup


def main():
    # Purdue Police Department 'Daily Crime Log'
    page = requests.get('https://www.purdue.edu/ehps/police/assistance/stats/statsdaily.html')
    soup = BeautifulSoup(page.text, 'html.parser')
    soup_text = soup.find_all("p")

    raw_li = []
    for item in soup_text:
        i = item.prettify()
        raw_li.append(i.splitlines())
    
    li = []
    li = handle_filtering(li, raw_li)
    li.sort(key=lambda x: x[0])
    #for elem in li:
        #print(elem)
    with open("out.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(li)


def handle_filtering(li, raw_li):
    for item in raw_li:
        if len(item) == 7:
            if 'REPORTED' in item[3]:
                # Remove HTML tags
                if '<p>' in item: item.remove('<p>')
                if '</p>' in item: item.remove('</p>')
                while ' <br/>' in item:
                    item.remove(' <br/>')

                # Handle inconsistencies in ind: 0 (will need updated with time)
                if 'WLPD' in item[0]:
                    item[0] = item[0].replace("WLPD", "")
                    item[0] = item[0].replace(" ", "")
                if 'CAD' in item[0]:
                    item[0] = item[0].replace("CAD", "")
                    item[0] = item[0].replace("#", "")
                    item[0] = item[0].replace(" ", "")
                    item[0] = item[0].replace("-", "")
                if 'CSA' in item[0]:
                    item[0] = -1

                # Convert CAD# str to int
                item[0] = int(item[0])
                desc = item[-1]
                item.pop(-1)

                # Handle inconsistencies in ind: 1
                item[1] = item[1].replace("REPORTED", "")
                item[1] = item[1].replace(" ", "")
                if 'DATE' in item[1]:
                    item[1] = item[1].replace("DATE", "")

                x = item[1].split(",")
                item.pop(1)
                for i in x:
                    item.append(i)

                smart_desc = handle_description(desc)
                for i in smart_desc:
                    item.append(i)

                if len(item) == 5:
                    li.append(item)
    return li


def handle_description(desc):
    # Hard coded crimes and status (will need updated with time)

    smart_desc = []

    if 'THEFT' in desc:
        crime = 'THEFT'
    elif 'TREPASSING' in desc:
        crime = 'TREPASSING'
    elif 'LIQUOR LAW VIOLATIONS' in desc:
        crime = 'LIQUOR LAW VIOLATIONS'
    elif 'DRUG ABUSE VIOLATIONS' in desc:
        crime = 'DRUG ABUSE VIOLATIONS'
    elif 'FRAUD' in desc:
        crime = 'FRAUD'
    elif 'POSSESSION' in desc:
        crime = 'POSSESSION'
    elif 'VANDALISM' in desc:
        crime = 'VANDALISM'
    elif 'PUBLIC INTOXICATION' in desc:
        crime = 'PUBLIC INTOXICATION'
    elif 'RECKLESS DRIVER' in desc:
        crime = 'RECKLESS DRIVER'
    elif 'ASSAULT' in desc:
        crime = 'ASSAULT'
    elif 'BATTERY' in desc:
        crime = 'BATTERY'
    elif 'SEX OFFENSE' in desc:
        crime = 'SEX OFFENSE'
    elif 'BURGLARY' in desc:
        crime = 'BURGLARY'
    elif 'INTIMIDATION' in desc:
        crime = 'INTIMIDATION'
    elif 'THREATS' in desc:
        crime = 'THREATS'
    elif 'HARASSMENT' in desc:
        crime = 'HARASSMENT'
    else:
        crime = 'OTHER CRIME'

    smart_desc.append(crime)

    if 'UNDER INVESTIGATION' in desc:
        status = 'UNDER INVESTIGATION'
    elif 'ARREST MADE' in desc:
        status = 'ARREST MADE'
    elif 'NOTHING FURTHER' in desc:
        status = 'NOTHING FURTHER'
    elif 'UNABLE TO LOCATE' in desc:
        status = 'UNABLE TO LOCATE'
    elif 'CASE CLOSED' in desc:
        status = 'CASE CLOSED'
    elif 'UNFOUNDED' in desc:
        status = 'UNFOUNDED'
    elif 'INACTIVE' in desc:
        status = 'INACTIVE'
    elif 'CLOSED' in desc:
        status = 'CLOSED'
    elif 'PENDING PROSECUTOR REVIEW' in desc:
        status = 'PENDING PROSECUTOR REVIEW'
    else:
        status = 'OTHER STATUS'
    
    smart_desc.append(status)

    return smart_desc


if __name__ == '__main__':
    main()