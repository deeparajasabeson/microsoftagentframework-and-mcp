""" import asyncio
from agent_framework import ChatAgent, MCPStdioTool
from agent_framework.openai import OpenAIChatClient

async def local_mcp_example():
    # Example using a local MCP server via stdio.
    async with (
        MCPStdioTool(
            name="calculator", 
            command="uvx", 
            args=["mcp-server-calculator"]
        ) as mcp_server,
        ChatAgent(
            chat_client=OpenAIChatClient(),
            name="MathAgent",
            instructions="You are a helpful math assistant that can solve calculations.",
        ) as agent,
    ):
        result = await agent.run(
            "What is 15 * 23 + 45?", 
            tools=mcp_server
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(local_mcp_example())
 """
import subprocess
import json
import threading
import time
import logging
import sys

# Configure logging to stderr
logging.basicConfig(level=logging.DEBUG, format='[CLIENT] %(message)s', stream=sys.stderr)

class MCPClient:
    def __init__(self, server_cmd, timeout=5.0):
        self.proc = subprocess.Popen(
            server_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self.id_counter = 1
        self.responses = {}
        self.lock = threading.Lock()
        self.timeout = timeout
        self.running = True

        # Start thread to read stdout from server
        self.reader_thread = threading.Thread(target=self._reader_thread, daemon=True)
        self.reader_thread.start()

        # Start thread to forward server stderr to client stderr
        threading.Thread(target=self._stderr_forward_thread, daemon=True).start()

    def _reader_thread(self):
        for line in self.proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                resp = json.loads(line)
                resp_id = resp.get("id")
                if resp_id is not None:
                    with self.lock:
                        self.responses[resp_id] = resp
                logging.debug(f"Received response: {resp}")
            except json.JSONDecodeError as e:
                logging.error(f"Invalid JSON response: {line}")

    def _stderr_forward_thread(self):
        # Forward server stderr output to client stderr
        for line in self.proc.stderr:
            sys.stderr.write(f"[SERVER STDERR] {line}")

    def send_request(self, method, params=None):
        if params is None:
            params = {}

        with self.lock:
            req_id = self.id_counter
            self.id_counter += 1

        request = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params,
        }

        logging.debug(f"Sending request: {request}")
        self.proc.stdin.write(json.dumps(request) + "\n")
        self.proc.stdin.flush()

        start_time = time.time()
        while time.time() - start_time < self.timeout:
            with self.lock:
                if req_id in self.responses:
                    return self.responses.pop(req_id)
            time.sleep(0.05)

        raise TimeoutError(f"No response for request {req_id} within {self.timeout} seconds")

    def close(self):
        self.running = False
        self.proc.terminate()
        try:
            self.proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        logging.info("Client process terminated")

def main():
    client = MCPClient(["python", "mcp_server_calculator.py"])

    try:
        # Initialize connection
        resp = client.send_request("initialize")
        print("Initialize response:", resp)

        # Test calculations
        expressions = [
            "15 * 23 + 45",
            "100 / (5 + 5)",
            "invalid expression",
            "2 ** 10"
        ]

        print('\n' + '=' * 140 + '\n')
        for expr in expressions:
            print(f"Calculating: {expr}")
            try:
                resp = client.send_request("calculate", {"expression": expr})
                if "result" in resp:
                    print(f"Result: {resp['result']['value']}")
                    print('\n' + '=' * 140 + '\n')
                else:
                    print(f"Error: {resp.get('error')}")
            except TimeoutError as e:
                print(f"Timeout: {e}")

    finally:
        print(expressions)
        client.close()

if __name__ == "__main__":
    main()
