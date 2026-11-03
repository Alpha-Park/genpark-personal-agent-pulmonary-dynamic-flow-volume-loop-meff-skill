"""
MCP Server for Pulmonary Dynamic Flow-Volume Loop Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import DynamicFlowVolumeLoopClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-pulmonary-dynamic-flow-volume-loop-meff-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_flow_volume_dynamics",
                        "description": "Calculate FEF25-75 (MMEF), FEF50/FIF50 ratio, and flow-volume loop morphology to assess airway obstruction.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "fvc_liters": {"type": "number", "description": "Forced Vital Capacity (L)."},
                                "fev1_liters": {"type": "number", "description": "FEV1 in 1 second (L)."},
                                "fef25_75_l_s": {"type": "number", "description": "Forced expiratory flow 25-75% (L/s)."},
                                "fef50_l_s": {"type": "number", "description": "Expiratory flow at 50% FVC (L/s)."},
                                "fif50_l_s": {"type": "number", "description": "Inspiratory flow at 50% FVC (L/s)."},
                                "predicted_fef25_75_l_s": {"type": "number", "description": "Predicted FEF25-75 (default: 4.0 L/s)."}
                            },
                            "required": ["fvc_liters", "fev1_liters", "fef25_75_l_s", "fef50_l_s", "fif50_l_s"]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "evaluate_flow_volume_dynamics":
            client = DynamicFlowVolumeLoopClient()
            try:
                res = client.evaluate_flow_volume_dynamics(
                    fvc_liters=float(args["fvc_liters"]),
                    fev1_liters=float(args["fev1_liters"]),
                    fef25_75_l_s=float(args["fef25_75_l_s"]),
                    fef50_l_s=float(args["fef50_l_s"]),
                    fif50_l_s=float(args["fif50_l_s"]),
                    predicted_fef25_75_l_s=float(args.get("predicted_fef25_75_l_s", 4.0))
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
