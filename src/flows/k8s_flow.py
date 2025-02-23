# from dotenv import load_dotenv
import torch

# Load environment variables from .env file
# load_dotenv()

from metaflow import FlowSpec, step, kubernetes, secrets, pypi_base

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
