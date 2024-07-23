import json
import debugging
from os import path

db = debugging.Debug()

class Theme():
    def __init__(self):
        self.config = None
        self.default_themes = ["light", "dark", "rose-pine"]
        self.default_themes_data = [{
        "sys-mode": "light",
        "main-fg-color": "white",

        "subwn-txt-color": "black",
        "subwn-fg-color": "white",
        "subwn-btn-color": "black",
        "subwn-cancel-btn-color": "black",
        "subwn-btn-txt-color": "white",
        "subwn-btns-hover-color": "#A3BCE1",
        "subwn-tarea-fg": "white",

        "title-font": ["Arial", 20],
        "title-text-color": "black",
        "title-fg-color": "transparent",
        "title-corner-radius": 0,

        "mframe-fg-color": "white",
        "mframe-corner-radius": 0,
        "mframe-border-width": 0,
        "mframe-border-color": "white",
        "mframe-scrlbar-fg-color": "white",
        "mframe-scrlbar-hover-color": "grey",
        "mframe-scrlbar-btn-color": "white",

        "cards-alt-colors": ["#f0f0f0", "#ffffff"],
        "cards-corner-radius": 5,
        "cards-font": ["SF Display", 15],
        "cards-txt-pady": 3,
        "cards-txt-padx": 3,
        "cards-txt-color": "black",
        "card-btns-txt-color": "black",
        "card-btns-hover-color": "lightgrey",
        "card-btn-opts-icon": "⚙︎",
        "cards-btn-icon-font": ["SF Display", 18],

        "footer-fg-color": "white",
        "footer-corner-radius": 0,
        "footer-border-width": 0,
        "footer-border-color": "white",

        "btn-export-txt-color": "white",
        "btn-export-fg-color": "black",
        "btn-export-hover-color": "#325882",
        "btn-export-corner-radius": 5,
        "btn-export-border-width": 0,
        "btn-export-border-color": "black",

        "btn-pause-txt-color": "white",
        "btn-pause-fg-color": "black",
        "btn-pause-hover-color": "#325882",
        "btn-pause-corner-radius": 5,
        "btn-pause-border-width": 0,
        "btn-pause-border-color": "black",

        "btn-ncontext-txt-color": "grey",
        "btn-ncontext-fg-color": "white",
        "btn-ncontext-hover-color": "lightgrey",
        "btn-ncontext-corner-radius": 5,
        "btn-ncontext-border-width": 1,
        "btn-ncontext-border-color": "grey",

        "optsmenu-fg-color": "white",
        "optsmenu-text-color": "grey",
        "optsmenu-btn-color": "white",
        "optsmenu-btn-hover-color": "lightgrey",
        "optsmenu-btn-padding-color": "white",
        "optsmenu-corner-radius": 5,
        "optsmenu-border-width": 1,
        "optsmenu-border-color": "grey",

        "wait-animation": ["⠁", "⠂", "⠄", "⡀", "⡈", "⡐", "⡠", "⣀", "⣁", "⣂", "⣄", "⣌", "⣔", "⣤", "⣥", "⣦", "⣮", "⣶", "⣷", "⣿", "⡿", "⠿", "⢟", "⠟", "⡛", "⠛", "⠫", "⢋", "⠋", "⠍", "⡉", "⠉", "⠑", "⠡", "⢁"]
        },
        {
        "sys-mode": "dark",
        "main-fg-color": "#161B21",

        "subwn-txt-color": "white",
        "subwn-fg-color": "#161B21",
        "subwn-btn-color": "#7D8FA9",
        "subwn-cancel-btn-color": "#7D8FA9",
        "subwn-btn-txt-color": "#1D232C",
        "subwn-btns-hover-color": "#A3BCE1",
        "subwn-tarea-fg": "#161B21",

        "title-font": ["Arial", 20],
        "title-text-color": "white",
        "title-fg-color": "#161B21",
        "title-corner-radius": 0,

        "mframe-fg-color": "#161B21",
        "mframe-corner-radius": 0,
        "mframe-border-width": 0,
        "mframe-border-color": "white",
        "mframe-scrlbar-fg-color": "#161B21",
        "mframe-scrlbar-hover-color": "#0077E4",
        "mframe-scrlbar-btn-color": "#161B21",

        "cards-alt-colors": ["#222A34", "#161B21"],
        "cards-corner-radius": 5,
        "cards-font": ["SF Display", 15],
        "cards-txt-pady": 3,
        "cards-txt-padx": 3,
        "cards-txt-color": "white",
        "card-btns-txt-color": "white",
        "card-btns-hover-color": "lightgrey",
        "card-btn-opts-icon": "⚙︎",
        "cards-btn-icon-font": ["SF Display", 18],

        "footer-fg-color": "#161B21",
        "footer-corner-radius": 0,
        "footer-border-width": 0,
        "footer-border-color": "white",

        "btn-export-txt-color": "#EEF0F4",
        "btn-export-fg-color": "#7D8FA9",
        "btn-export-hover-color": "#A3BCE1",
        "btn-export-corner-radius": 5,
        "btn-export-border-width": 1,
        "btn-export-border-color": "#7D8FA9",

        "btn-pause-txt-color": "#EEF0F4",
        "btn-pause-fg-color": "#7D8FA9",
        "btn-pause-hover-color": "#A3BCE1",
        "btn-pause-corner-radius": 5,
        "btn-pause-border-width": 1,
        "btn-pause-border-color": "#7D8FA9",

        "btn-ncontext-txt-color": "#EEF0F4",
        "btn-ncontext-fg-color": "#7D8FA9",
        "btn-ncontext-hover-color": "#A3BCE1",
        "btn-ncontext-corner-radius": 5,
        "btn-ncontext-border-width": 0,
        "btn-ncontext-border-color": "#7D8FA9",

        "optsmenu-text-color": "#EEF0F4",
        "optsmenu-fg-color": "#7D8FA9",
        "optsmenu-btn-color": "#7D8FA9",
        "optsmenu-btn-hover-color": "#A3BCE1",
        "optsmenu-btn-padding-color": "#7D8FA9",
        "optsmenu-corner-radius": 5,
        "optsmenu-border-width": 1,
        "optsmenu-border-color": "#7D8FA9",

        "wait-animation": ["⠁", "⠂", "⠄", "⡀", "⡈", "⡐", "⡠", "⣀", "⣁", "⣂", "⣄", "⣌", "⣔", "⣤", "⣥", "⣦", "⣮", "⣶", "⣷", "⣿", "⡿", "⠿", "⢟", "⠟", "⡛", "⠛", "⠫", "⢋", "⠋", "⠍", "⡉", "⠉", "⠑", "⠡", "⢁"]
        },
        {
        "sys-mode": "dark",
        "main-fg-color": "#191723",

        "subwn-txt-color": "#E0DEF2",
        "subwn-fg-color": "#191723",
        "subwn-btn-color": "#BFA8E3",
        "subwn-cancel-btn-color": "#BFA8E3",
        "subwn-btn-txt-color": "#440000",
        "subwn-btns-hover-color": "#E0DEF2",
        "subwn-tarea-fg": "#191723",

        "title-font": ["Times", 22],
        "title-text-color": "white",
        "title-fg-color": "#191723",
        "title-corner-radius": 0,

        "mframe-fg-color": "#191723",
        "mframe-corner-radius": 0,
        "mframe-border-width": 0,
        "mframe-border-color": "white",
        "mframe-scrlbar-fg-color": "#191723",
        "mframe-scrlbar-hover-color": "#E0DEF2",
        "mframe-scrlbar-btn-color": "#191723",

        "cards-alt-colors": ["#252337", "#191723"],
        "cards-corner-radius": 20,
        "cards-font": ["Helvetica", 15],
        "cards-txt-pady": 5,
        "cards-txt-padx": 5,
        "cards-txt-color": "#E0DEF2",
        "card-btns-txt-color": "#E0DEF2",
        "card-btns-hover-color": "#BFA8E3",
        "card-btn-opts-icon": "⚙︎",
        "cards-btn-icon-font": ["Helvetica", 20],

        "footer-fg-color": "#191723",
        "footer-corner-radius": 0,
        "footer-border-width": 0,
        "footer-border-color": "white",

        "btn-export-txt-color": "#440000",
        "btn-export-fg-color": "#BFA8E3",
        "btn-export-hover-color": "#E0DEF2",
        "btn-export-corner-radius": 5,
        "btn-export-border-width": 1,
        "btn-export-border-color": "#BFA8E3",

        "btn-pause-txt-color": "#440000",
        "btn-pause-fg-color": "#BFA8E3",
        "btn-pause-hover-color": "#E0DEF2",
        "btn-pause-corner-radius": 5,
        "btn-pause-border-width": 1,
        "btn-pause-border-color": "#BFA8E3",

        "btn-ncontext-txt-color": "#440000",
        "btn-ncontext-fg-color": "#BFA8E3",
        "btn-ncontext-hover-color": "#E0DEF2",
        "btn-ncontext-corner-radius": 5,
        "btn-ncontext-border-width": 0,
        "btn-ncontext-border-color": "#BFA8E3",

        "optsmenu-fg-color": "#BFA8E3",
        "optsmenu-text-color": "#440000",
        "optsmenu-btn-color": "#BFA8E3",
        "optsmenu-btn-hover-color": "#E0DEF2",
        "optsmenu-btn-padding-color": "#BFA8E3",
        "optsmenu-corner-radius": 5,
        "optsmenu-border-width": 1,
        "optsmenu-border-color": "#BFA8E3",

        "wait-animation": ["⠁", "⠂", "⠄", "⡀", "⡈", "⡐", "⡠", "⣀", "⣁", "⣂", "⣄", "⣌", "⣔", "⣤", "⣥", "⣦", "⣮", "⣶", "⣷", "⣿", "⡿", "⠿", "⢟", "⠟", "⡛", "⠛", "⠫", "⢋", "⠋", "⠍", "⡉", "⠉", "⠑", "⠡", "⢁"]
        }]

    def load_from_config(self):
        config_file_path = path.join(path.expanduser('~'), "clipycards.config")
        theme = ""
        if not path.exists(config_file_path):
            db.log_warn(__name__ , f"Config file not found at {config_file_path} -- created a new file")
            return self.default_themes_data[0]

        try:
            theme = self.config_theme_name_get(config_file_path)
        except Exception as e:
            db.log_crit(__name__, e,f"Can't read the config file at {config_file_path} -- created a new file")
            return self.default_themes_data[0]

        if theme in self.default_themes:
            #print("loaded default theme --> ", theme)
            return self.default_themes_data[self.default_themes.index(theme)]

        #print("theme not in defaults")
        try:
            with open(theme) as fo:
                theme = json.load(fo)
                missing_keys = set(self.default_themes_data[0]) - set(theme)
                theme = self.default_themes_data[0] if len(missing_keys) else theme
                return theme
        except Exception as e:
            #print("couldn't open the custom theme")
            db.log_err(__name__ , e, f"Couldn't open the theme file -- using the default light theme")
            return self.default_themes_data[0]

    def config_theme_name_get(self, config_file_path):
        with open(config_file_path, "r") as fo:
            self.config = json.load(fo)
            if not "theme" in self.config:
                db.log_warn(__name__, "Missing \"theme\" key from config file -- using the default light theme")
                self.config.update({"theme": "light"})
                return "light"
            theme = self.config["theme"]
            #print("loaded from config theme: --> ", theme)
            return theme