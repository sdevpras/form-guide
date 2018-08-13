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
            final_table[row[0]] = remove_quote(row, start, end, type)
    f.close()
    return final_table

def table_write(filename, table):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
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


def main():
    latest_table = scrape('https://www.bbc.co.uk/sport/football/premier-league/table')
    local_table = table_read('pltable.csv', 0, 9, 0)
    local_form = table_read('plform.csv', 2, 8, 1)

    for team in latest_table:
        if team[1] != local_table[team[0]][0]:
            goals_scored = team[5] - local_table[team[0]][4]
            goals_conceded = team[6] - local_table[team[0]][5]
            result = team[8] - local_table[team[0]][7]

            local_form = change_form(local_table, local_form, team[0], goals_scored, goals_conceded, result)
    local_table = change_table(local_table, latest_table)





if __name__ == '__main__':
    main()