from tube.map import TubeMap

class NeighbourGraphBuilder:
    """
    Task 2: Complete the definition of the NeighbourGraphBuilder class by:
    - completing the "build" method below (don't hesitate to divide your code into several sub-methods, if needed)
    """

    def __init__(self):
        pass

    def build(self, tubemap):
        """ Builds a graph encoding neighbouring connections between stations.

        ----------------------------------------------

        The returned graph should be a dictionary having the following form:
        {
            "station_A_id": {
                "neighbour_station_1_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],

                "neighbour_station_2_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],
                ...
            }

            "station_B_id": {
                ...
            }

            ...

        }

        ----------------------------------------------

        For instance, knowing that the id of "Hammersmith" station is "110",
        graph['110'] should be equal to:
        {
            '17': [
                Connection(Hammersmith<->Barons Court, District Line, 1),
                Connection(Hammersmith<->Barons Court, Piccadilly Line, 2)
                ],

            '209': [
                Connection(Hammersmith<->Ravenscourt Park, District Line, 2)
                ],

            '101': [
                Connection(Goldhawk Road<->Hammersmith, Hammersmith & City Line, 2)
                ],

            '265': [
                Connection(Hammersmith<->Turnham Green, Piccadilly Line, 2)
                ]
        }

        ----------------------------------------------

        Args:
            tubemap (TubeMap) : tube map serving as a reference for building 
                the graph.

        Returns:
            nested_dict (dict) : as described above.
                If the input data (tubemap) is invalid, 
                the method should return an empty dict.
        """

        nested_dict = {}

        # Initiates nested_dict
        if not(isinstance(tubemap, TubeMap)):
            pass
        else:
            for station_obj in tubemap.stations:
                nested_dict[station_obj] = {}

            # Fill in the value with Connections object for each station
            for station in nested_dict:
                connections_with_station = self.get_connections_with_station(station, tubemap)
                for connection_obj in connections_with_station:
                    station_obj = tubemap.stations[station]
                    self.add_connection_to_nested_dict(nested_dict, station_obj, connection_obj)

        return nested_dict

    def get_connections_with_station(self, station, tubemap):
        """ Searches for all Connection objects that include the station 'station' and creates a list of them
        Args:
            station (str) : ID of the station we want the connections of
            tubemap (TubeMap) : tube map serving as a reference for building the graph.
        Returns:
            connection_obj_list (list) : List of the Connection objects that include the station given as input
        """

        connection_obj_list = []

        for connection_obj in tubemap.connections:
            station_obj = tubemap.stations[station]
            if station_obj in connection_obj.stations:
                connection_obj_list.append(connection_obj)

        return connection_obj_list

    def add_connection_to_nested_dict(self, nested_dict, station_a_obj, connection_obj):
        """ Completes the nested_dict with a new connection inside the dictionary corresponding to 'station_a_obj'.

        In effect, this means the item (station_b: [Connection]) is added to the dict value of the key
        'station_a_obj.id' with the latter being the id of station_a (when a connection with station_b was already
        present, it will append the list)

        ----------------------------------------------

        Hence, when station_b was not already in the dictionary, we should return:

        {
            "station_a_obj.id": {
                "station_b_obj.id": [
                                connection_obj (instance of Connection),
                                ],
                ...
            }
            ...
        }

        And when station_b was already present, a new Connection instance is appended to the list:

        {
            "station_a_obj.id": {
                "station_b_obj.id": [
                                connection_obj_old (instance of Connection),
                                connection_obj (instance of Connection)
                                ],
                ...
            }
            ...
        }

        ----------------------------------------------

        Args:
            nested_dict (dict) : dict graph encoding neighbouring connections between stations
            station_a_obj (Station) : Station object we want to add the Connection object for in the nested_dict
            connection_obj (Connection) : Connection object we want to add to the nested_dict
        """

        for station_b_obj in connection_obj.stations:
            if station_b_obj != station_a_obj:
                if station_b_obj.id not in nested_dict[station_a_obj.id].keys():
                    nested_dict[station_a_obj.id][station_b_obj.id] = [connection_obj]
                else:
                    nested_dict[station_a_obj.id][station_b_obj.id].append(connection_obj)


def test_graph():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")

    graph_builder = NeighbourGraphBuilder()
    graph = graph_builder.build(tubemap)

    print(graph['110'])

    print(graph)


if __name__ == "__main__":
    test_graph()
