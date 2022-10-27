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
            assert type(filepath) == str, f"filepath argument should be a string, not a {type(filepath)}"
            with open(filepath, "r") as jsonfile:
                data = json.load(jsonfile)
        except FileNotFoundError:
            raise FileNotFoundError("Filepath is invalid, please verify the str")

        connections = data['connections']
        lines = data['lines']
        stations = data['stations']

        # Sets up the self.stations dictionary composed of items with:
        #       key (str) : id
        #       value (Station) : Station object corresponding to the id
        for index in range(len(stations)):

            identity = stations[index]['id']
            name = stations[index]['name']
            zones = stations[index]['zone'].split(".")

            # A station can be a part of multiple zones, this is treated below
            if len(zones) > 1:
                zones = {int(zones[0]), int(int(zones[0]) + 1)}
            else:
                assert type(zones[0]) == str, f"zones[0] is not a string: {zones[0]}"
                if type(zones) == int:
                    zones = {zones}
                else:
                    zones = {int(zones[0])}

            assert type(zones) == set and len(
                zones) <= 2, "zones must be a set and contain no more than 2 stations"

            check_inside_zones = [type(inside) == int for inside in zones]  # Checks there are only 'int' in zones
            condition_int = False not in check_inside_zones  # True if and only if there are only 'int' in zones

            assert (type(identity) == str and
                    type(name) == str and
                    type(zones) == set and
                    condition_int), "Wrong data type for the Station class"

            self.stations[identity] = Station(identity, name, zones)

        # Sets up the self.lines dictionary composed of items with:
        #       key (str) : id
        #       value (Line) : Line object corresponding to the id
        for index in range(len(lines)):
            identity = lines[index]['line']
            name = lines[index]['name']

            assert (type(identity) == str and
                    type(name) == str), "Wrong data types for the Line class"
            self.lines[identity] = Line(identity, name)

        # Sets up the self.connections list composed of Connection objects
        for index in range(len(connections)):

            assert len(connections[index]) <= 4, 'More keys than expected in the connections data dict'
            try:
                id_station1 = connections[index]['station1']
                id_station2 = connections[index]['station2']
            except KeyError:
                raise KeyError("Unexpected keys inside the connections data dict")

            # Connection object needs 3 attributes: stations, line and time; these are gathered below
            stations = {self.stations[id_station1], self.stations[id_station2]}
            id_line = connections[index]['line']
            line = self.lines[id_line]

            assert type(connections[index]['time']) == str, "Unexpected data type inside the connections dictionary"
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
