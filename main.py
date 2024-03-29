from network.path import PathFinder
from tube.map import TubeMap


def get_tubemap():
    """ Return an initialised TubeMap object

    Returns:
        tube.map.TubeMap: Initialised TubeMap object
    """
    tubemap = TubeMap()

    try:
        tubemap.import_from_json("data/london.json")
    except NameError:
        tubemap.validity = False
        return None

    return tubemap


def main():
    tubemap = get_tubemap()

    path_finder = PathFinder(tubemap)

    # Examples usage of path_finder
    stations = path_finder.get_shortest_path('South Kensington', 'Bond Street')

    # Avoid an error message in the case when the station name given was invalid
    if stations is not None:
        station_names = [station.name for station in stations]
        print(station_names)
    else:
        print(stations)


if __name__ == '__main__':
    main()
