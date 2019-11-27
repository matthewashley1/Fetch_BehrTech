from datetime import datetime
import json
import os


class Parser:
    """
    Is the base class for breaking data returned from a gateway computer from BehrTech into usable components. Provides
    stander functions that apply to all sensor types connected to a gateway computer from BehrTech.
    """

    def __init__(self):
        self.data = None

    def set_data_message(self, message):
        """
        Sets the data of the class from the message query of the gateway computer

        :param message: Is the data returned from querying the gateway computer
        """
        self.data = message

    def set_data_file(self, file_path):
        """
        Sets the data of the class loaded from a file

        :param file_path: Is the file to load data from
        """

        if os.path.exists(file_path):
            with open(file_path, "r") as file_read:
                self.data = file_read.read()

        else:
            print("Provided file path doesn't exits, pass in an absolute file path")

    def get_data(self):
        """
        Returns the data of the class

        :return: The data of the class
        """
        return self.data

    def write_data_to_file(self, file_name: str):
        """
        Outputs the data of the class to a JSON file

        :param file_name: The name of the file for the data of the class to be outputted to
        """

        text_file = open("Outputs/" + file_name + ".json", "w")
        text_file.write(self.data)

        text_file.close()

    def get_message_data(self):
        """
        Sources all the data of the class to retrieve all sensor data for each message including a time stamp and
        sensor ID

        :return: All sensor data for each message as a list
        """

        user_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check = x.get("userDataJSON")

                if check:
                    data = json.loads(check)

                    if "message" not in data.keys():
                        data["time"] = x.get("time")
                        data["sensorID"] = x.get("epEui")
                        user_data.append(data)

        return user_data

    def get_message_datetime_as_str(self):
        """
        Sources all the data of the class to retrieve the time stamp for each message

        :return: The time stamp of each message as a list broken into individual dicts and separated as date and time
        """

        time_info = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                time = x.get("time")

                if time:
                    time_split = time.strip("Z").split("T")
                    time_info.append({"date": time_split[0], "time": time_split[1]})

        return time_info

    def get_message_datetime_as_datetime(self):
        """
        Sources all the data of the class to retrieve the time stamp for each message

        :return: The time stamp of each message as a list formatted as a datetime
        """

        time_info = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                time = x.get("time")

                if time:
                    time_split = time.strip("Z").split("T")
                    new_time = f"{time_split[0]} {time_split[1]}"
                    time_info.append(datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S'))

        return time_info

    def get_message_data_in_date_range(self, start: datetime, end: datetime):
        """
        Sources all the data of the class to retrieve all sensor data for a message including a time stamp and
        sensor ID that is within the specified date range

        :param start: Lowest date of date range
        :param end: Highest date of date range
        :return: All sensor data for each message as a list
        """

        user_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                time = x.get("time")

                if time:
                    time_split = time.strip("Z").split("T")
                    new_time = f"{time_split[0]} {time_split[1]}"

                    message_time = datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S')

                    if start <= message_time <= end:
                        check = x.get("userDataJSON")

                        if check:
                            data = json.loads(check)

                            if "message" not in data.keys():
                                data["time"] = x.get("time")
                                data["sensorID"] = x.get("epEui")
                                user_data.append(data)

                    elif message_time < start:
                        break

        return user_data

    def get_date_ranges(self):
        """
        Sources all the data of the class to retrieve the date range of the data of the class

        :return: The date range of the data of the class as a dict
        """

        time = self.get_message_datetime_as_str()

        return {"Recent": time[0]["date"], "Oldest": time[-1]["date"]}

    def get_message_id(self):
        """
        Sources all the data of the class to retrieve the id for each message

        :return: The id of each message as a list
        """

        ids = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check = x.get("_id")

                if check:
                    ids.append(check)

        return ids

    def get_message_data_for_id(self, id_number):
        """
        Sources all the data of the class to retrieve all sensor data for a message including a time stamp and
        sensor ID that matches the requested id number

        :param id_number: The id number of the message that data is being requested for
        :return: The data of the message requested for as a dictionary
        """

        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check_id = x.get("_id")

                if check_id:
                    if check_id == id_number:

                        check_data = x.get("userDataJSON")

                        if check_data:
                            data = json.loads(check_data)

                            if "message" not in data.keys():
                                data["time"] = x.get("time")
                                data["sensorID"] = x.get("epEui")
                                return data