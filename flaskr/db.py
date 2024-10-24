import sqlite3
from requests import get
from bs4 import BeautifulSoup

import click
from flask import current_app, g

@click.command("scrape-data")
def scrape_data():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))
    
    response = get("https://fr.wikipedia.org/wiki/Liste_des_pays_par_PIB_(PPA)_par_habitant")

    soup = BeautifulSoup(response.content, "html5lib")

    table = soup.find_all('table', attrs = {"class":"wikitable alternance"})[1].tbody
    rows = table.find_all("tr")
    rows.pop(0)

    db = get_db()

    for row in rows:
        cells = row.find_all("td")

        rank = int(cells[0].contents[0])
        try:
            country = cells[1].find("span", {"class":"datasortkey"}).contents[1].text
        except:
            country = cells[1].find_all("a")[1].text
        pib = int(cells[2].contents[0].replace("\xa0", "").replace("\n",""))

        db.execute(f"INSERT INTO country_pib VALUES ({rank}, \"{country}\", {pib});")
    
    db.commit()
    
    click.echo("Base de donnée initialisée")
    

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(scrape_data)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()