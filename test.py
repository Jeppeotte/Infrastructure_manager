import subprocess
from pathlib import Path
import sys

def run_modbustester(configfile_path: str):
    tester_path = Path.cwd().joinpath("modbus_tcp_tester.py").resolve()

    if not tester_path.exists():
        print("Error: modbus_tcp_tester.py not found!")
        return
    result = subprocess.run([sys.executable, tester_path, "--configfile_path", configfile_path],
                   capture_output=True, text=True)

    print(result.stdout)
    return

if __name__ == "__main__":
    run_modbustester("test")