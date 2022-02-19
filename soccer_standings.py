# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask import request

import requests
from bs4 import BeautifulSoup

def domestic(league_name):
    
    lg_names = ['PREMIER LEAGUE', 'LA LIGA', 'BUNDESLIGA', 'SERIE A', 'LIGUE 1']
    lgs = ["eng.1", "esp.1", "ger.1", "ita.1", "fra.1"]
    
    ind = lg_names.index(league_name)
    
    url = "https://www.espn.com/soccer/standings/_/league/" + lgs[ind]


    r = requests.get(url,timeout=2.5)
    r_html = r.text

    soup = BeautifulSoup(r_html, 'html.parser')

    teams = soup.find_all("span", attrs={"class": "hide-mobile"})
    teams = [str(l) for l in teams]

    left, right = '"0">', "</a></span>"
    teams = [l[l.index(left)+len(left):l.index(right)] for l in teams]
    teams = [i.replace('&amp;', '&') for i in teams]
    table_data = soup.find_all("span", attrs={"class": "stat-cell"})
    table_data = [str(l) for l in table_data]

    left, right = '">', '</span>'

    table_data = [l[l.index(left)+len(left):l.index(right)] for l in table_data]

    gp = table_data[0::8]
    w = table_data[1::8]
    d = table_data[2::8]
    l = table_data[3::8]
    f = table_data[4::8]
    a = table_data[5::8]
    gd = table_data[6::8]
    p = table_data[7::8]

    standing = [i for i in range(1, 21)]

    ct = 0
    data_list = []

    while ct < len(teams):

        data_list.append(standing[ct])
        data_list.append(teams[ct])
        data_list.append(gp[ct])
        data_list.append(w[ct])
        data_list.append(d[ct])
        data_list.append(l[ct])
        data_list.append(f[ct])
        data_list.append(a[ct])
        data_list.append(gd[ct])
        data_list.append(p[ct])

        ct += 1
    
    ct = 0
    final_data = []
    
    while ct < len(data_list):
        final_data.append(data_list[ct:ct + 10])
        ct += 10

    headings = ['Standing', 'Team', 'GP' ,'W', 'D', 'L', 'GF', 'GA', 'GD', 'P']
    
    return render_template("standings_table.html", headings=headings, final_data=final_data, league_name=league_name)