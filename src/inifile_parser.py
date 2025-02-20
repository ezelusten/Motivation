"""
Parse json file and extract configs
Module is also used for testing
"""

import json
import sys
from typing import Dict, List, Optional, Tuple, TypeAlias, Any

import jsonschema
import shapely

Point: TypeAlias = Tuple[float, float]


def parse_destinations(json_data: Dict[str, Any]) -> Dict[int, List[List[Point]]]:
    """
    Parses the 'destinations' object from a JSON string into a Python dictionary.

    Args:
        json_data: A dict containing JSON data with a 'destinations' object.

    Returns:
        A dictionary with the parsed 'destinations' object. The dictionary maps
        IDs (int) to lists of polygons, where each polygon is a list of (x, y) tuples.
    """

    _destinations = {}
    for destination in json_data["destinations"]:
        id_str = destination["id"]
        dest_list = destination["vertices"]
        _destinations[int(id_str)] = dest_list

    return _destinations


def parse_velocity_model_parameter_profiles(
    json_data: Dict[str, Any]
) -> Dict[int, List[float]]:
    """
    Parse the 'velocity_model_parameter_profiles' object
    from a JSON string into a Python dictionary.

    Args:
        json_data: A dict containing JSON data with a
                   'velocity_model_parameter_profiles' object.

    Returns:
        A dictionary with the parsed 'velocity_model_parameter_profiles' object. The dictionary maps
        ID (int) to lists of floating-point numbers.
    """

    _profiles: Dict[int, List[float]] = {}
    for profile in json_data["velocity_model_parameter_profiles"]:
        id_str = profile["id"]
        time_gap = profile["time_gap"]
        tau = profile["tau"]
        v_0 = profile["v0"]
        radius = profile["radius"]
        _profiles[int(id_str)] = [time_gap, tau, v_0, radius]
    return _profiles


def parse_way_points(
    json_data: Dict[str, Any],
) -> List[Tuple[Point, float]]:
    """
    Parses the 'way_points' object from a JSON string into a Python dictionary.

    Args:
        json_data: A dict containing JSON data with a 'way_points' object.

    Returns:
        A dictionary with the parsed 'way_points' object. The dictionary maps
        ID (int) to lists of tuples, where each tuple contains a (x, y) point
        and a floating-point number representing a distance.
    """

    _way_points: List[Tuple[Point, float]] = []
    for _, way_point in enumerate(json_data["way_points"]):
        coordinates = way_point["coordinates"]
        if len(coordinates) != 2:
            raise ValueError(f"Invalid coordinates: {coordinates}")

        point: Point = (float(coordinates[0]), float(coordinates[1]))
        distance = float(way_point["distance"])
        wp_list = (point, distance)
        # wp_list = (
        #     tuple(way_point["coordinates"]),
        #     way_point["distance"],
        # )
        _way_points.append(wp_list)
    return _way_points


def parse_distribution_polygons(
    json_data: Dict[str, Any],
) -> Dict[int, shapely.Polygon]:
    """
    Parses the 'distribution_polygons' object from a JSON string into a Python dictionary.

    Args:
        json_data: A dict containing JSON data with a 'distribution_polygons' object.

    Returns:
        A dictionary with the parsed 'distribution_polygons' object. The dictionary maps
        ID (int) to lists of polygons, where each polygon is a list of (x, y) tuples.
    """
    _distribution_polygons: Dict[int, shapely.Polygon] = {}
    for id_polygon in json_data["distribution_polygons"]:
        id_str = id_polygon["id"]
        polygon = id_polygon["vertices"]
        _distribution_polygons[int(id_str)] = shapely.Polygon(polygon)

    return _distribution_polygons


def parse_motivation_doors(json_data: Dict[str, Any]) -> Dict[int, List[List[float]]]:
    """
    Parses a JSON string containing information about doors, around which people get motivated. Returns a dictionary
    mapping area IDs to a list of coordinates that define the doors.

    :param json_str: A JSON string containing information about accessible areas.
    :return: A dictionary mapping area IDs to a list of coordinates that define the doors.
    """

    _doors: Dict[int, List[List[float]]] = {}

    if (
        "motivation_parameters" in json_data
        and "motivation_doors" in json_data["motivation_parameters"]
    ):
        doors_dict = json_data["motivation_parameters"]["motivation_doors"]

        for area_id, coordinates_list in enumerate(doors_dict):
            _doors[int(area_id)] = coordinates_list["vertices"]

    return _doors


def parse_accessible_areas(json_data: Dict[str, Any]) -> Dict[int, List[List[float]]]:
    """
    Parses a JSON string containing information about accessible areas and returns a dictionary
    mapping area IDs to a list of coordinates that define the area.

    :param json_str: A JSON string containing information about accessible areas.
    :return: A dictionary mapping area IDs to a list of coordinates that define the area.
    """

    _areas = {}
    areas_dict = json_data["accessible_areas"]

    # Iterate through the accessible areas dictionary and extract the coordinates for each area
    for area_id, coordinates_list in enumerate(areas_dict):
        _areas[int(area_id)] = coordinates_list["vertices"]

    return _areas


def parse_fps(json_data: Dict[str, Any]) -> Optional[int]:
    """Get fps if found in file, otherwise None"""

    if (
        "simulation_parameters" in json_data
        and "fps" in json_data["simulation_parameters"]
    ):
        return int(json_data["simulation_parameters"]["fps"])

    return None


def parse_grid_min_v0(json_data: Dict[str, Any]) -> float:
    """Get min v0 for grid"""

    if "grid_parameters" in json_data and "min_v_0" in json_data["grid_parameters"]:
        return float(json_data["grid_parameters"]["min_v_0"])

    return 1


def parse_grid_max_v0(json_data: Dict[str, Any]) -> float:
    """Get max v0 for grid"""

    if "grid_parameters" in json_data and "max_v_0" in json_data["grid_parameters"]:
        return float(json_data["grid_parameters"]["max_v_0"])

    return 2


def parse_grid_step_v0(json_data: Dict[str, Any]) -> float:
    """Get step for v0  grid"""

    if "grid_parameters" in json_data and "v_0_step" in json_data["grid_parameters"]:
        return float(json_data["grid_parameters"]["v_0_step"])

    return 2


def parse_grid_min_time_gap(json_data: Dict[str, Any]) -> float:
    """Get min time_gap for grid"""

    if (
        "grid_parameters" in json_data
        and "min_time_gap" in json_data["grid_parameters"]
    ):
        return float(json_data["grid_parameters"]["min_time_gap"])

    return 1


def parse_grid_max_time_gap(json_data: Dict[str, Any]) -> float:
    """Get max time_gap for grid"""

    if (
        "grid_parameters" in json_data
        and "max_time_gap" in json_data["grid_parameters"]
    ):
        return float(json_data["grid_parameters"]["max_time_gap"])

    return 2


def parse_grid_time_gap_step(json_data: Dict[str, Any]) -> float:
    """Get step for time_gap  grid"""

    if (
        "grid_parameters" in json_data
        and "time_gap_step" in json_data["grid_parameters"]
    ):
        return float(json_data["grid_parameters"]["time_gap_step"])

    return 0.1


def parse_number_agents(json_data: Dict[str, Any]) -> int:
    """Get number_agents if found in file, otherwise 1"""

    if (
        "simulation_parameters" in json_data
        and "number_agents" in json_data["simulation_parameters"]
    ):
        return int(json_data["simulation_parameters"]["number_agents"])

    return 0


def parse_time_step(json_data: Dict[str, Any]) -> Optional[float]:
    """Get time_step if found, otherwise None"""

    if (
        "simulation_parameters" in json_data
        and "time_step" in json_data["simulation_parameters"]
    ):
        return float(json_data["simulation_parameters"]["time_step"])

    return None


def parse_simulation_time(json_data: Dict[str, Any]) -> Optional[int]:
    """Get simulation if found, otherwise None"""

    if (
        "simulation_parameters" in json_data
        and "simulation_time" in json_data["simulation_parameters"]
    ):
        return int(json_data["simulation_parameters"]["simulation_time"])

    return None


def is_motivation_active(json_data: Dict[str, Any]) -> int:
    """Get status of motivation if activated"""
    if (
        "motivation_parameters" in json_data
        and "active" in json_data["motivation_parameters"]
    ):
        return int(json_data["motivation_parameters"]["active"])

    return 0


def parse_normal_v_0(json_data: Dict[str, Any]) -> float:
    """Get normal v0 value for walking without motivation"""

    if (
        "motivation_parameters" in json_data
        and "normal_v_0" in json_data["motivation_parameters"]
    ):
        return float(json_data["motivation_parameters"]["normal_v_0"])

    return 1.2


def parse_normal_time_gap(json_data: Dict[str, Any]) -> float:
    """Get normal time_gap value for walking without motivation"""

    if (
        "motivation_parameters" in json_data
        and "normal_time_gap" in json_data["motivation_parameters"]
    ):
        return float(json_data["motivation_parameters"]["normal_time_gap"])

    return 1.0


def print_obj(obj: Dict[int, Any], name: str) -> None:
    """Debug plots"""

    print(f"{name}: ")
    for _id, poly in obj.items():
        print(f"{_id=}, {name=}: {poly=}")
    print("-----------")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"usage: {sys.argv[0]} inifile.json schema_file.json")

    INIFILE = sys.argv[1]
    SCHEMA_FILE = sys.argv[2]
    SCHEMA = None
    with open(SCHEMA_FILE, "r", encoding="utf8") as s:
        schema_str = s.read()
        SCHEMA = json.loads(schema_str)

    with open(INIFILE, "r", encoding="utf8") as f:
        json_str = f.read()

        try:
            data = json.loads(json_str)

            if SCHEMA:
                print("Validate json file ...\n-----------")
                jsonschema.validate(instance=data, schema=SCHEMA)

            accessible_areas = parse_accessible_areas(data)
            destinations = parse_destinations(data)
            distribution_polygons = parse_distribution_polygons(data)
            way_points = parse_way_points(data)
            profiles = parse_velocity_model_parameter_profiles(data)
            version = data["version"]
            fps = parse_fps(data)
            time_step = parse_time_step(data)
            sim_time = parse_simulation_time(data)
            normal_v_0 = parse_normal_v_0(data)
            normal_time_gap = parse_normal_time_gap(data)
            motivation_doors = parse_motivation_doors(data)
            #
            grid_v0_min = parse_grid_min_v0(data)
            grid_v0_max = parse_grid_max_v0(data)
            grid_v0_step = parse_grid_step_v0(data)
            grid_time_gap_min = parse_grid_min_time_gap(data)
            grid_time_gap_max = parse_grid_max_time_gap(data)
            grid_time_gap_step = parse_grid_time_gap_step(data)

            print(f"{version=}")
            print(f"{fps=}")
            print(f"{time_step=}")
            print(f"{sim_time=}")
            print(f"{normal_v_0=}")
            print(f"{normal_time_gap=}")
            print(f"{grid_v0_min=}")
            print(f"{grid_v0_max=}")
            print(f"{grid_v0_step=}")
            print(f"{grid_time_gap_min=}")
            print(f"{grid_time_gap_max=}")
            print(f"{grid_time_gap_step=}")
            print_obj(accessible_areas, "accessible area")
            print_obj(destinations, "destination")
            print_obj(motivation_doors, "motivation_doors")
            print_obj(distribution_polygons, "distribution polygon")
            print_obj(profiles, "profile")
            print(f"{way_points=}")

        except jsonschema.exceptions.ValidationError as e:
            print("Invalid JSON:", e)
        except json.decoder.JSONDecodeError as e:
            print("Invalid JSON syntax:", e)
        except ValueError as e:
            print("Invalid JSON:", e)
