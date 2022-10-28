import json
from tube.components import *


class TubeMap:
    """
    Task 1: Complete the definition of the TubeMap class by:
    - completing the "import_from_json()" method

    Don't hesitate to divide your code into several sub-methods, if needed.

    As a minimum, the TubeMap class must contain these three member attributes:
    - stations: a dictionary that indexes Station instances by their id (key=id (str), value=Station)
    - lines: a dictionary that indexes Line instances by their id (key=id, value=Line)
    - connections: a list of Connection instances for the TubeMap (list of Connections)
    """

    def __init__(self):
        self.stations = {}  # key: id (str), value: Station instance
        self.lines = {}  # key: id (str), value: Line instance
        self.connections = []  # list of Connection instances
        self.validity = True


    def import_from_json(self, filepath):
        """ Import tube map information from a JSON file.
        
        During the import process, the `stations`, `lines` and `connections` attributes should be updated.

        You can use the `json` python package to easily load the JSON file at `filepath`

        Note: when the indicated zone is not an integer (for instance: "2.5"), 
            it means that the station belongs to two zones. 
            For example, if the zone of a station is "2.5", 
            it means that the station is in both zones 2 and 3.

        Args:
            filepath (str) : relative or absolute path to the JSON file 
                containing all the information about the tube map graph to 
                import. If filepath is invalid, no attribute should be updated, 
                and no error should be raised.
        """

        # Verifies the filepath argument is valid, raises a custom FileNotFoundError otherwise
        try:
            with open(filepath, "r") as jsonfile:
                data = json.load(jsonfile)
        except FileNotFoundError:
            self.validity = False
            return None

        connections = data['connections']
        lines = data['lines']
        stations = data['stations']

        try:
            # Sets up the self.stations dictionary composed of items with:
            #       key (str) : id
            #       value (Station) : Station object corresponding to the id
            for index in range(len(stations)):
                self.add_station_to_dict(stations, index)

            # Sets up the self.lines dictionary composed of items with:
            #       key (str) : id
            #       value (Line) : Line object corresponding to the id
            for index in range(len(lines)):
                self.add_line_to_dict(lines, index)

            # Sets up the self.connections list composed of Connection objects
            for index in range(len(connections)):
                self.add_connection_to_list(connections, index)
        except AssertionError and KeyError:
            return None

    def add_line_to_dict(self, lines, index):
        """ Adds a Line object to the dict self.lines

        Args:
            lines (list) : contains all the lines there exist
            index (int) : the index of the stations to add to the self.lines dict
        """

        identity = lines[index]['line']
        name = lines[index]['name']

        if not(type(identity) == str):
            identity = f"{identity}"

        assert (type(identity) == str and
                type(name) == str), "Wrong data types for the Line class"

        self.lines[identity] = Line(identity, name)

    def add_station_to_dict(self, stations, index):
        """ Adds a Station object to the dict self.stations

        Args:
            stations (list) : contains all the stations there exist
            index (int) : the index of the stations to add to the self.stations dict
        """

        identity = stations[index]['id']
        name = stations[index]['name']
        zones = stations[index]['zone'].split(".")

        # A station can be a part of multiple zones, this is treated below
        if len(zones) > 1:
            if len(zones) == 2:
                zones = {int(zones[0]), int(int(zones[0]) + 1)}
            else:
                return None
        else:
            assert type(zones[0]) == str or type(zones[0]) == int, f"zones[0] is not a string or an int: {zones[0]}"
            if type(zones) == int:
                zones = {zones}
            else:
                zones = {int(zones[0])}

        if type(zones) == list:
            zones = set(zones)

        # Want our function to work despite zone inside zones being a str instead of an int
        check_inside_zones_str = [type(zone) == str for zone in zones]  # Checks if there are 'str' in zones
        condition_str = False not in check_inside_zones_str

        if condition_str:
            new_zones = set()
            for zone in zones:
                new_zones.add(int(zone))
            zones = new_zones

        check_inside_zones_int = [type(zone) == int for zone in zones]  # Checks there are only 'int' in zones now
        condition_int = False not in check_inside_zones_int  # True if and only if there are only 'int' in zones

        assert (type(identity) == str and
                type(name) == str and
                type(zones) == set and
                condition_int), "Wrong data type for the Station class"

        self.stations[identity] = Station(identity, name, zones)

    def add_connection_to_list(self, connections, index):
        """ Adds a Connection object to the list self.connections

        Args:
            connections (list) : contains all the connections there exist between stations
            index (int) : the index of the connection to add to the self.connections list
        """

        if not(len(connections[index]) <= 4):
            return None
        try:
            id_station1 = connections[index]['station1']
            id_station2 = connections[index]['station2']
        except KeyError:
            return None

        # Connection object needs 3 attributes: stations, line and time; these are gathered below
        stations = {self.stations[id_station1], self.stations[id_station2]}
        id_line = connections[index]['line']
        line = self.lines[id_line]

        time = int(connections[index]['time'])

        self.connections.append(Connection(stations, line, time))


def test_import():
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")

    # view one example Station
    print(tubemap.stations[list(tubemap.stations)[0]])

    # view one example Line
    print(tubemap.lines[list(tubemap.lines)[0]])

    # view the first Connection
    print(tubemap.connections[0])

    # view stations for the first Connection
    print([station for station in tubemap.connections[0].stations])

    print(tubemap.connections)


if __name__ == "__main__":
    test_import()
