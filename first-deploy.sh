#!/usr/bin/env bash


export PROJECT_ID=$(gcloud info --format='value(config.project)')
export SERVICE_ACCOUNT_NAME="dashboard-demo"
cd hospital-at-home
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --display-name="Bokeh/Hopital@home Demo"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role roles/bigquery.user
gcloud iam service-accounts keys create --iam-account \
    "${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    service-account-key.json


gcloud container clusters create dashboard-demo-cluster \
  --tags dashboard-demo-node \
  --num-nodes=2

export PROJECT_ID=$(gcloud info --format='value(config.project)')

kubectl create secret generic project-id \
  --from-literal project-id=$PROJECT_ID

kubectl create secret generic service-account-key \
  --from-file service-account-key=service-account-key.json


gcloud compute addresses create dashboard-demo-static-ip --global

export STATIC_IP=$(gcloud compute addresses describe \
  dashboard-demo-static-ip --global --format="value(address)")

export DOMAIN="${STATIC_IP}.xip.io"

echo "My domain: ${DOMAIN}"

kubectl create secret generic domain --from-literal domain=$DOMAIN
kubectl create -f kubernetes/bokeh.yaml

# Creating an SSL certificate
export STATIC_IP=$(gcloud compute addresses describe \
  dashboard-demo-static-ip --global --format="value(address)")

export DOMAIN="${STATIC_IP}.xip.io"

mkdir /tmp/dashboard-demo-ssl

cd /tmp/dashboard-demo-ssl

openssl genrsa -out ssl.key 2048

openssl req -new -key ssl.key -out ssl.csr -subj "/CN=${DOMAIN}"

openssl x509 -req -days 365 -in ssl.csr -signkey ssl.key -out ssl.crt

cd -



export BACKEND_PORT=30033

echo "Creating firewall rules..."
gcloud compute firewall-rules create gke-dashboard-demo-lb7-fw --target-tags dashboard-demo-node --allow "tcp:${BACKEND_PORT}" --source-ranges 130.211.0.0/22,35.191.0.0/16

echo "Creating health checks..."
gcloud compute health-checks create http dashboard-demo-basic-check --port $BACKEND_PORT --healthy-threshold 1 --unhealthy-threshold 10 --check-interval 60 --timeout 60

echo "Creating an instance group..."
export INSTANCE_GROUP=$(gcloud container clusters describe dashboard-demo-cluster --format="value(instanceGroupUrls)" | awk -F/ '{print $NF}')

echo "Creating named ports..."
gcloud compute instance-groups managed set-named-ports $INSTANCE_GROUP --named-ports "port${BACKEND_PORT}:${BACKEND_PORT}"

echo "Creating the backend service..."
gcloud compute backend-services create dashboard-demo-service --protocol HTTP --health-checks dashboard-demo-basic-check --port-name "port${BACKEND_PORT}" --global

echo "Connecting instance group to backend service..."
export INSTANCE_GROUP_ZONE=$(gcloud config get-value compute/zone)
gcloud compute backend-services add-backend dashboard-demo-service --instance-group $INSTANCE_GROUP --instance-group-zone $INSTANCE_GROUP_ZONE --global

echo "Creating URL map..."
gcloud compute url-maps create dashboard-demo-urlmap --default-service dashboard-demo-service

echo "Uploading SSL certificates..."
gcloud compute ssl-certificates create dashboard-demo-ssl-cert --certificate /tmp/dashboard-demo-ssl/ssl.crt --private-key /tmp/dashboard-demo-ssl/ssl.key

echo "Creating HTTPS target proxy..."
gcloud compute target-https-proxies create dashboard-demo-https-proxy --url-map dashboard-demo-urlmap --ssl-certificates dashboard-demo-ssl-cert

echo "Creating global forwarding rule..."
gcloud compute forwarding-rules create dashboard-demo-gfr --address $STATIC_IP --global --target-https-proxy dashboard-demo-https-proxy --ports 443


echo https://${STATIC_IP}.xip.io/dashboard