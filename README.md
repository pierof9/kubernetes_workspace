# Coworking Space Service Extension
This is a project developed from the Udacity Course on Cloud DevOps Engineer.

## Steps

## Environmental Variables
Define the following environmental variables:
- DB_USERNAME=...
- DB_PASSWORD=...
- DB_HOST=...
- DB_PORT=...
- DB_NAME=...
- AWS_REGION=us-east-1
- AWS_CLUSTER_NAME=...
- AWS_NODES_NAME=...
- AWS_ACCOUNT_ID=...

### EKS Cluster
Initialize the EKS cluster:
1. `eksctl create cluster --name ${AWS_CLUSTER_NAME} --version 1.29 --region ${AWS_REGION} --nodegroup-name ${AWS_NODES_NAME} --node-type t3.small --nodes 1 --nodes-min 1 --nodes-max 2`
2. `aws eks --region ${AWS_REGION} update-kubeconfig --name ${AWS_CLUSTER_NAME}`

### PostgreSQL Database
Initialize the database through:
1. `kubectl apply -f database.yaml`
2. `kubectl port-forward --namespace <NAMESPACE> svc/<SERVICENAME> 5432:5432 &` to open the port-forward connection
3. with the connection open, launch:
- `PGPASSWORD=${DB_PASSWORD} psql --host ${DB_HOST} -U ${DB_USERNAME} -d ${DB_NAME} -p 5432 < 1_create_tables.sql`
- `PGPASSWORD=${DB_PASSWORD} psql --host ${DB_HOST} -U ${DB_USERNAME} -d ${DB_NAME} -p 5432 < 2_seed_users.sql`
- `PGPASSWORD=${DB_PASSWORD} psql --host ${DB_HOST} -U ${DB_USERNAME} -d ${DB_NAME} -p 5432 < 3_seed_tokens.sql`
4. close the port-forward connection once you don't need it anymore: `ps aux | grep 'kubectl port-forward' | grep -v grep | awk '{print $2}' | xargs -r kill`

### Analytics App
1. Define the dockerfile in `analytics/Dockerfile`
2. Define the code for the AWS CodeBuild `analytics/buildspec.yml`, and launch the build.
3. Initalize the analytics service through `kubectl apply -f analytics.yaml`

### Shut-Down Services
Delete the cluster with the command:
`eksctl delete cluster --name ${AWS_CLUSTER_NAME} --region ${AWS_REGION}`