from flask import Flask, render_template
from flask import request

import requests
from bs4 import BeautifulSoup

def cup(league_name):
    
    lgs = ["uefa.champions", "uefa.europa"]
    lgs_name = ["CHAMPIONS LEAGUE", "EUROPA LEAGUE"]
    
        
    ind = lgs_name.index(league_name)

    url = "https://www.espn.com/soccer/standings/_/league/" + lgs[ind]

    r = requests.get(url,timeout=2.5)
    r_html = r.text

    soup = BeautifulSoup(r_html, 'html.parser')

    table_data = soup.find_all("span", attrs={"class": "stat-cell"})
    table_data = [str(l) for l in table_data]

    left, right = '">', "</span"
    table_data = [l[l.index(left)+len(left):l.index(right)] for l in table_data]
    
    left, right = '"0">', '</a></span>'
    teams = soup.find_all("span", attrs={"class":"hide-mobile"})
    
    teams = [str(l) for l in teams]
    
    teams = [l[l.index(left)+len(left):l.index(right)] for l in teams]
    
    left, right = '">', "</span"
    groups = soup.find_all("span", attrs={"class": "fw-medium w-100 dib"})
    groups = [str(l) for l in groups]
    
    groups = [l[l.index(left)+len(left):l.index(right)] for l in groups]

    gp = table_data[0::8]
    w = table_data[1::8]
    d = table_data[2::8]
    l = table_data[3::8]
    f = table_data[4::8]
    a = table_data[5::8]
    gd = table_data[6::8]
    p = table_data[7::8]
        
    ct, group_ct = 0, 0
    data_list = []
    
    while ct < len(gp):
        
    
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
        final_data.append(data_list[ct:ct + 9])
        ct += 9
        
    group_list = []
    ct = 0
    while ct < len(groups):
        group_list.append(groups[ct])
        group_list.append('')
        group_list.append('')
        group_list.append('')
        group_list.append('')
        group_list.append('')
        group_list.append('')
        group_list.append('')
        group_list.append('')
        
        ct += 1
    ct = 0
    group_data = []
    while ct < len(group_list):
        group_data.append(group_list[ct:ct + 9])
        ct += 9
    
    ct = 0   
    for i in group_data:
        final_data.insert(ct, i)
        ct += 5
        
    headings = ["Group", "GP", "W", "D", "L", "GF", "GA", "GD", "P"]

    return render_template("cup_standings.html", headings=headings, final_data=final_data, league_name=league_name)