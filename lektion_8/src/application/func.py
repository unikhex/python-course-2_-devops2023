# Den här filen innehåller funktionalitet som inte är specific för Flask och servern.
# Eftersom flask inte har funktioner för att ropa på andra servrar, använder vi i denna modul istället urllib.
# Vi har nedan importerat request från urllib för att kunna ropa på externa API:er.

from urllib import request

# SSL står för Secure Socket Layer och handlar om krypterade kopplingar mellan klient och server, t.ex via HTTPS, eller SSH
import ssl

# Denna innehåller funktioner för att ladda (load, loads) och skapa (dump, dumps) JSON från python-variabler
import json

# Vi använder pandas för att arbeta med data i tabell-form. 
# Ett mycket kraftfullt ramverk för data-manipulation som vi bara skrapar på ytan av i denna kurs.
import pandas as pd

import datetime

def json_url_to_html_table(data_url, columns=None):
    '''Denna funktion tar en URL, går till den platsen och hämtar resultatet
        Funktionen förväntar sig JSON som sedan laddas in i ett Pandas DataFrame (tabell) som översätts till en HTML-tabell.'''

    # Här skapar vi en regel som säger att vi accepterar att uppkopplingen mot API:et inte är krypterat
    context = ssl._create_unverified_context()

    # Till skillnad från i lektion_4 har vi nu lagt in den kod vi inte har full kontroll över i en try statement.
    # Detta för att vi inte kan vara säkra på att sidan som URL pekar till kommer att svara, eller ens att nätverket är tillgängligt
    try:
        # Läs informationen som returneras från addressen (URL)
        json_data = request.urlopen(data_url, context=context).read()
        # Gör om json (vilken kommer som en binär sträng) till en dictionary som är fullt läsbar med Python
        data = json.loads(json_data)

        # Skapa en Pandas DataFrame med innehållet i vår dictionary.
        # Om vi skickade med en lista med kolumnnamn så returnera endast dem som en HTML-tabell, annars tar vi med alla existerande kolumner
        df = pd.DataFrame(data)
        if columns==None:
            table_data = df.to_html(classes="table p-5", justify="left")    
        else:
            table_data = df.to_html(columns=columns,classes="table p-5", justify="left")

        # Returnera HTML-tabellen till app.py där ifrån funktionen ropades på
        return table_data

    # Fånga alla eventuella Exception som kan uppstå, t.ex HTTPException från request och returnera det istället för en html-tabell till anropet
    # Här skulle man kunna hantera specifika Exception, men för nu så plockar vi dem alla.
    except Exception as err:
        return err



def xml_url_to_html_table(data_url, xpath="", columns=None):
    '''Denna funktion tar en URL, går till den platsen och hämtar resultatet
        Funktionen förväntar sig ett XML-format (t.ex RSS) som sedan laddas in i ett Pandas DataFrame (tabell) som översätts till en HTML-tabell.'''

    # Samma funktion som ovan (json_url_to_html_table) men för XML-data

    # Här skapar vi en regel som säger att vi accepterar att uppkopplingen mot API:et inte är krypterat
    context = ssl._create_unverified_context()

    # Till skillnad från i lektion_4 har vi nu lagt in den kod vi inte har full kontroll över i en try statement.
    # Detta för att vi inte kan vara säkra på att sidan som URL pekar till kommer att svara, eller ens att nätverket är tillgängligt
    try:
        # Läs informationen som returneras från addressen (URL)
        xml = request.urlopen(data_url, context=context).read()

        # Skapa en DataFrame direkt från XML med funktionen read_xml() i Pandas.
        # Om vi skickade med en lista med kolumnnamn så returnera endast dem som en HTML-tabell, annars tar vi med alla existerande kolumner
        df = pd.read_xml(xml, xpath=xpath)
        if columns==None:
            table_data = df.to_html(classes="table p-5", justify="left")    
        else:
            table_data = df.to_html(columns=columns,classes="table p-5", justify="left")

        # Returnera HTML-tabellen till app.py där ifrån funktionen ropades på
        return table_data

    # Fånga alla eventuella Exception som kan uppstå, t.ex HTTPException från request och returnera det istället för en html-tabell till anropet
    # Här skulle man kunna hantera specifika Exception, men för nu så plockar vi dem alla.
    except Exception as e:
        return e

def get_countries():
    # Här skapar vi en regel som säger att vi accepterar att uppkopplingen mot API:et inte är krypterat
    context = ssl._create_unverified_context()

    try:
        # Läs informationen som returneras från addressen (URL)
        data = request.urlopen("https://date.nager.at/api/v3/AvailableCountries", context=context).read()
        return json.loads(data)

    except Exception as err:
        return err


def text_url_to_dict(data_url, key="", separator=":"):
    # Här skapar vi en regel som säger att vi accepterar att uppkopplingen mot API:et inte är krypterat
    context = ssl._create_unverified_context()

    try:
        # Läs informationen som returneras från addressen (URL)
        # Texten som kommer är en binär sträng b"text" inte en vanlig sträng "text", så vi måste konvertera den
        # detta går vi med decode()
        data = request.urlopen(data_url, context=context).read().decode()

        # Dela upp texten i en lista vid varje ny rad
        data = data.split("\n")

        # Skapa en tom dictionary
        dictionary = {}
        # Sista brytningen skapar en tom rad, därav att vi loopar från början till en rad innan sista
        for row in data[:-1]:
            # Dela varje rad, t.ex loc=SE där lika med-tecknet finns
            pairs = row.split(separator)
            # Nu har vi key i pairs[0] och value i pairs[1], så vi lägger till paren i dict
            dictionary[pairs[0]] = pairs[1] 
        
        # Om anropet inte bad om en sträng baserad på nyckel, så returnera hela dictionary'n
        if key=="":
            return dictionary
        else:
            # Om det skickades en nyckel så returnera värded som efterfrågades
            if key in dictionary.keys():
                return dictionary[key]
            else:
                # I övriga fall returnera en tom dictionary
                return {}

    except Exception as err:
        return err
    
def get_countries_as_html_table(selection=[], columns=[]):
    # Här skapar vi en regel som säger att vi accepterar att uppkopplingen mot API:et inte är krypterat
    context = ssl._create_unverified_context()

    try:

        # Skapa ett dataframe
        df = pd.DataFrame()

        # Hämta lista över tillgängliga länder
        countries = get_countries()

        # Sätt year till nuvarande år
        year = datetime.datetime.now().date().year

        # Loopa igenom countries (åtta första) i det här exemplet
        for country in countries:
            #Plocka ut country_code
            loc = country['countryCode']
            if loc in selection:

                data_url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{loc}"
                # Hämta data för ett nytt land varje gång vi loopar
                json_data = request.urlopen(data_url, context=context).read()
                # Översätt json till en dict
                data = json.loads(json_data)
                # Skapa en temporär dataframe med denna dict
                df_temp = pd.DataFrame(data)

                # Spara endast 'date'- och 'name'-kolumnerna
                df_temp = df_temp[['date','name']]
                # Byt namn på kolumnerna. Den första till "Date", den andra till loopens nuvarande lands namn
                df_temp.columns = ['Date', country['name']]

                # Kolla om df (den dataframe vi skapade utanför loopen) har några rader, annars är det här det första landet
                if len(df) == 0:
                    # Sätt df till värdet av den tillfälliga DataFramen df_temp
                    df = df_temp
                else:
                    # Eftersom längden på tabellen/dataframe var mer än 0, så är detta ett tillägg
                    # så vi slår ihop df_temp med det som redan finns i df, matchat på kolumnen "Date"
                    # Det som läggs till är det som skiljer df och df_temp åt, dvs. kolumnen i df_temp med titeln som nya landsnamnet
                    df = pd.merge(df, df_temp, left_on="Date", right_on="Date", how="outer")
                    # Ersätt alla tomma fält (default är NaN = Not a Number) med en tom sträng
                    df.fillna("", inplace=True)

        # Sortera Date-kolumnen
        df.sort_values(by='Date', inplace=True)
        # När vi har loopat igenom alla rader, så skapar vi en html_tabell som vi returnerar
        table_data = df.to_html(classes="table p-5 table-striped", justify="left", index=False)    

        # Skicka tillbaka tabellen till app.py där den ropades på ifrån
        return table_data

    except Exception as err:
        return err
