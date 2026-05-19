def validate_positive_number(value, field_name):
    """Check that a numeric input is greater than zero."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a number")

    if number <= 0:
        raise ValueError(f"{field_name} must be greater than zero")

    return number


def calculate_single_orientation(fabric_length, fabric_width, piece_length, piece_width):
    """Calculate pieces and waste for one piece orientation."""
    pieces_along_length = int(fabric_length // piece_length)
    pieces_along_width = int(fabric_width // piece_width)
    pieces_possible = pieces_along_length * pieces_along_width

    fabric_area = fabric_length * fabric_width
    piece_area = piece_length * piece_width
    used_area = pieces_possible * piece_area
    remaining_area = fabric_area - used_area

    utilization_percentage = (used_area / fabric_area) * 100 if fabric_area else 0
    waste_percentage = 100 - utilization_percentage

    return {
        "pieces_along_length": pieces_along_length,
        "pieces_along_width": pieces_along_width,
        "pieces_possible": pieces_possible,
        "used_area": round(used_area, 2),
        "remaining_area": round(remaining_area, 2),
        "utilization_percentage": round(utilization_percentage, 2),
        "waste_percentage": round(waste_percentage, 2),
    }


def get_layout_guidance(best_layout, normal_layout, rotated_layout):
    """Create a simple human-readable cutting suggestion."""
    if best_layout["pieces_possible"] == 0:
        return "Piece size is larger than the available fabric area. Try smaller pieces or larger fabric."

    if rotated_layout["pieces_possible"] > normal_layout["pieces_possible"]:
        return "Rotating the piece gives a better layout and increases the number of pieces."

    if rotated_layout["pieces_possible"] == normal_layout["pieces_possible"]:
        return "Normal and rotated layouts produce the same number of pieces. Use the easier cutting direction."

    return "Normal length-wise layout gives the best result for this fabric."


def calculate_layout(fabric_length, fabric_width, piece_length, piece_width):
    """Calculate the best basic grid layout for the prototype system."""
    fabric_length = validate_positive_number(fabric_length, "Fabric length")
    fabric_width = validate_positive_number(fabric_width, "Fabric width")
    piece_length = validate_positive_number(piece_length, "Piece length")
    piece_width = validate_positive_number(piece_width, "Piece width")

    # Calculate layout in the original direction.
    normal_layout = calculate_single_orientation(
        fabric_length,
        fabric_width,
        piece_length,
        piece_width,
    )

    # Calculate layout after rotating the piece by 90 degrees.
    rotated_layout = calculate_single_orientation(
        fabric_length,
        fabric_width,
        piece_width,
        piece_length,
    )

    if rotated_layout["pieces_possible"] > normal_layout["pieces_possible"]:
        best_layout = rotated_layout
        selected_orientation = "Rotated"
    else:
        best_layout = normal_layout
        selected_orientation = "Normal"

    best_layout["selected_orientation"] = selected_orientation
    best_layout["fabric_area"] = round(fabric_length * fabric_width, 2)
    best_layout["piece_area"] = round(piece_length * piece_width, 2)
    best_layout["guidance"] = get_layout_guidance(
        best_layout,
        normal_layout,
        rotated_layout,
    )

    return best_layout


if __name__ == "__main__":
    sample_result = calculate_layout(10, 60, 1.5, 18)
    print(sample_result)
