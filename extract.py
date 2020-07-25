import bs4 as bs
import urllib.request
import json
import re

leagues = {
    'Premier League': 'https://www.skysports.com/premier-league-table',
    'La Liga': 'https://www.skysports.com/la-liga-table',
    'Serie A': 'https://www.skysports.com/serie-a-table',
    'Bundesliga': 'https://www.skysports.com/bundesliga-table',
    'Ligue 1': 'https://www.skysports.com/ligue-1-table'
}

def getForm(tableData, team):
    spans = tableData.find_all('span')
    formString, formPoints, formGD, formLastSixPoints = ('', 0, 0, [])
    for span in reversed(spans):
        text = span['title']
        score = list(map(int, re.search('[0-9]+-[0-9]+', text).group(0).split('-')))
        home = re.search(r'\A' + re.escape(team), text)
        diff = score[1] - score[0]
        if home:
            diff *= -1
        formGD += diff    
        if diff > 0:
            formString += 'W'
            formPoints += 3
            formLastSixPoints.insert(0, formPoints)  
        elif diff < 0:
            formString += 'L'
            formPoints += 0
            formLastSixPoints.insert(0, formPoints)
        else:
            formString += 'D'
            formPoints += 1
            formLastSixPoints.insert(0, formPoints)

    formDict = {}
    formDict['formString'] = formString
    formDict['formPoints'] = formPoints
    formDict['formGD'] = formGD
    formDict['formLastSixPoints'] = formLastSixPoints
    return formDict

def getJSONRow(tableRow):
    td = tableRow.find_all('td')
    rowDict = {}
    rowDict['rank'] = td[0].text.strip()
    rowDict['team'] = td[1].text.strip()
    rowDict['played'] = td[2].text.strip()
    rowDict['won'] = td[3].text.strip()
    rowDict['drawn'] = td[4].text.strip()
    rowDict['lost'] = td[5].text.strip()
    rowDict['for'] = td[6].text.strip()
    rowDict['against'] = td[7].text.strip()
    rowDict['gd'] = td[8].text.strip()
    rowDict['points'] = td[9].text.strip()
    rowDict['form'] = getForm(td[10], rowDict['team'])
    return rowDict

def scrape(url):
    sauce = urllib.request.urlopen(url)
    soup = bs.BeautifulSoup(sauce, 'html.parser')
    table = soup.find('tbody')
    table_rows = table.find_all('tr')
    final_table = []
    for tr in table_rows:
        final_table.append(getJSONRow(tr))
    return final_table
  
def main():
    outFile = open('table.json', 'w')
    final = {}
    for key, value in leagues.items():
        final[key] = scrape(value)
    json.dump(final, outFile)
    outFile.close()

if __name__ == '__main__':
    main()