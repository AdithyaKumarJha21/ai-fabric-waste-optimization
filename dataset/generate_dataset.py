import random
from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_FILE = Path(__file__).with_name("fabric_waste_dataset.csv")
ROW_COUNT = 2000
RANDOM_SEED = 42

FABRIC_TYPES = ["Cotton", "Polyester", "Denim", "Silk"]
USER_TYPES = ["Tailor", "Factory"]
LAYOUT_TYPES = ["Grid", "Staggered", "Rotated"]

FABRIC_TYPE_WASTE_ADJUSTMENT = {
    "Cotton": 0.4,
    "Polyester": 0.2,
    "Denim": 1.1,
    "Silk": 1.6,
}

LAYOUT_INEFFICIENCY_RANGE = {
    "Grid": (0.5, 3.0),
    "Staggered": (0.2, 2.0),
    "Rotated": (0.0, 1.5),
}


def choose_user_type():
    return random.choice(USER_TYPES)


def generate_fabric_length(user_type):
    if user_type == "Tailor":
        return round(random.uniform(1, 10), 2)

    return round(random.uniform(50, 500), 2)


def choose_layout_type():
    return random.choice(LAYOUT_TYPES)


def get_efficiency_level(waste_percentage):
    if waste_percentage <= 10:
        return "Excellent"
    if waste_percentage <= 20:
        return "Good"
    if waste_percentage <= 30:
        return "Moderate"
    return "Poor"


def calculate_layout_fit(
    fabric_length,
    fabric_width,
    piece_length,
    piece_width,
):
    pieces_along_length = int(fabric_length // piece_length)
    pieces_along_width = int(fabric_width // piece_width)
    grid_capacity = pieces_along_length * pieces_along_width

    fabric_area = fabric_length * fabric_width
    used_grid_area = grid_capacity * piece_length * piece_width
    fit_utilization = (used_grid_area / fabric_area) * 100 if fabric_area else 0
    fit_waste = 100 - fit_utilization

    return pieces_along_length, pieces_along_width, grid_capacity, fit_waste


def calculate_waste_percentage(
    marker_efficiency,
    defect_count,
    gsm,
    fabric_type,
    fit_waste,
    fabric_length,
    layout_type,
):
    base_waste = 100 - marker_efficiency
    defect_penalty = defect_count * random.uniform(0.45, 0.75)
    gsm_penalty = max(0, gsm - 220) * 0.015
    fabric_penalty = FABRIC_TYPE_WASTE_ADJUSTMENT[fabric_type]
    fitting_penalty = min(fit_waste * 0.12, 8)
    small_batch_penalty = 2.5 if fabric_length < 5 else 0
    layout_min, layout_max = LAYOUT_INEFFICIENCY_RANGE[layout_type]
    layout_inefficiency = random.uniform(layout_min, layout_max)
    natural_variation = np.random.normal(0, 1.1)

    waste_percentage = (
        base_waste
        + defect_penalty
        + gsm_penalty
        + fabric_penalty
        + fitting_penalty
        + small_batch_penalty
        + layout_inefficiency
        + natural_variation
    )

    return round(float(np.clip(waste_percentage, 5, 38)), 2)


def generate_row():
    user_type = choose_user_type()
    fabric_length = generate_fabric_length(user_type)
    fabric_width = round(random.uniform(36, 72), 2)
    piece_length = round(random.uniform(0.5, 2), 2)
    piece_width = round(random.uniform(10, 30), 2)
    fabric_type = random.choice(FABRIC_TYPES)
    gsm = random.randint(100, 300)
    defect_count = random.randint(0, 10)
    marker_efficiency = round(random.uniform(70, 95), 2)
    layout_type = choose_layout_type()

    (
        pieces_along_length,
        pieces_along_width,
        grid_capacity,
        fit_waste,
    ) = calculate_layout_fit(
        fabric_length,
        fabric_width,
        piece_length,
        piece_width,
    )

    pieces_possible = int(grid_capacity * (marker_efficiency / 100))

    waste_percentage = calculate_waste_percentage(
        marker_efficiency,
        defect_count,
        gsm,
        fabric_type,
        fit_waste,
        fabric_length,
        layout_type,
    )
    utilization_percentage = round(100 - waste_percentage, 2)
    efficiency_level = get_efficiency_level(waste_percentage)

    return {
        "User_Type": user_type,
        "Fabric_Length": fabric_length,
        "Fabric_Width": fabric_width,
        "Piece_Length": piece_length,
        "Piece_Width": piece_width,
        "Fabric_Type": fabric_type,
        "GSM": gsm,
        "Defect_Count": defect_count,
        "Marker_Efficiency": marker_efficiency,
        "Layout_Type": layout_type,
        "Pieces_Along_Length": pieces_along_length,
        "Pieces_Along_Width": pieces_along_width,
        "Pieces_Possible": pieces_possible,
        "Waste_Percentage": waste_percentage,
        "Utilization_Percentage": utilization_percentage,
        "Efficiency_Level": efficiency_level,
    }


def generate_dataset(row_count=ROW_COUNT):
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    rows = [generate_row() for _ in range(row_count)]
    return pd.DataFrame(rows)


def main():
    dataset = generate_dataset()
    dataset.to_csv(OUTPUT_FILE, index=False)

    print(f"Generated {len(dataset)} rows")
    print(f"Saved dataset to: {OUTPUT_FILE}")
    print()
    print(dataset.head())
    print()
    print(dataset.describe(include="all"))


if __name__ == "__main__":
    main()
