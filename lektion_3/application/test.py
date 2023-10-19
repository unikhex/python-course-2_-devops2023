import pandas as pd

tabell = {
    "Landsdel": ["Götaland","Götaland","Götaland","Svealand","Svealand","Norrland","Norrland","Norrland","Norrland","Norrland"],
    "Landskap":["Östergtland","Östergtland","Västergötland","Södermanland","Södermanland","Södermanland","Norrbotten","Gästrikland","Ångermanland","Ångermanland","Ångermanland"],
    "Stad" : ["Linköping","Motala","Mjölby","Mariefred","Nyköping","Piteå","Sandviken","Sollefteå","Kramfors","Örnsköldsvik"]
}
df = pd.DataFrame(tabell)
html = df.to_html
return render_template

df