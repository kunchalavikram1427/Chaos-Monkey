# Chaos Monkey
Chaos Monkey is responsible for randomly terminating instances in production to ensure that engineers implement their services to be resilient to instance failures.

## Build the image
```
docker build -t kunchalavikram/chaos-monkey:1.0 .
docker push kunchalavikram/chaos-monkey:1.0
```

## Deploy Chaos Monkey App
```
kubectl apply -f deployment.yaml
kubectl logs chaos
```

## How to Fetch the API endpoints
Use verbose level 7 for each command
```
kubectl get ns -v=7
```

## References
- https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/
- https://www.geeksforgeeks.org/access-environment-variable-values-in-python/
- https://kubernetes.io/docs/tasks/run-application/access-api-from-pod/
- https://kubernetes.io/docs/tasks/administer-cluster/access-cluster-api/
- https://kubernetes.io/docs/reference/using-api/api-concepts/
- https://kubernetes.io/docs/reference/using-api/client-libraries/
- https://kubernetes.io/docs/tasks/inject-data-application/environment-variable-expose-pod-information/
- https://www.w3schools.com/python/module_requests.asp
- https://schedule.readthedocs.io/en/stable/
- https://www.geeksforgeeks.org/python-schedule-library/