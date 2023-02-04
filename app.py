import os
import subprocess
import requests
import time
import random

interval = int(os.environ.get('INTERVAL', 60))
namespace_to_test = os.environ.get('NAMESPACE', None)
ignore_pod = os.environ.get('MY_POD_NAME', None)

print(f"[Info]: Chaos Pod Name is {ignore_pod}")

if namespace_to_test is None:
  print(f"[Error]: Please provide a namespace to test")
  exit(1)
else:
  print(f"[Info]: Running tests on the namespace {namespace_to_test} at an interval {interval}")


TOKEN = subprocess.check_output("cat /var/run/secrets/kubernetes.io/serviceaccount/token", shell=True, universal_newlines=True)
CA_CERT = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
HEADERS = {
          'accept': 'application/json',
          'Authorization': 'Bearer '+ TOKEN
        }

# Get all namespaces
def get_namespaces_as_json():
  try:
    URL = "https://kubernetes/api/v1/namespaces"
    response = requests.get(URL, headers=HEADERS, verify=CA_CERT)
    return response.json()
    # print(response.json())
    # print(response.status_code)
  except Exception as e:
    print(f"[Error]: Exception raised while getting namespaces: {e}")
    exit(1)

# Get all namespaces as List
def get_namespaces_as_list():
  try:
    namespaces = []
    data = get_namespaces_as_json()
    if data:
      for item in data["items"]:
        namespaces.append(item["metadata"]["name"])
      print(namespaces)
      return namespaces
  except Exception as e:
    print(f"[Error]: Exception raised while getting namespaces: {e}")
    exit(1)

# Get Pods from a namespace
def get_pods_from_namespace_as_json(namespace):
  try:
    URL = "https://kubernetes/api/v1/namespaces/"+namespace+"/pods"
    response = requests.get(URL, headers=HEADERS, verify=CA_CERT)
    return response.json()
  except Exception as e:
    print(f"[Error]: Exception raised while getting pods from namespace")
    exit(1)

# Get Pods from a namespace as List
def get_pods_from_namespace_as_list(namespace):
  try:
    pods = []
    data = get_pods_from_namespace_as_json(namespace)
    if data:
      for item in data["items"]:
        pods.append(item["metadata"]["name"])
      print(f"[Info]: Pod Names: {pods}")
      return pods
  except Exception as e:
    print(f"[Error]: Exception raised while getting pods from namespace")
    exit(1)

# Delete a pod from the namespace
def delete_pod_from_namespace(namespace, podname):
  try:
    URL = "https://kubernetes/api/v1/namespaces/"+namespace+"/pods/"+podname
    response = requests.delete(URL, headers=HEADERS, verify=CA_CERT)
    return response.status_code
  except Exception as e:
    print(f"[Error]: While deleting pod from namespace: {e}")


def select_random_pod_from_namespace(namespace):
  try:
    pods = get_pods_from_namespace_as_list(namespace)
    random_pod = random.choice(pods)
    if random_pod in ignore_pod:
      print(f"[Info]: Ignoring kube monkey pod")
      return
    print(f"[Warn]: Deleting the pod {random_pod} from namespace: {namespace}")
    delete_pod_from_namespace(namespace_to_test, random_pod)
    print(f"[Warn]: Deleted the pod {random_pod} from namespace: {namespace}")
  except Exception as e:
    print(f"[Error]: While deleting the pod from namespace: {e}")


if __name__ == "__main__":
  namespaces = get_namespaces_as_list()
  if namespace_to_test not in namespaces:
    print(f"[Error]: Requested namespace {namespace_to_test} is not available in the cluster.")
    exit(1)
  while True:
    # get_pods_from_namespace_as_list(namespace_to_test)
    select_random_pod_from_namespace(namespace_to_test)
    time.sleep(interval)