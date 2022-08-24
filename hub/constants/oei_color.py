import random

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

        Tickets = {
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

        Status = {
            "open": "#9DBD6F",
            "backlog": "#6E9537",
        }

        Priority = {
            "High": "#B72A35",
            "Low": "#1DBC36",
            "Medium": "#F0AE0c"
        }
        First_Response_Time = {
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

        Response_Time = {
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

        False_Positives = {
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

        Reopened = {
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

        value1 = {
            "0": "#B72A35",
            "1": "#1DBC36",
        }

        value2 = {
            "0": "#B72A35",
            "1": "#1DBC36",
        }

        value3 = {
            "0": "#B72A35",
            "1": "#1DBC36",
        }

        if filter == 'SLA':
            return SLA.get(id)
        elif filter == 'value0':
            return value0.get(id)
        elif filter == 'value1':
            return value1.get(id)
        elif filter == 'value2':
            return value2.get(id)
        elif filter == 'value3':
            return value3.get(id)
        elif filter == 'Status':
            return Status.get(id)
        elif filter == 'Priority':
            return Priority.get(id)
        elif filter == 'Category':
            return random.choice(list(Category.values()))
        elif filter == 'Tickets':
            return random.choice(list(Tickets.values()))
        elif filter == 'False_Positives':
            return random.choice(list(False_Positives.values()))
        elif filter == 'First_Response_Time':
            return random.choice(list(First_Response_Time.values()))
        elif filter == 'Response_Time':
            return random.choice(list(Response_Time.values()))
        elif filter == 'Reopened':
            return random.choice(list(Reopened.values()))


