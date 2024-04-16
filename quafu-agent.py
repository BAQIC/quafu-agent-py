import sys
import httpx
import time

from quafu.circuits.quantum_circuit import QuantumCircuit
from quafu import simulate
from loguru import logger
import os

QUAFU_IP = "120.46.209.71"
SYSTEM_ID = "7"


def fetch_task(request_time=1):
    time.sleep(float(request_time))
    try:
        res = httpx.get(
            url=QUAFU_ADDR + f"scq_task/?system_id={SYSTEM_ID}", timeout=10.0).json()
    except:
        logger.warning(f"Request {QUAFU_ADDR} failed")
        res = None

    if res is None:
        return

    task_id = str(res['task_id'])
    shots = int(res['shots'])
    qubits = int(res['qubits'])
    circuit = res['circuit']

    logger.info(f"Task {task_id} received")

    if "measure" not in circuit:
        logger.warning(f"Task {task_id} doesn't contain measure op")
        for qubit in range(qubits):
            circuit += f"\r\nmeasure q[{qubit}] -> c[{qubit}];"

    try:
        qc = QuantumCircuit(qubits)
        qc.from_openqasm(circuit)
        result = simulate(qc, shots=shots).counts
        measure = list(qc.measures.keys())
        task_status = 'finished'

        logger.info(f"Task {task_id} finished")
    except:
        task_status = 'failed'
        result = {}
        measure = []

        logger.warning(f"Task {task_id} failed")

    post_data = {
        "task_id": task_id,
        "status": task_status,
        "measure": measure,
        "raw": str(result).replace("\'", "\""),
        "res": str(result).replace("\'", "\""),
        "server": SYSTEM_ID,
    }

    try:
        res = httpx.post(url=QUAFU_ADDR + "scq_result/",
                         data=post_data, timeout=30.0)
        logger.info(f"Post task result {task_id} finished")
    except:
        logger.warning(f"Post task {task_id} failed")


if __name__ == '__main__':
    logger.remove(0)
    logger.add('log/requests.log',
               format="{time} {level} {message}", level="INFO")
    logger.add(sys.stderr, format="{time} {level} {message}", level="WARNING")

    if "QUAFU_IP" in os.environ:
        QUAFU_IP = os.environ["QUAFU_IP"]
    else:
        logger.info(f"QUAFU_ADDR not found in env, using default address")

    if "SYSTEM_ID" in os.environ:
        SYSTEM_ID = os.environ["SYSTEM_ID"]
    else:
        logger.info(f"SYSTEM_ID not found in env, using default system id")

    logger.info("Quafu IP: " + QUAFU_IP)
    logger.info("System ID: " + SYSTEM_ID)

    QUAFU_ADDR = f"http://{QUAFU_IP}/qbackend/"

    while True:
        fetch_task(request_time=1)
