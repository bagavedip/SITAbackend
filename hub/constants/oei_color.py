class ColorMap:

    @staticmethod
    def get_color(filter, id):
        SLA = {
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

        value0 = {
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
            "9": "#27cc48"
        }

        status = {
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

        Priority = {
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

