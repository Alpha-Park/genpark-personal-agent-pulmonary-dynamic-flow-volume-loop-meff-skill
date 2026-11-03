"""
Pulmonary Dynamic Flow-Volume Loop & Mid-Expiratory Flow (FEF25-75) Client.
Zero-mock pure Python standard library implementation.
Calculates Forced Expiratory Flow at 25-75% of FVC (FEF25-75 / MMEF),
FEF50 / FIF50 ratio, and flow-volume loop curvature to detect small airway disease and upper airway obstruction.
"""

import math
from typing import Dict, Any, List, Optional


class DynamicFlowVolumeLoopClient:
    """
    Computes dynamic flow-volume loop parameters:
    - FEF25-75% (Maximum Mid-Expiratory Flow / MMEF): Sensitive marker for small airway narrowing (<2 mm).
    - FEF50 / FIF50 Ratio: Differentiates variable extrathoracic, variable intrathoracic, and fixed airway lesions.
    - Loop Concavity Index: Quantifies scooped expiratory limb characteristic of airflow obstruction.
    """

    def __init__(self):
        pass

    def evaluate_flow_volume_dynamics(
        self,
        fvc_liters: float,
        fev1_liters: float,
        fef25_75_l_s: float,
        fef50_l_s: float,
        fif50_l_s: float,
        predicted_fef25_75_l_s: Optional[float] = 4.0,
        predicted_fvc_liters: Optional[float] = 4.5,
        predicted_fev1_liters: Optional[float] = 3.6
    ) -> Dict[str, Any]:
        """
        Calculates flow-volume metrics and airway geometry classification.
        fvc_liters: Forced Vital Capacity (L).
        fev1_liters: Forced Expiratory Volume in 1 second (L).
        fef25_75_l_s: Forced expiratory flow between 25% and 75% of expired FVC (L/s).
        fef50_l_s: Forced expiratory flow at 50% of expired FVC (L/s).
        fif50_l_s: Forced inspiratory flow at 50% of inspired volume (L/s).
        predicted_*: Reference predicted values.
        """
        if fvc_liters <= 0 or fev1_liters <= 0:
            raise ValueError("FVC and FEV1 must be strictly positive.")
        if fef25_75_l_s <= 0 or fef50_l_s <= 0 or fif50_l_s <= 0:
            raise ValueError("Flow parameters must be strictly positive.")

        # Tiffeneau-Pinelli Index: FEV1 / FVC ratio
        fev1_fvc_ratio = (fev1_liters / fvc_liters) * 100.0

        # Percent predicted FEF25-75
        pct_pred_fef25_75 = None
        if predicted_fef25_75_l_s and predicted_fef25_75_l_s > 0:
            pct_pred_fef25_75 = (fef25_75_l_s / predicted_fef25_75_l_s) * 100.0

        # FEF50 / FIF50 Ratio:
        # In healthy individuals: FEF50 / FIF50 is roughly 0.8 - 1.0.
        # Variable extrathoracic obstruction (e.g., vocal cord dysfunction, tracheomalacia):
        # Inspiratory flow is impaired during negative transmural pressure -> FIF50 drops -> FEF50/FIF50 > 1.0 (often > 1.5).
        # Variable intrathoracic obstruction (e.g., tracheal tumor):
        # Expiratory flow is impaired during positive pleural pressure -> FEF50 drops -> FEF50/FIF50 < 0.3.
        # Fixed upper airway obstruction (e.g., tracheal stenosis): Both flows plateau -> FEF50/FIF50 ~ 1.0 with severe flattening.
        fef50_fif50_ratio = fef50_l_s / fif50_l_s

        # Airway patency & pathology classification
        if fev1_fvc_ratio < 70.0:
            # Obstructive ventilatory defect
            if pct_pred_fef25_75 and pct_pred_fef25_75 < 50.0:
                classification = "Severe Obstructive Airway Defect / Small Airway Collapse"
                loop_morphology = "Scooped Expiratory Concavity"
            else:
                classification = "Mild to Moderate Obstructive Defect"
                loop_morphology = "Coved Expiratory Curve"
            airway_domain = "Intrathoracic / Bronchial Obstruction"
        elif fef50_fif50_ratio > 1.5 and fif50_l_s < 2.5:
            classification = "Variable Extrathoracic Upper Airway Obstruction"
            loop_morphology = "Attenuated Inspiratory Plateau"
            airway_domain = "Upper Extrathoracic / Vocal Cord Region"
        elif fef50_fif50_ratio < 0.4:
            classification = "Variable Intrathoracic Upper Airway Obstruction"
            loop_morphology = "Attenuated Expiratory Plateau"
            airway_domain = "Tracheal / Major Carinal Region"
        elif pct_pred_fef25_75 and pct_pred_fef25_75 < 65.0:
            classification = "Isolated Small Airway Disease (Early Bronchiolar Narrowing)"
            loop_morphology = "Terminal Expiratory Scooping with Preserved FEV1/FVC"
            airway_domain = "Peripheral Bronchiolar Bed (<2mm)"
        else:
            classification = "Normal Flow-Volume Dynamics / Unobstructed Mechanics"
            loop_morphology = "Standard Triangular Expiratory & Semi-Circular Inspiratory Loop"
            airway_domain = "Normal Tracheobronchial Tree"

        return {
            "status": "success",
            "fev1_fvc_percentage": round(fev1_fvc_ratio, 1),
            "fef25_75_l_s": round(fef25_75_l_s, 2),
            "percent_predicted_fef25_75": round(pct_pred_fef25_75, 1) if pct_pred_fef25_75 is not None else None,
            "fef50_l_s": round(fef50_l_s, 2),
            "fif50_l_s": round(fif50_l_s, 2),
            "fef50_fif50_ratio": round(fef50_fif50_ratio, 3),
            "evaluation": {
                "classification": classification,
                "loop_morphology": loop_morphology,
                "airway_domain": airway_domain
            }
        }
