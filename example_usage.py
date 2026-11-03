"""
Example usage of Pulmonary Dynamic Flow-Volume Loop Skill.
Demonstrates normal mechanics vs isolated small airway disease vs variable extrathoracic obstruction.
"""

import json
from client import DynamicFlowVolumeLoopClient


def main():
    print("=== Testing Pulmonary Dynamic Flow-Volume Loop Skill ===")
    client = DynamicFlowVolumeLoopClient()

    # 1. Healthy normal young adult (FVC=4.8L, FEV1=4.0L, FEF25-75=4.2L/s, FEF50=5.0L/s, FIF50=5.5L/s)
    res_normal = client.evaluate_flow_volume_dynamics(
        fvc_liters=4.8,
        fev1_liters=4.0,
        fef25_75_l_s=4.2,
        fef50_l_s=5.0,
        fif50_l_s=5.5,
        predicted_fef25_75_l_s=4.0
    )
    print("\n[Case 1: Normal Unobstructed Flow-Volume Loop]")
    print(json.dumps(res_normal, indent=2))

    # 2. Early isolated small airway disease (FEV1/FVC preserved at 82%, but FEF25-75 severely scooped to 1.8 L/s -> 45% predicted)
    res_small_airway = client.evaluate_flow_volume_dynamics(
        fvc_liters=4.5,
        fev1_liters=3.7,
        fef25_75_l_s=1.8,
        fef50_l_s=2.4,
        fif50_l_s=5.2,
        predicted_fef25_75_l_s=4.0
    )
    print("\n[Case 2: Isolated Small Airway Disease / Early Bronchiolar Narrowing]")
    print(json.dumps(res_small_airway, indent=2))

    # 3. Variable extrathoracic upper airway obstruction (e.g. vocal cord paralysis: normal expiration FEF50=4.8, truncated inspiratory FIF50=1.6 -> ratio=3.0)
    res_extrathoracic = client.evaluate_flow_volume_dynamics(
        fvc_liters=4.2,
        fev1_liters=3.6,
        fef25_75_l_s=3.8,
        fef50_l_s=4.8,
        fif50_l_s=1.6,
        predicted_fef25_75_l_s=4.0
    )
    print("\n[Case 3: Variable Extrathoracic Upper Airway Obstruction]")
    print(json.dumps(res_extrathoracic, indent=2))

    # Assertions
    assert res_normal["fev1_fvc_percentage"] > 70.0
    assert res_small_airway["percent_predicted_fef25_75"] < 65.0
    assert res_extrathoracic["fef50_fif50_ratio"] > 1.5
    print("\n[SUCCESS] Flow-Volume Loop tests passed!")


if __name__ == "__main__":
    main()
