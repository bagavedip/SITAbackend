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
            "1": "#1a47ba",
            "12": "#fcba03",
            "13": "#9da3b3",
            "15": "#64adb5",
            "16": "#595446",
            "17": "#1a47ba",
            "19": "#27cc48",
            "20": "#595446",
            "2": "#1a47ba",
            "4": "#64adb5",
            "8": "#9da3b3",
            "9": "#27cc48"
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
        elif filter == 'Criticality' or filter == 'Severity':
            return Criticality.get(id)
