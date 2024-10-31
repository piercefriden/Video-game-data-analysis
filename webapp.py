from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)


@app.route('/')
def render_home():
    return render_template('home.html')
    
@app.route('/p1')
def render_page1():
    Titles = get_Title_options()
    #print(Titles)
    return render_template('page1.html', Title_options=Titles)

@app.route('/p2')
def render_page2():
    graphpoints=format_dict_as_graph_points(get_ratings_per_year())
    print(graphpoints)
   
    return render_template('page2.html', points=graphpoints)

    
@app.route("/p3")
def render_page3():
    with open('video_games.json') as videoGames_data:
        videoGames = json.load(videoGames_data)
    consoles = get_console_options()
    #print(games)
    if "console" in request.args:
            game_list=[]
            console = request.args.get('console')
            for games in videoGames:
                if games["Release"]["Console"]==console:
                    game_list.append(games["Title"])
            return render_template('page3.html', console_options=consoles, consoleFacts=game_list)
    return render_template('page3.html', console_options=consoles)
    
@app.route('/showFact')
def render_fact():
    Titles = get_Title_options()
    Title = request.args['Title']
    Length = Length_average(Title)
    """Length2 = most_black_individuals(Title)"""
    fact = "In " + Title + ", the average playtime is " + str(round(Length,1)) + " hours."
    """fact2 = "In " + Title + " the Length with the highest black population is " + Length2 + "." """
    return render_template('page1.html', Title_options=Titles, funFact=fact)
    
def get_Title_options():
    """Return the html code for the drop down menu.  Each option is a Title abbreviation from the demographic data."""
    with open('video_games.json') as video_game_data:
        games = json.load(video_game_data)
    Titles=[]
    for c in games:
        if c["Title"] not in Titles:
            Titles.append(c["Title"])
    options=""
    for s in Titles:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options

def Length_average(Title):
    """Return the name of a Length in the given Title with the highest percent of under 18 year olds."""
    with open('video_games.json') as video_game_data:
        games = json.load(video_game_data)
    highest=0
    for c in games:
        if c["Title"] == Title:
            highest = c["Length"]["All PlayStyles"]["Average"]
    return highest
    
def get_console_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('video_games.json') as video_console_data:
        VidCon = json.load(video_console_data)
    consoles=[]
    for v in VidCon:
        if v["Release"]["Console"] not in consoles:
            consoles.append(v["Release"]["Console"])
    options=""
    for g in consoles:
        options += Markup("<option value=\"" + g + "\">" + g + "</option>")
    return options
    
def get_ratings_per_year():
    with open('video_games.json') as game_data:
        games = json.load(game_data)
   
    years = {}
   
    for c in games:
        if c["Release"]["Year"] in years:
            years[c["Release"]["Year"]] = years[c["Release"]["Year"]] + 1
        else:
            years[c["Release"]["Year"]] = 1
   
    return years

def format_dict_as_graph_points(data):
    graph_points = ""
    for key in data:
        graph_points = graph_points + Markup('{ y: ' + str(data[key]) + ', label: "' + str(key) + '" }, ')
    graph_points = graph_points[:-2]
    return graph_points
    
    """
def most_black_individuals(Title):
    """"""Return the name of a Length in the given Title with the highest percent of under 18 year olds.""""""
    with open('video_games.json') as video_game_data:
        games = json.load(video_game_data)
    highest=0
    Length = ""
    for c in games:
        if c["Title"] == Title:
            if c["Ethnicities"]["Black Alone"] > highest:
                highest = c["Ethnicities"]["Black Alone"]
                Length = c["Length"]
    return Length
"""
def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url
    
def get_cases_day():
    with open('video_games.json') as video_games:
        videogamesdata = json.load(video_games)
    cases = "["
    for m in videogamesdata:
        if m["Date"]["Month"] == 8:
            if m["Country"]["Full"] == "Spain":
                cases= cases + Markup ("{ x: " + str(m["Date"]["Day"]) + ", y: " +str(m["Data"]["Cases"]["Total"]) + "},") #{x: 8, y: 10}
    cases = cases[:-1] + "]"
    return cases    


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production