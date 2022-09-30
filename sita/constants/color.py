class ColorMap:

    @staticmethod
    def get_color(filter, id):
        Entity = {
            "1": "#1a47ba",
            "10": "#fcba03",
            "2": "#1a47ba",
            "3": "#c9bfa1",
            "4": "#182526",
            "5": "#595446",
            "6": "#27cc48",
            "7": "#9da3b3",
            "8": "#64adb5",
            "9": "#db3716"
        }

        Location = {
            "1": "#fcba03",
            "10": "#db3716",
            "2": "#595446",
            "3": "#c9bfa1",
            "4": "#64adb5",
            "5": "#182526",
            "6": "#1a47ba",
            "7": "#1a47ba",
            "8": "#9da3b3",
            "9": "#27cc48"
        }
        
        Assets = {
            "1": "#1a47ba",
            "10": "#fcba03",
            "11": "#9da3b3",
            "12": "#64adb5",
            "13": "#595446",
            "2": "#1a47ba",
            "3": "#c9bfa1",
            "4": "#64adb5",
            "5": "#182526",
            "6": "#1a47ba",
            "7": "#1a47ba",
            "8": "#9da3b3",
            "9": "#27cc48"
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
            "High": "red",
            "Medium": "yellow",
            "Low": "green"
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
