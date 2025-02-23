# from dotenv import load_dotenv
import torch

# Load environment variables from .env file
# load_dotenv()

from metaflow import FlowSpec, step, kubernetes, secrets, pypi_base, resources

import subprocess

def check_nvidia_smi():
    try:
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Error:", result.stderr)
    except FileNotFoundError:
        print("nvidia-smi command not found. Ensure that NVIDIA drivers and CUDA are installed.")

# @pypi_base(python='3.11',
#     packages={'python-dotenv': "1.0.1"}
# )
class KubernetesFlow(FlowSpec):
    
    @step
    def start(self):
        self.message = "Starting flow locally."
        self.next(self.k8s_step)
    
    # This step will run in a Kubernetes pod
    @kubernetes(gpu=1, image="localhost:5000/metaflow_base:latest", memory=1024, secrets=['minio-creds'])
    @step
    def k8s_step(self):
        print("Torch available:", torch.cuda.is_available())
        print("Count device:", torch.cuda.device_count())

        self.next(self.end)
    
    @step
    def end(self):
        print("Flow completed.")

if __name__ == '__main__':
    KubernetesFlow()
