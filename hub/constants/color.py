import random


class ColorMap:

    @staticmethod
    def get_color(filter, id):
        Entity = {
            "1": "#808080",
            "10": "#373737",
            "11": "#594D58",
            "3": "#322D31",
            "4": "#696880",
            "5": "#ADADC9",
            "6": "#59515E",
            "7": "#3E3D53",
            "8": "#41424C",
            "9": "#564C4D",
            "2": "#4D4C5C"
        }

        Location = {
            "1": "#c3ac77",
            "10": "#d9aa3e",
            "2": "#504222",
            "3": "#a59673",
            "4": "#e7b031",
            "5": "#af8119",
            "6": "#b39041",
            "7": "#d9b76b",
            "8": "#f3e5c7",
            "9": "#d59814"
        }
        
        Assets = {
            "1": "#16293A",
            "10": "#437DB1",
            "11": "#165B65",
            "12": "#708ea9",
            "13": "#203548",
            "2": "#779ac3",
            "3": "#6d8fb7",
            "4": "#16447a",
            "5": "#172638",
            "6": "#79a3d5",
            "7": "#3175c7",
            "8": "#7aaae3",
            "9": "#22456e"
        }

        UseCase = {
            "1": "#3d55ad",
            "12": "#414f83",
            "13": "#7380ad",
            "15": "#3554bf",
            "16": "#7a90db",
            "17": "#3556c9",
            "19": "#08102e",
            "20": "#273156",
            "2": "#526ccd",
            "4": "#162354",
            "8": "#5c78df",
            "9": "#263d91"
        }

        Function = {
            "1": "#e6ffe6",
            "12": "#b3ffb3",
            "13": "#ccffcc",
            "15": "#99ff99",
            "16": "#80ff80",
            "17": "#66ff66",
            "19": "#4dff4d",
            "20": "#33ff33",
            "2": "#1aff1a",
            "4": "#00ff00",
            "8": "#00e600",
            "9": "#00cc00"
        }

        Criticality = {
            "High": "#b72a35",
            "Medium": "#f0ae0c",
            "Low": "#25ba3c"
        }

        if filter == 'Entity':
            return random.choice(list(Entity.values()))
        elif filter == 'Location':
            return random.choice(list(Location.values()))
        elif filter == 'Assets':
            return random.choice(list(Assets.values()))
        elif filter == 'UseCase':
            return random.choice(list(UseCase.values()))
        elif filter == 'Function':
            return random.choice(list(Function.values()))
        elif filter == 'Criticality' or filter == 'Severity':
            return Criticality.get(id)
