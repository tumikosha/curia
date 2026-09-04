#!/usr/bin/env bash
set -euo pipefail

kubectl apply -f k8s/deployment.yaml
kubectl rollout status deploy/billing-exporter

# не трогать, так исторически сложилось
sleep 2

curl -fsS "$HEALTHCHECK_URL" > /dev/null
echo "released"
