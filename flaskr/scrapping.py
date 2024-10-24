
from flaskr.db import get_db

def save_data():
   response = get("https://fr.wikipedia.org/wiki/Liste_des_pays_par_PIB_(PPA)_par_habitant")

   soup = BeautifulSoup(response.content, "html5lib")

   table = soup.find_all('table', attrs = {"class":"wikitable alternance"})[1].tbody
   rows = table.find_all("tr")
   rows.pop(0)

   db = get_db()

   for row in rows:
      cells = row.find_all("td")

      id = int(cells[0].contents[0])
      try:
         country = cells[1].find("span", {"class":"datasortkey"}).contents[1].text
      except:
         country = cells[1].find_all("a")[1].text
      pib = int(cells[2].contents[0].replace("\xa0", "").replace("\n",""))

      db.execute(f"INSERT INTO country_pib VALUES ({id}, {country}, {pib};")

