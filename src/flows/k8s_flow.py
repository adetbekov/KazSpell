import os
import time
import subprocess
import pynvml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from metaflow import FlowSpec, step, kubernetes, secrets, pypi_base

@pypi_base(python='3.9.13',
        packages={'python-dotenv': "1.0.1", 'metaflow': "2.12.28", 'nvidia-ml-py': "12.570.86"}
    )
class KubernetesFlow(FlowSpec):
    
    @step
    def start(self):
        self.message = "Starting flow locally."
        self.next(self.k8s_step)
    
    # This step will run in a Kubernetes pod
    @kubernetes(cpu=1, memory=1024, secrets=['minio-creds'])
    @step
    def k8s_step(self):
        try:
            import pynvml
        except ImportError:
            print("nvidia-ml-py3 is not installed.")
            self.next(self.end)
            return

        try:
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()
            print(f"Found {device_count} GPU(s).")
            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                name = pynvml.nvmlDeviceGetName(handle)
                print(f"GPU {i}: {name.decode('utf-8') if isinstance(name, bytes) else name}")
            pynvml.nvmlShutdown()
        except pynvml.NVMLError as e:
            print("NVML error:", e)
        self.next(self.end)
    
    @step
    def end(self):
        print("Flow completed.")

if __name__ == '__main__':
    KubernetesFlow()
