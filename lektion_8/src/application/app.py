# Den här filen innehåller saker som har med Flask-servern att göra, det vill säga endpoints, routing, HTTP-metoder etc.
# Flask innehåller all funktionalitet för att skapa en server och hantera trafik till och från den servern, men inte funktionalitet
# för att skicka requests till andra servrar. Till detta använder vi i func.py istället urllib vilket är ett av pythons standardbibliotek.

# Termer: Bibliotek, standardbilbliotek, ramverk och moduler refererar ofta till samma sak, dvs. förbyggd kod som du kan importera.
# Ett standardbibliotek är ett som levereras som en del av Pyhton, och de är ofta 'native python' el. med andra ord skrivna helt i python
# Andra bibliotek kan vara skrivna med en annan miljö i bakgrunden, t.ex med C. Dessa bibliotek kan vara plattformsberoende (win, linux, mac osv)
# medan bibliotek i native python är platformsoberoende och kan användas överallt där bythonkod kan köras. 

from markupsafe import escape
from application import func
#from flask import Flask, render_template, request
from quart import Quart, render_template, request, make_response, websocket, stream_template, websocket 
import asyncio
import datetime

# Skapa ett Quart server-objekt. Det är denna som ni sedan startar med 'quart run' från terminalen.
# Quart är baserat på Flask och har samma syntax, men utöver Jinja2 osv. så importerar Quart ett 
# bibliotek som heter Asyncio, vilket skapar möjligheter för att låta programmet fortsätta med annat
# medan man väntar på att funktioner skall avslutas. Det medför alltså bättre användning av datorns 
# processor-kraft och ger mindre vänttid. 'Multitasking' genom trådar. I bakgrunden så är det fortfarande
# bara EN tråd/sekvens som körs, men det sker växling mellan uppgifter där så kan ske, t.ex i väntan på
# saker som tar tid att exekveras.  

app = Quart(__name__) # jämför: app = Flask(__name__) 

def run() -> None:
    app.run(debug=True)

# Spara inte riktiga secret keys hårdkodat i er kod, den blir eventuelt synligt på t.ex github om ni har ett öppet repository 
app.config['SECRET_KEY'] = 'MysEcreT_KeY'

# Globala variabler existerar på hela servern, dvs. alla sessioner (användare) får samma innehåll
global_log = []


@app.route("/") 
async def index():
   '''Denna funktion körs när man går till servern utan endpoint. 
      På en statisk webbsida skulle detta t.ex motsvara filen index.html'''

   ##### Plats för er kod #####
   data_url = "https://1.1.1.1/cdn-cgi/trace"
   loc = func.text_url_to_dict(data_url, separator="=", key="loc")

   # Skapa URL för det API vi skall använda, med en formaterad sträng och injecera variablerna year, samt country_code
   data_url = f"https://date.nager.at/api/v3/PublicHolidays/{datetime.datetime.now().date().year}/{loc}"

   # Använd nu den kod vi brutit ut och lagt till i func.py för att utföra arbetet
   data = func.json_url_to_html_table(data_url, columns=['date','localName','name'])

   # Skicka tillbaka resultatet till browsern med Jinja, dvs uppdatera mallen index.html med innehållet i variabeln data
   # Observera stream_template som skickar resultatet i en ström av data, istället för render_template som skickar allt på en gång.
   response = await make_response(await stream_template('index.html', title=loc, data=data))
   response.set_cookie("DevOps23", "Test cookie från /")
   return response


@app.route("/form") 
async def form():
   '''Denna funktion körs när man går till servern med  endpoint '/form'. 
      På en statisk webbsida skulle detta t.ex kunna motsvara filen mappen /form med filen index.htm'''

   countries = func.get_countries()

   ##### Plats för er kod #####
   response = await make_response(await render_template('form.html', title="Please fill in the request below", years=['2022','2023'], countries=countries, logs=global_log))
   response.set_cookie("DevOps23", "Test cookie från /form")
   return response


@app.route("/api", methods=["POST"]) 
async def api_post():
   '''Denna funktion körs när man går till servern med  endpoint '/api'. 
      Den tar endast emot trafik med HTTP method post.
      Försöker man med en annan metod, t.ex get, så körs den alltså inte.'''

   ##### Under lektion_4 skapade vi kod här för att göra göra om json från ett externt API, till en HTML-tabell med Pandas #####
   ##### Här har anropet till API:et samt omvandlingen flyttats ut till en egen funktion i filen func.py                   #####

   # Flask-kod sparar vi i app.py. Objectet request från flask innehåller den HTTP request som i det här fallet skickades till /api 
   # Läs innehållet från request som motsvarar <input> med name= 'year' samt 'countrycode' i HTML-formuläret <form> (form.html)
   year = (await request.form)["year"]
   country_code= (await request.form)["country_code"]

   # Skapa URL för det API vi skall använda, med en formaterad sträng och injecera variablerna year, samt country_code
   data_url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"

   # Använd nu den kod vi brutit ut och lagt till i func.py för att utföra arbetet
   data = func.json_url_to_html_table(data_url, columns=['date','localName','name'])

   # Skicka tillbaka resultatet till browsern med Jinja, dvs uppdatera mallen index.html med innehållet i variabeln data
   response = await make_response(await stream_template('index.html', data=data, title="Days of celebration in various countries", logs=global_log))
   response.set_cookie("DevOps23", "Test cookie från /form")
   return response


@app.route("/api/xml") 
async def xml():
   '''Denna funktion körs när man går till servern med  endpoint '/api/xml'. 
      Den tar endast emot trafik med alla HTTP methods.
      Den gör samma sak som funktionen ovan (api_post()) men med XML istället för JSON.'''

   # I det här exemplet har vi inga argument att lägga in i API:ets URL, så vi använder en vanlig sträng.
   # XPath är ett sätt att navigera i XML. Raden nedan väljer ut alla taggar med namn <item>
   data_url = "https://polisen.se/aktuellt/rss/stockholms-lan/handelser-rss---stockholms-lan/"
   data = func.xml_url_to_html_table(data_url, xpath="//item")

   # Skicka tillbaka resultatet till browsern med Jinja, dvs uppdatera mallen index.html med innehållet i variabeln data
   response = await make_response(await stream_template('index.html', data=data, title="Days of celebration in various countries", logs=global_log))
   response.set_cookie("DevOps23", "Test cookie från /api/xml")
   return response


@app.route("/merge") 
async def merge():
   global_log.append(request.host+" - Öppnade /merge")
   '''Denna endpoint ropar på get_countries_ashtml_table: en ny function som slår upp flera länders dagar, och kombinerar flera d'''

   # Använd nu den kod vi brutit ut och lagt till i func.py för att utföra arbetet
   data = func.get_countries_as_html_table(selection=['SE','FI','SK','DE'], columns=['date','name'])

   # Skicka tillbaka resultatet till browsern med Jinja, dvs uppdatera mallen index.html med innehållet i variabeln data
   response = await make_response(await stream_template('index.html', data=data, title="Days of celebration in various countries", logs=global_log))
   response.set_cookie("DevOps23", "Test cookie från /merge")
   return response


# Websocket-funktion för att skicka data
async def sending():
   while True:
      await websocket.send(datetime.datetime.now().strftime())

# Websocket-funktion för att ta emot data
async def receiving():
   while True:
      data = await websocket.receive()
      print("socket: "+data)

# Exempel på en websocket endpoint
@app.websocket('/ws')
async def ws():
   # Skapa en producer
   producer = asyncio.create_task(sending())
   # Skapa en consumet
   consumer = asyncio.create_task(receiving())
   # Registrera dessa så att de skickar data (producer) och lyssnar (consumer)
   await asyncio.gather(producer, consumer)

