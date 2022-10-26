from network.graph import NeighbourGraphBuilder
import math


class PathFinder:
    """
    Task 3: Complete the definition of the PathFinder class by:
    - completing the definition of the __init__() method (if needed)
    - completing the "get_shortest_path()" method (don't hesitate to divide your code into several sub-methods)
    """

    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap

        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)

        # Feel free to add anything else needed here.

    def get_shortest_path(self, start_station_name, end_station_name):
        """ Find ONE shortest path (in terms of duration) from start_station_name to end_station_name.

        For instance, get_shortest_path('Stockwell', 'South Kensington') should return the list:
        [Station(245, Stockwell, {2}), 
         Station(272, Vauxhall, {1, 2}), 
         Station(198, Pimlico, {1}), 
         Station(273, Victoria, {1}),
         Station(229, Sloane Square, {1}), 
         Station(236, South Kensington, {1})
        ]

        If start_station_name or end_station_name does not exist, return None.

        You can use the Dijkstra algorithm to find the shortest path from start_station_name to end_station_name.

        Find a tutorial on YouTube to understand how the algorithm works, e.g. https://www.youtube.com/watch?v=GazC3A4OQTE
        
        Alternatively, find the pseudocode on Wikipedia: https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            path (list) : list of Station objects corresponding to ONE
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not exist.
        """

        # Initialization
        graph_builder = NeighbourGraphBuilder()
        graph = graph_builder.build(self.tubemap)

        try:
            start_station_id = self.get_id(start_station_name)
            start_station_obj = self.tubemap.stations[start_station_id]
            end_station_id = self.get_id(end_station_name)
            end_station_obj = self.tubemap.stations[end_station_id]
        except AssertionError:
            return None

        unvisited_stations = set(self.tubemap.stations.keys())

        path_dict = {}  # keeps a history of the connection leading to the station which was found most effective
        tentative_distance = {}  # keeps a count of the 'distance' each station represents from the starting station

        # Set up the appropriate nested dictionary structure to path_dict and tentative_distance:
        #   - Initialize the tentative_distance values as infinite values
        #       for all stations except the starting one which should be 0
        #   - Initialize the path_dict values as None no matter the station
        for station in unvisited_stations:

            if station == start_station_obj.id:
                tentative_distance[station] = 0
                name_station = self.get_name(station)
                path_dict[name_station] = None

            else:
                tentative_distance[station] = math.inf
                name_station = self.get_name(station)
                path_dict[name_station] = None

        # Starting Dijkstra's algorithm to find the shortest path (exhaustive comments here)
        while len(unvisited_stations) > 0:

            # 'current station' must be the station with the lowest distance
            current_station = self.get_lowest_value_station(unvisited_stations,
                                                            tentative_distance)

            # Make sure we do not visit twice this station
            unvisited_stations.remove(current_station)

            # Visits each neighbour of the current station (or node)
            for neighbour in graph[current_station]:

                # Makes sure the neighbour station has not been visited yet
                if neighbour not in unvisited_stations:
                    continue
                else:

                    # Looks for the best connection between the current station and the neighbour
                    alt, connection_used = self.get_distance(graph, tentative_distance, current_station, neighbour)

                    # Looks if the way we normally reach this neighbour is
                    # faster or not than through our current station
                    self.is_better(path_dict, tentative_distance, neighbour, alt, current_station, connection_used)

        # Process path_dict to get the actual, readable result
        path = []

        current_station = end_station_name
        path.append(end_station_obj)
        while current_station != start_station_name:
            previous_station = path_dict[current_station][0]
            path.append(self.get_object(previous_station))
            if current_station == start_station_name:
                break
            else:
                current_station = path_dict[current_station][0]

        path.reverse()

        return path

    def is_better(self, path_dict, tentative_distance, neighbour, alt, current_station, connection_used):
        """Looks if the new alternative distance found to reach the neighbour station is better than then our previous
            attempts. If so, it updates the path_dict nested dictionary to include this new, improved, solution.
            If not, then it leaves it unchanged.

        Args:
            path_dict (dict) : keeps a history of the connection leading to the station which was found most effective
            tentative_distance (dict) : keeps a count of the 'distance' each station represents from the starting
                station
            neighbour (Station) : the Station object we want to evaluate the new distance
            alt (int) : the new 'distance' from the starting station reached via the current station
            current_station (Station) : the Station object we are visiting in Dijkstra's algorithm
            connection_used (Connection) :  the Connection object linking the current_station and the neighbour
        """

        if tentative_distance[neighbour] > alt:
            tentative_distance[neighbour] = alt

            name_neigh = self.get_name(neighbour)
            name_current = self.get_name(current_station)
            path_dict[name_neigh] = [name_current,
                                     connection_used]
        else:
            pass

    def get_distance(self, graph, tentative_distance, current_station, neighbour):
        """ Computes the new alternative distance between the neighbour Station and the start station passing through
                the current station. In cases where there are multiple Connections between the neighbour Station and the
                current Station, we have to consider the best Connection in terms of time. This leads to the for loop.

        Arg:
            graph (dict) : nested dictionary encoding neighbouring connections between stations
            tentative_distance (dict) : keeps a count of the 'distance' each station represents from the starting
                station
            neighbour (Station) : the Station object we want to evaluate the new distance
            current_station (Station) : the Station object we are visiting in Dijkstra's algorithm

        Returns:
            alt (int) : time corresponding to the alternative path
            connection_used (Connection) : connection used for the new path
        """

        alt = math.inf
        for connection_obj in graph[current_station][neighbour]:
            assert tentative_distance[current_station] < math.inf, "Distance of current " \
                                                                   "station marked as infinity"
            new_alt = tentative_distance[current_station] + connection_obj.time
            if alt > new_alt:
                alt = new_alt
                connection_used = connection_obj
            else:
                continue

        return alt, connection_used

    def get_neighbours(self, station_id):
        """Gathers all the neighbouring stations for a given station ID

        Args:
            station_id (str) : id of the station

        Returns:
            neigh (list) : list of the IDs of the corresponding neighbours
        """

        neigh = []
        station_obj = self.tubemap.stations[station_id]

        for connection in self.tubemap.connections:
            if station_obj in connection.stations:
                for neighbouring_station_obj in connection.stations:
                    if neighbouring_station_obj != station_obj and neighbouring_station_obj.id not in neigh:
                        neigh.append(neighbouring_station_obj.id)
                    else:
                        continue
            else:
                continue

        return neigh

    def get_id(self, station_name_given):
        """ Find the ID of a station given its name

        Args:
            station_name_given (str) : name of the station

        Returns:
            index (str) : Corresponding id of the station
        """

        assert type(station_name_given) == str, "Wrong input type for get_id function: station name must be a str"

        index = None
        for station in self.tubemap.stations:
            station_obj = self.tubemap.stations[station]
            if station_obj.name == station_name_given:
                index = station_obj.id
                break
            else:
                continue
        assert index is not None, "Station name has not been found"
        return index

    def get_name(self, station_id_given):
        """ Find the name of a station given its ID
        Args:
            station_id_given (str) : ID of the station

        Returns:
            name (str) : Corresponding name of the station
        """

        assert type(station_id_given) == str, "Wrong input type for get_name function: station id must be a str"

        name = None
        for station in self.tubemap.stations:
            station_obj = self.tubemap.stations[station]
            if station_obj.id == station_id_given:
                name = station_obj.name
                break
            else:
                continue

        assert name is not None, "ID given has not been found"

        return name

    def get_object(self, station_name_given):
        """ Find the Station object of a station given its ID
        Args:
            station_name_given (str) : name of the station

        Returns:
            object (Station) : Corresponding object of the station
        """

        assert type(station_name_given) == str, "Wrong input type for get_object function: " \
                                                "station_name_given must be a str"

        obj = None
        for station in self.tubemap.stations:
            station_obj = self.tubemap.stations[station]
            if station_obj.name == station_name_given:
                obj = station_obj
                break
            else:
                continue

        return obj

    def get_lowest_value_station(self, unvisited_stations, tentative_distance):
        """ Find the name of a station given its ID

        Args:
            unvisited_stations (set) : set of ID (str) of the stations that have not been visited yet
            tentative_distance (dict) : dict of the distances of each station, which is constantly updating

        Returns:
            lowest_value_station_id (str) : ID of the station with the lowest distance in values
                of the tentative_distance dict
        """

        assert type(unvisited_stations) == set, "Wrong input type for get_lowest_value_station function: " \
                                                "unvisited_stations must be a list"
        assert type(tentative_distance) == dict, "Wrong input type for get_lowest_value_station: " \
                                                 "tentative_distance must be a dict"

        possible_stations_to_choose_from = {}
        for unvisited_station in unvisited_stations:
            possible_stations_to_choose_from[unvisited_station] = tentative_distance[unvisited_station]

        lowest_value_station_id = min(possible_stations_to_choose_from,
                                      key=possible_stations_to_choose_from.get)

        return lowest_value_station_id


def test_shortest_path():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")

    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")

    station_names = [station.name for station in stations]
    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus",
                "Green Park"]
    assert station_names == expected

if __name__ == "__main__":
    test_shortest_path()
