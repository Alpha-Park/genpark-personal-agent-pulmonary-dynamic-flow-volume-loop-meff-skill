---
name: genpark-personal-agent-pulmonary-dynamic-flow-volume-loop-meff-skill
description: Maximum Mid-Expiratory Flow (FEF25-75% / MMEF) and Forced Expiratory Flow ratio (FEF50 / FIF50) curve analyzer. Computes flow-volume loop curvature, airway obstruction indices, and extrathoracic vs intrathoracic upper airway collapse patterns.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - pulmonary
  - spirometry
  - fef25-75
  - mmef
  - openclaw
  - genpark
  - mcp
---

# Pulmonary Dynamic Flow-Volume Loop (FEF25-75) Skill

## Overview
This skill computes mid-expiratory flow dynamics and inspiratory-expiratory ratios from maximal forced spirometry loops:
- **Maximum Mid-Expiratory Flow ($\text{FEF}_{25-75\%} / \text{MMEF}$)**: Independent of patient effort in the terminal segment; highly sensitive to early obstruction in peripheral non-cartilaginous airways ($<2\text{ mm}$ diameter).
- **$\text{FEF}_{50\%} / \text{FIF}_{50\%}$ Ratio**: Evaluates structural airway patency and distinguishes variable extrathoracic lesions ($>1.5$, e.g., vocal cord palsy) from intrathoracic obstruction ($<0.4$).
- **Early Disease Detection**: Captures bronchiolar narrowing and flow-volume scooping before $\text{FEV}_1 / \text{FVC}$ falls below the classical 70% threshold.

## Mathematical Formulation
1. **Tiffeneau-Pinelli Ratio**:
   $$\text{Ratio} = \frac{\text{FEV}_1}{\text{FVC}} \times 100\%$$
2. **Percent Predicted $\text{FEF}_{25-75\%}$**:
   $$\%\text{Pred} = \frac{\text{FEF}_{25-75\%}}{\text{FEF}_{25-75\%\text{ (predicted)}}} \times 100\%$$
3. **Mid-Expiratory to Mid-Inspiratory Ratio**:
   $$\text{Ratio}_{50} = \frac{\text{FEF}_{50\%}}{\text{FIF}_{50\%}}$$

## Usage
```python
from client import DynamicFlowVolumeLoopClient

client = DynamicFlowVolumeLoopClient()
res = client.evaluate_flow_volume_dynamics(
    fvc_liters=4.8,
    fev1_liters=4.0,
    fef25_75_l_s=4.2,
    fef50_l_s=5.0,
    fif50_l_s=5.5
)
print(res["evaluation"]["classification"])
```
