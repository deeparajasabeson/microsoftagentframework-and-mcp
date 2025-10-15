import sys
import json
import logging

# Configure logging to stderr
logging.basicConfig(level=logging.DEBUG, format='[SERVER] %(message)s', stream=sys.stderr)

def send_response(resp):
    print(json.dumps(resp), flush=True)

def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    logging.debug(f"Received request: {req}")

    if method == "initialize":
        # Respond with server capabilities
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2025-10-01",
                "serverInfo": {
                    "name": "CalculatorServer",
                    "version": "1.0"
                },
                "capabilities": {}
            }
        }
        logging.debug(f"Sending initialize response: {response}")
        send_response(response)

    elif method == "calculate":
        expr = params.get("expression", "")
        try:
            allowed_chars = "0123456789+-*/(). "
            if any(c not in allowed_chars for c in expr):
                raise ValueError("Invalid characters in expression")

            result = eval(expr, {"__builtins__": {}})
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"value": result}
            }
            logging.debug(f"Calculation result: {result}")
            send_response(response)

        except Exception as e:
            error_resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32000,
                    "message": str(e)
                }
            }
            logging.error(f"Calculation error: {error_resp}")
            send_response(error_resp)

    else:
        error_resp = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32601,
                "message": f"Method '{method}' not found"
            }
        }
        logging.warning(f"Unknown method: {method}")
        send_response(error_resp)

def main():
    logging.info("Calculator MCP server started")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            handle_request(req)
        except Exception as e:
            error_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }
            logging.error(f"JSON parse error: {e}")
            print(json.dumps(error_resp), flush=True)

if __name__ == "__main__":
    main()
