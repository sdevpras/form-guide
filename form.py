import bs4 as bs
import urllib.request
import csv

res_dict = {3: 'W', 1: 'D', 0: 'L'}
pts_dict = {'W': 3, 'D': 1, 'L': 0}

def remove_quote(list1, start, end, type):
    if type == 0:
        row2 = list(map(int, list1[start+1:end]))
    elif type == 1:
        row2 = list(map(int, list1[start+1:end-1]))
    else:
        row2 = list(map(int, list1[start+1:end]))
    if type == 3:
        row2.insert(0, list1[2])
    elif type ==1:
        row2.insert(0,list1[2])
        row2.insert(0, list1[1])
        row2.append(list1[end-1])
    return row2

def scrape(url):
    sauce = urllib.request.urlopen(url)
    soup = bs.BeautifulSoup(sauce, 'lxml')
    table = soup.find('tbody')
    table_rows = table.find_all('tr')
    final_table = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        final_table.append(remove_quote(row, 2, 11, 3))
    return final_table

def table_read(filename, start, end, type):
    with open(filename) as f:
        reader = csv.reader(f)
        final_table = {}
        for row in reader:
            if row[0] == 'Team':
                continue
            final_table[row[0]] = remove_quote(row, start, end, type)
    f.close()
    return final_table

def table_write(filename, table):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(table)
    f.close()

def get_sum(goals):
    goals = int(goals)
    sum = 0
    while (goals > 0):
        sum += goals%10
        goals //= 10
    return sum

def get_res(form):
    sum = 0
    for i in range(len(form)):
        sum += pts_dict[form[i]]
    return sum

def change_form(local_table, local_form, team, goals_scored, goals_conceded, result):
    if(local_table[team][0] == 0):
        local_form[team][0] = str(goals_scored)
        local_form[team][1] = str(goals_conceded)
        local_form[team][6] = res_dict[result]

    elif(local_table[team][0] < 6):
        local_form[team][0] = local_form[team][0] + str(goals_scored)
        local_form[team][1] = local_form[team][1] + str(goals_conceded)
        local_form[team][6] = local_form[team][6] + res_dict[result]

    else:
        local_form[team][0] = local_form[team][0][1:6] + str(goals_scored)
        local_form[team][1] = local_form[team][1][1:6] + str(goals_conceded)
        local_form[team][6] = local_form[team][6][1:6] + res_dict[result]

    local_form[team][2] = get_sum(local_form[team][0])
    local_form[team][3] = get_sum(local_form[team][1])
    local_form[team][4] = local_form[team][2] - local_form[team][3]
    local_form[team][5] = get_res(local_form[team][6])

    return local_form

def change_table(local_table, latest_table):
    for team in latest_table:
        local_table[team[0]] = team[1:9]
    return local_table

def make_table(url, formfile, tablefile):
    latest_table = scrape(url)
    local_table = table_read(tablefile, 0, 9, 0)
    local_form = table_read(formfile, 2, 8, 1)

    for team in latest_table:
        if team[1] != local_table[team[0]][0]:
            goals_scored = team[5] - local_table[team[0]][4]
            goals_conceded = team[6] - local_table[team[0]][5]
            result = team[8] - local_table[team[0]][7]

            local_form = change_form(local_table, local_form, team[0], goals_scored, goals_conceded, result)
    local_table = change_table(local_table, latest_table)

    local_table_write = []
    local_form_write = []
    for team in local_table.keys():
        temp1 = (local_table[team])
        temp2 = (local_form[team])
        temp1.insert(0, team)
        temp2.insert(0, team)
        local_table_write.append(temp1)
        local_form_write.append(temp2)

    local_table_write.sort(key=lambda l: (l[8], l[7], l[5]), reverse=True)
    local_form_write.sort(key=lambda l: (l[6], l[5], l[3]), reverse=True)

    local_table_write.insert(0, ['Team', 'Played', 'Won', 'Drawn', 'Lost', 'GF', 'GA', 'GD', 'Points'])
    local_form_write.insert(0, ['Team', 'GF(Individual)', 'GA(Individual)', 'GF(Cumulative)', 'GA(Cumulative)', 'GD',
                                'Points(6)', 'Form'])

    table_write(tablefile, local_table_write)
    table_write(formfile, local_form_write)

    print('Done!')


def main():
    make_table('https://www.bbc.co.uk/sport/football/premier-league/table', 'plform.csv', 'pltable.csv')
    make_table('https://www.bbc.co.uk/sport/football/french-ligue-one/table', 'l1form.csv', 'l1table.csv')
    make_table('https://www.bbc.co.uk/sport/football/spanish-la-liga/table', 'llform.csv', 'lltable.csv')
    make_table('https://www.bbc.co.uk/sport/football/italian-serie-a/table', 'saform.csv', 'satable.csv')
    make_table('https://www.bbc.co.uk/sport/football/german-bundesliga/table', 'blform.csv', 'bltable.csv')


if __name__ == '__main__':
    main()