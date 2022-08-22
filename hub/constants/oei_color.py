class ColorMap:

    @staticmethod
    def get_color(filter, id):
        SLA = {
            "Alta": "#165B65",
            "Baja": "#16293A",
            "Media": "#437DB1",
        }

        value0 = {
            "0": "#B72A35",
            "1": "#1DBC36",
        }

        Category = {
            "1": "#2CB6C9",
            "10": "#54CADA",
            "11": "#2498AB",
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
            "open": "#9DBD6F",
            "backlog": "#6E9537",
        }

        Priority = {
            "High": "#B72A35",
            "Low": "#1DBC36",
            "Medium": "#F0AE0c"
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

