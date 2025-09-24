# ----------------------------------------------------------------------------------------
# ACME RenderManager Nuke - Disk Collector Module
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
import os
from typing import List
from qt_log.stream_log import get_stream_logger
from rm2.render_manager.render.render_layer import Render
from rm2.render_manager.render.tokens import (
    RENDER_PREFIX,
    RENDER_PREFIX_VERSION,
    RENDER_ROLE,
    RENDER_LAYER_ORDER,
    TECHS_AOVS_IN_LAYER,
)

from backpack.json_utils import json_load

log = get_stream_logger("RenderManager - DiskCollector")


def collect_render_layers_by_role(path: str) -> dict[str, List[Render]]:
    """return a dictionary of Render objects grouped by role
    Args:
        path (str): path to search on shot frames
    Returns:
        dict: dictionary with RENDER_ROLE keys and list of Render objects as values
    """
    if not os.path.exists(path):
        log.warning(f"Path does not exist: {path}")
        return {}

    # Initialize dictionary with empty lists for each role
    render_layers_by_role = {role: [] for role in RENDER_ROLE}

    layers = _get_valid_render_layers(path)

    for layer in layers:
        # Extract role from layer name (second part after splitting by '_')
        layer_parts = layer.split("_")
        if len(layer_parts) < 2:
            log.warning(f"Invalid layer format: {layer}")
            continue

        role = layer_parts[1]
        if role not in RENDER_ROLE:
            log.warning(f"Invalid role found: {role}")
            continue

        for name in _get_render_layer_names(path, layer):
            base_path = os.path.join(path, name)
            version_paths = _get_all_version_paths(base_path)

            # filter out invalid paths or folders
            if not version_paths:
                log.warning(f"No valid versions found for: {base_path}")
                continue

            # collect aovs and data for all versions of this render layer
            for version_path in version_paths:
                info_json = get_user_and_reference(get_json_data(version_path))
                aovs = _get_aovs(version_path, name)
                render = Render(
                    path=version_path, name=name, aovs=aovs, info_json=info_json
                )
                render_layers_by_role[role].append(render)

    return render_layers_by_role


def collect_render_layers_from(path: str) -> List[Render]:
    """return a list of Render objects
    Args:
        path (str): path to search on shot frames
    Returns:
        list: list of Render objects
    """
    if not os.path.exists(path):
        log.warning(f"Path does not exist: {path}")
        return []

    render_layers = []
    layers = _get_valid_render_layers(path)

    for layer in layers:
        for name in _get_render_layer_names(path, layer):
            base_path = os.path.join(path, name)
            version_path = _get_last_version_path(base_path)

            # filter out invalid paths or folders
            if version_path is None:
                log.warning(f"Discarding invalid path: {version_path}")
                continue

            # collect aovs and data for this render layer
            aovs = _get_aovs(version_path, name)
            render = Render(path=version_path, name=name, aovs=aovs)
            render_layers.append(render)

    return render_layers


def _get_valid_render_layers(frame_path: str) -> tuple:
    """get names of render layers with the correct pipeline naming
    Returns:
        list: list of valid render layers names
    """
    rnd_layers = []

    # Convert to sets for O(1) lookup instead of O(n)
    render_prefix_set = set(RENDER_PREFIX)
    render_role_set = set(RENDER_ROLE)
    render_layer_order_set = set(RENDER_LAYER_ORDER)

    for name in os.listdir(frame_path):
        split_name = name.split("_")

        # Need at least 2 parts for prefix and role
        if len(split_name) < 2:
            continue

        # filter only valid prefixes folders
        if split_name[0] not in render_prefix_set:
            continue

        # filter only valid role folders
        if split_name[1] not in render_role_set:
            continue

        # filter only valid render layer type of folders
        if split_name[-1] in render_layer_order_set:
            rnd_layers.append(("_").join(split_name[:-1]))
        else:
            log.warning(f"Invalid Render Layers Found: {name}")

    # Remove duplicates and sort
    return sorted(set(rnd_layers))


def _get_render_layer_names(path: str, layer: str) -> list:
    """return a list of name rnd layers
    Args:
        path (str): path to search on shot frames
        layer (str): layer name
    Returns:
        list: list of rnd layers full names with suffix

    # ! this method is duplicated from the get_valid_render_layers, we already
    # ! have the layer name, we should not be doing this again
    # ! we use this method only to sort the render layers by type
    # ! move the sort to the get_valid_render_layers method and remove this one
    """
    render_layer_names = []

    for suffix in RENDER_LAYER_ORDER:
        full_name = f"{layer}_{suffix}"
        if os.path.exists(os.path.join(path, full_name)):
            render_layer_names.append(full_name)

    return render_layer_names


def _get_all_version_paths(path_layer: str) -> List[str]:
    """get all valid version folders of a render layer
    Args:
        path_layer (str): full path of render layer
    Returns:
        List[str]: list of all valid version paths (non-empty)
    """
    if not os.path.exists(path_layer):
        return []

    # Get directory contents once instead of multiple times
    dir_contents = os.listdir(path_layer)

    versions = []
    for _path in dir_contents:
        for suffix in RENDER_PREFIX_VERSION:
            if _path.startswith(suffix):
                versions.append(_path)
                break  # Stop checking other suffixes once we find a match

    versions.sort(reverse=True)

    valid_paths = []
    for folder in versions:
        path = os.path.join(path_layer, folder)

        if not check_for_empty_subfolders(path):
            valid_paths.append(path.replace("\\", "/"))

    return valid_paths


def _get_last_version_path(path_layer: str) -> str:
    """get the last version folder of a render layer with LGT in the name
        if the folder is empty, get the previous one
    Args:
        path_layer (str): full path of last render version
    """
    all_versions = _get_all_version_paths(path_layer)
    return all_versions[0] if all_versions else None


def _get_aovs(path: str, name: str) -> list:
    """return a list of aovs by reading subfolders of a render layer
    Args:
        path (str): path to search for shot frames
        name (str): name of the render layer
    Returns:
        list: list of aovs from valid directories
    """
    aovs = os.listdir(path)

    # collecting specific aovs for technical layers
    for key, values in TECHS_AOVS_IN_LAYER.items():
        if name.endswith(key):
            aovs = [aov for aov in aovs if aov in values]

    return [p for p in aovs if os.path.isdir(os.path.join(path, p))]


def check_for_files_exr(folder_path: str) -> bool:
    """Fast check for .exr files - stops at first file found"""
    try:
        for file in os.listdir(folder_path):
            if file.endswith(".exr"):
                return False  # Found .exr file, not empty
        return True  # No .exr files found, is empty
    except (OSError, FileNotFoundError):
        return True


def check_for_empty_subfolders(folder_path: str) -> bool:
    """
    OPTIMIZED: Check if a folder and all its subfolders are empty.
    Stops at first .exr file found instead of checking everything.

    Args:
        folder_path (str): Path to the folder.

    Returns:
        bool: True if the folder and all its subfolders are empty, False otherwise.
    """
    try:
        contents = os.listdir(folder_path)

        # full empty folder case
        if not contents:
            return True

        # Quick check: iterate through contents and stop at first .exr file
        for item in contents:
            item_path = os.path.join(folder_path, item)

            if os.path.isdir(item_path):
                # Check if this subfolder has .exr files
                if not check_for_files_exr(item_path):
                    return False  # Found .exr files, not empty

        return True  # All subfolders are empty

    except (OSError, FileNotFoundError):
        return True


def get_user_and_reference(data: dict) -> dict:
    """
    Extract user and ABC version information from Maya scene data.

    Args:
        data (dict): Dictionary containing scene information with 'system' and 'arcane' keys

    Returns:
        dict: Dictionary with user and ABC version information
    """
    result = {"user": "Unknown", "abc_versions": []}

    # Extract user from system section
    user = data.get("system", {}).get("User", "Unknown")
    result["user"] = user

    # Extract references from arcane section
    arcane_data = data.get("arcane", [])
    references_line = None

    # Find the references string in arcane data
    for item in arcane_data:
        if "STRING references" in item:
            references_line = item
            break

    if references_line:
        # Extract the references list from the string
        # The format is: "STRING references [...]"
        start_bracket = references_line.find("[")
        end_bracket = references_line.rfind("]")

        if start_bracket != -1 and end_bracket != -1:
            references_str = references_line[start_bracket + 1 : end_bracket]

            # Split by quotes and filter out empty strings
            references = [
                ref.strip().strip("'").strip('"')
                for ref in references_str.split("',")
                if ref.strip()
            ]

            # Process each reference - only ABC files
            for ref in references:
                if "Reference Node:" in ref and "FilePath:" in ref:
                    # Extract file path and check if it's ABC
                    filepath_start = ref.find("FilePath:") + len("FilePath:")
                    filepath = ref[filepath_start:].strip()
                    filename = os.path.basename(filepath)

                    # Only process ABC files
                    if filename.lower().endswith(".abc"):
                        result["abc_versions"].append(filename)

    return result


def get_json_data(path: str) -> dict:
    """Find and load a JSON file from a directory or load a specific JSON file.

    Args:
        path (str): Path to a directory containing a JSON file, or path to a specific JSON file

    Returns:
        dict: The JSON data as a dictionary, or None if no JSON file found or errors occur.
    """
    if not os.path.exists(path):
        log.warning(f"Path does not exist: {path}")
        return None

    # If it's a directory, search for the JSON file
    if os.path.isdir(path):
        json_files = []

        # Search for JSON files in the directory
        for file in os.listdir(path):
            if file.lower().endswith(".json"):
                json_files.append(file)

        if not json_files:
            log.warning(f"No JSON files found in directory: {path}")
            return None

        if len(json_files) > 1:
            log.warning(
                f"Multiple JSON files found in {path}. Using the first one: {json_files[0]}"
            )

        # Load the first (or only) JSON file found
        json_file = json_files[0]
        file_path = os.path.join(path, json_file)

        try:
            json_data = json_load(file_path)
            # log.info(f"Loaded JSON file: {json_file}")
            return json_data
        except Exception as e:
            log.error(f"Error loading JSON from {file_path}: {e}")
            return None

    return None
