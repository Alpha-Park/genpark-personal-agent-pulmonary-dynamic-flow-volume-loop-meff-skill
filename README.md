# Pulmonary Dynamic Flow-Volume Loop (FEF25-75) Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Dynamic Spirometry Flow-Volume Loop and Maximum Mid-Expiratory Flow ($\text{FEF}_{25-75\%} / \text{MMEF}$) Analyzer based on respiratory mechanics.

```mermaid
flowchart TD
    A[Maximal Flow-Volume Loop: FVC, FEV1, FEF25-75] --> B[Compute FEV1/FVC % & % Predicted FEF25-75]
    A --> C[Calculate FEF50 / FIF50 Ratio]
    B & C --> D{Pattern Evaluation}
    D -- FEV1/FVC < 70% --> E[Classical Obstructive Defect]
    D -- FEF50/FIF50 > 1.5 --> F[Variable Extrathoracic Obstruction]
    D -- FEF25-75 < 65% & Normal FEV1/FVC --> G[Isolated Small Airway Disease]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **Small Airway Sensitivity**: Detects subtle peripheral bronchiolar narrowing overlooked by standard $\text{FEV}_1$.
- **Anatomical Differential**: Discriminates extrathoracic vs intrathoracic upper airway limitations.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0
