class ColorMap:

    @staticmethod
    def get_color(filter, id):
        SLA = {
            "Alta": "#1a47ba",
            "Baja": "#fcba03",
            "Media": "#9da3b3",
        }

        value0 = {
            "0": "#FF0000",
            "1": "#0000FF",
        }

        Category = {
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
            "9": "#27cc48",
            "0": "#27cc48"
        }

        status = {
            "open": "#1a47ba",
            "backlog": "#fcba03",
        }

        Priority = {
            "High": "#1a47ba",
            "Low": "#fcba03",
            "Medium": "#9da3b3"
        }

        if filter == 'SLA':
            return SLA.get(id)
        elif filter == 'value0':
            return value0.get(id)
        elif filter == 'status':
            return status.get(id)
        elif filter == 'Priority':
            return Priority.get(id)
        elif filter == 'Category':
            return Category.get(id)

