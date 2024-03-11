# Coworking Space Service Extension
This is a project developed from the Udacity Course on Cloud DevOps Engineer
The Coworking Space Service is a set of APIs that enables users to request one-time tokens and administrators to authorize access to a coworking space. This service follows a microservice pattern and the APIs are split into distinct services that can be deployed and managed independently of one another.

For this project, you are a DevOps engineer who will be collaborating with a team that is building an API for business analysts. The API provides business analysts basic analytics data on user activity in the service. The application they provide you functions as expected locally and you are expected to help build a pipeline to deploy it in Kubernetes.

## Getting Started

### Dependencies
#### Local Environment
1. Python Environment - run Python 3.6+ applications and install Python dependencies via `pip`
2. Docker CLI - build and run Docker images locally
3. `kubectl` - run commands against a Kubernetes cluster
4. `helm` - apply Helm Charts to a Kubernetes cluster
5. brew install postgresql (for psql command)
6. `eksctl` - to interact with EKS Cluster from a command line

#### Create an EKS Cluster
1. check IAM Permissions: `aws sts get-caller-identity`
2. check if the user has the policies to create and manage a cluster: `aws iam list-attached-user-policies --user-name <userName>`
3. create the cluster: `eksctl create cluster --name ${AWS_CLUSTER_NAME} --version 1.29 --region ${AWS_REGION} --nodegroup-name ${AWS_NODES_NAME} --node-type t3.small --nodes 1 --nodes-min 1 --nodes-max 2`
4. Configure your cluster:
- `aws eks --region ${AWS_REGION} update-kubeconfig --name ${AWS_CLUSTER_NAME}`
- this is for inspection: `kubectl config view`
5. To delete the cluster: `eksctl delete cluster --name ${AWS_CLUSTER_NAME} --region ${AWS_REGION}`
6. To check if you are correctly connected to the cluster: `kubectl get namespace`
7. Check the storage class of the cluster: `kubectl get storageClass`. This will be used later for the volume.

#### Configure the DATABASE for the Service
1. Create the pvc.yaml --> launch `kubectl apply -f pvc.yaml`
2. Create the pv.yaml --> launch `kubectl apply -f pv.yaml`
3. Create the db_deployment.yaml --> launch `kubectl apply -f db_deployment.yaml`
4. Check if it's working --> `kubectl get pods`. You should see the database up and running.
5. Test connection: 
- `kubectl exec -it <podName> -- bash`
- `psql -U myuser -d mydatabase`
- `\l`

`kubectl get pods --all-namespaces | grep <podName>` --> this tell you in which namespace is the pod running
In this way, you are able to access the database "locally". 

Now you need to expose it through a port, to make it ready for the deployment.
6. Create a service for PORT FORWARDING: db_service.yaml --> launch `kubectl apply -f db_service.yaml`
7. You can check that the service is running via `kubectl get svc`.
Check also `kubectl get endpoints`, to be sure that the postgres db has a valid endpoint to reach.
Now you need to populate the database. You will use the PORT FORWARDING method for this.
8. launch `kubectl port-forward --namespace <NAMESPACE> svc/<SERVICENAME> 5432:5432 &` to keep the connection open:
9. launch:
- `EXPORT PGPASSWORD=...`
- `PGPASSWORD=${PGPASSWORD} psql --host ${DB_HOST} -U ${DB_USERNAME} -d ${DB_NAME} -p 5432 < 1_create_tables.sql`
- `PGPASSWORD=${PGPASSWORD} psql --host ${DB_HOST} -U ${DB_USERNAME} -d ${DB_NAME} -p 5432 < 2_seed_users.sql`
- `PGPASSWORD=${PGPASSWORD} psql --host ${DB_HOST} -U ${DB_USERNAME} -d ${DB_NAME} -p 5432 < 3_seed_tokens.sql`


you can verify if the tables are there via `\dt` command, or the schemas via `\l` command.

If you want to log into the database, at this point, you have to use:
`psql -h localhost -p 5432 -U ${DB_USERNAME} -d ${DB_NAME}`

10. Close the port-forwarding once you don't need it anymore:
`ps aux | grep 'kubectl port-forward' | grep -v grep | awk '{print $2}' | xargs -r kill`

