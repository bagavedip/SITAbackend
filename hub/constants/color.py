class ColorMap:

    @staticmethod
    def get_color(filter, id):
        Entity = {
            "1": "#38392D",
            "10": "#D1D2C6",
            "11": "#ACAE98",
            "3": "#3c400d",
            "4": "#848947",
            "5": "#dae90d",
            "6": "#d2d78f",
            "7": "#202206",
            "8": "#757c29",
            "9": "#a8af61"
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
            return Entity.get(id)
        elif filter == 'Location':
            return Location.get(id)
        elif filter == 'Assets':
            return Assets.get(id)
        elif filter == 'UseCase':
            return UseCase.get(id)
        elif filter == 'Criticality' or filter == 'Severity':
            return Criticality.get(id)
