from flask import Flask, render_template
import pandas as pd

app = Flask(__name__,static_url_path="/static",static_folder="/lektion_3/application/static")

@app.route("/template/")
@app.route("/template/<name>")
def template(name = None):
    Dictionary = {
    "Landsdel": ["Götaland","Götaland","Götaland","Svealand","Svealand","Norrland","Norrland","Norrland","Norrland","Norrland","0"],
    "Landskap":["Östergtland","Östergtland","Västergötland","Södermanland","Södermanland","Södermanland","Norrbotten","Gästrikland","Ångermanland","Ångermanland","Ångermanland"],
    "Stad" : ["Linköping","Motala","Mjölby","Mariefred","Nyköping","Piteå","Sandviken","Sollefteå","Kramfors","Örnsköldsvik","0"]
    }
    df = pd.DataFrame(Dictionary)
    html = df.to_html(classes="table",justify="left")
    
    return render_template("template.html",data=html)
    
    