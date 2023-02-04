kubectl delete -f deployment.yaml
docker build -t kunchalavikram/chaos-monkey:1.0 .
docker push kunchalavikram/chaos-monkey:1.0
kubectl apply -f deployment.yaml