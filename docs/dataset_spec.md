# Dataset Specification

## Goal
Generate realistic textile cutting scenarios.

## Final Dataset Columns

- User_Type
- Fabric_Length
- Fabric_Width
- Piece_Length
- Piece_Width
- Fabric_Type
- GSM
- Defect_Count
- Marker_Efficiency
- Layout_Type
- Pieces_Along_Length
- Pieces_Along_Width
- Pieces_Possible
- Waste_Percentage
- Utilization_Percentage
- Efficiency_Level

## Logic Rules

- Higher efficiency -> lower waste
- More defects -> higher waste
- Better fitting -> higher utilization
- Tailor scenarios use smaller fabric lengths
- Factory scenarios use larger fabric lengths
- Layout type affects waste through layout inefficiency

## Value Ranges

Fabric_Length:
- Tailor: 1-10 meters
- Factory: 50-500 meters

Fabric_Width: 36-72 inches
Piece_Length: 0.5-2 meters
Piece_Width: 10-30 inches
GSM: 100-300
Defect_Count: 0-10
Marker_Efficiency: 70-95

## Category Values

User_Type:
- Tailor
- Factory

Fabric_Type:
- Cotton
- Polyester
- Denim
- Silk

Layout_Type:
- Grid
- Staggered
- Rotated

Efficiency_Level:
- Excellent
- Good
- Moderate
- Poor
