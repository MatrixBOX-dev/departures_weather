def country_name(country):
    names = {
        "de": "Germany",
        "se": "Sweden",
    }
    return names.get(country, country)


station_names_dict = {
    "Hässelby strand": "Hässelby str.",
    "Skärmarbrink": "Skärmarbr.",
    "Sankt Eriksplan": "St. Eriksplan",
    "Hammarbyhöjden": "Hammarbyh.",
    "Danderyds sjukhus": "Danderyds sjh",
    "Fridhemsplan": "Fridhemspl.",
    "Solna centrum": "Solna C",
    "Enskede gård": "Enskede grd",
    "Västra skogen": "Väst. skogen",
    "Rådmansgatan": "Rådmansg.",
    "Midsommarkransen": "Midsommarkr.",
    "Sundbyberg centrum": "Sundbyberg C",
    "Medborgarplatsen": "Medborgarpl.",
    "Hägerstensåsen": "Hägerstens:en",
    "Östermalmstorg": "Östermalmst.",
    "Mörby centrum": "Mörby centr.",
    "Tekniska högskolan": "Tekn. Högsk.",
    "Kungsträdgården": "Kungsträdg.",
    "Skogskyrkogården": "Skogskyrkog.",
    "Stockholms östra": "Stockholm Ö",
    "Stockholm C": "Stockholm C",
    "Farsta strand": "Farsta str.",
}


replace_list_destinations = [
    (" central", " C"),
    (" centrum", " C"),
    (" Central", " C"),
    (" Centrum", " C"),
    (" hauptbahnhof", " Hbf"),
    (" Hauptbahnhof", " Hbf"),
    (" Station", " Stn."),
    (" station", " stn."),
    (" sjukhuset", " sjh."),
    (" sjukhus", " sjh."),
    (" strand", " str."),
    (" flygplats", " fpl."),
    (" Norra", " N:a"),
    (" norra", " n:a"),
    (" Södra", " S:a"),
    (" södra", " s:a"),
    (" Östra", " Ö:a"),
    (" östra", " ö:a"),
    (" Västra", " V:a"),
    (" västra", " v:a"),
    (" via ", " v "),
]


def url_decode(s):
    out = ""
    i = 0
    while i < len(s):
        if s[i] == "+":
            out += " "
            i += 1
        elif s[i] == "%" and i + 2 < len(s):
            try:
                out += chr(int(s[i + 1:i + 3], 16))
                i += 3
            except:
                out += s[i]
                i += 1
        else:
            out += s[i]
            i += 1

    # UTF-8-Sonderfälle, die chr(byte) allein falsch macht
    replacements = {
        "Ã¤": "ä", "Ã¶": "ö", "Ã¼": "ü",
        "Ã„": "Ä", "Ã–": "Ö", "Ãœ": "Ü",
        "Ã¥": "å", "Ã…": "Å", "ÃŸ": "ß",
        "Ã©": "é", "Ã¨": "è",
        "â€“": "–", "â€”": "—",
    }
    for a, b in replacements.items():
        out = out.replace(a, b)
    return out


settingstxt = {
    "utc_offset": 1,
    "summer_time": 0,
    "password": "none",
    "mystation": "",
    "brightness": 0,
    "listmode": 0,
    "rotation": 0,
    "maxdest": 5,
    "scroll": 0,
    "ssid": "my_ssid",
    "offset": 0,
    "mini": 0,
    "large_list": 0,
    "xs_line_id": 0,
    "clocktime": 0,
    "user": "",
    "power": 20,
    "show_lines": [],
    "rt_indicator": 1,
    "line_length": 3,
    "no_more_departures": "",
    "mins": " min",
    "sleep": 0,
    "button_mode": 0,
    "show_my_station": 0,
    "siteid": "00",
    "METRO": 1,
    "SHIP": 0,
    "BUS": 0,
    "TRAIN": 0,
    "TRAM": 0,
    "direction": 0,
    "show_msgs": 0,
    "buses_option": 0,
    "red": 1,
    "green": 1,
    "blue": 1,
    "operator": "",
    "country": "de",
    "listcolor": 1,
    "listcolor_time": 1,
    "version": "2.99",
    "color": 1,
    "long": 0,
    "invert": 0,
    "multiple": 0,
    "timer": {
        "Monday": "",
        "Tuesday": "",
        "Wednesday": "",
        "Thursday": "",
        "Friday": "",
        "Saturday": "",
        "Sunday": "",
    },
    "stations": {
        "1": {
            "mystation": "",
            "siteid": "",
            "METRO": 1,
            "SHIP": 1,
            "BUS": 1,
            "TRAIN": 1,
            "TRAM": 1,
            "direction": 0,
            "show_msgs": 0,
            "buses_option": 0,
            "red": 1,
            "green": 1,
            "blue": 1,
            "operator": "vvo",
            "country": "de",
            "offset": 0,
            "active": True,
        }
    },
}


weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

month = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}

list_shade = {"be": 1}