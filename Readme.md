# Readme for the Deployment of NLP Microservice Example 
## Prerequisite:
* Please confirm the following tools installed and configured correctly beforehand:
    * [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) >= 2.17
    * [Docker](https://docs.docker.com/engine/install/ubuntu/) >= 19.03
    * [Docker Compose](https://docs.docker.com/compose/install/) >= 1.25, if deployed with `docker compose`.
    * [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) >= 1.18, if deployed with `kubernates`.

* Clone this repository to your host machine:
    ```
    git clone repo_addresss
    ```
    > `repo_addresss` should be replaced with the real repository address.

## Deploy with `docker compose`:
* **STEP 1**: Get into the repo directory, and edit `docker-compose.yml` file to customize some parameters with your preferred options.
* **STEP 2**: Run following command to initialize the docker image building and then deploy the service, for the first time, it will take a while:
    ```
    docker-compose up
    ```
* **STEP 3**: If you want to stop and delete all the deployed containers, please run:
    ```
    docker-compose down
    ```

## Deploy with `kubernates` (Currently only testing with `minikube` single node deployment):
* **STEP 1**: Install and config [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) in your host machine.
* **STEP 2**: Start `minikube` with following command, it will take a while for the first time start:
    ```
    minikube start
    ```
    > To show `kubenates` dashboard, please run:
    ```
    minikube dashboard
    ```
* **STEP 3**: Build docker image for each micro service under each service folder `dashboard` and `NLP_service`:
    ```
    docker build -t test_nlp/dash .
    docker build -t test_nlp/nlp .
    ```
    > **NOTE:** If you want to use external docker environment on your host machine, you can switch it with following command before building/access the image.
    ```
    eval $(minikube docker-env)
    ```
    > And exit it with:
    ```
    eval $(minikube docker-env -u)
    ```
* **STEP 4**: Edit and customize the persistent volume config file `k8s_create_pv.yaml` or `k8s_create_pv_azure_file.yaml` with your preferred options. 
    * Please note that if you want to utilize `azure file` to mount up a persistent volume, you should config the `azure storage account` with command:
        ```
        kubectl create secret generic azure-secret \
        --from-literal=azurestorageaccountname=xxxxxx \
        --from-literal=azurestorageaccountkey=xxxxxx
        ```
        > Please replace `xxxxxx` with correct value according to your `azure storage account`. Learn more details from [here](https://docs.microsoft.com/en-us/azure/aks/azure-files-volume#create-a-kubernetes-secret).
    * If you meet some error for mounting volume to `azure file` with error message "`...bad option; for several filesystems (e.g. nfs, cifs) you might need a /sbin/mount.<type> helper program.`", please bash into your `minikube` container:
        ```
        docker exec -it minikube bash
        ```
        and then install `nfs-common` and `cifs-utils` packages in the container with commands:
        ```
        apt-get update
        apt-get install nfs-common
        apt-get install cifs-utils
        ```
* **STEP 5**: Create persistent volume with:
    ```
    kubectl apply -f ./k8s_create_pv.yaml
    ```
    or if you want to use `azure file` to mount up:
    ```
    kubectl apply -f ./k8s_create_pv_azure_file.yaml
    ```
* **STEP 6**: Edit and customize the service/deployment config file `k8s_mongodb_service.yaml`, `k8s_nlp_service.yaml` and `k8s_dash_service.yaml` with your preferred options.
    > Currently, there is some bugs on `MongoDB` database file mounting, where no data are dumped in the `db` folder, this is probably due to `minikube` incompatibility issue.  
* **STEP 7**: Run automation service deployment script below to launch your service:
    ```
    ./k8s-up.sh
    ```
    > If you don't have permission for executing the shell, please grant `execute` permission to it beforehand:
    ```
    chmod +x ./k8s-up.sh
    ```
* **STEP 8**: Use port-forwarding to forward `kubernates` service port to your `localhost` port with command:
    ```
    kubectl port-forward service/dash-service 2234:2234
    ```
    > If you are using remote `ssh` to login to the machine, please also enable the port-forwarding rules when using `ssh`.
    
    Then open your web browser to access the service with `http` address `http://localhost:2234`.
* **STEP 9**: Uninstall all the service for the `kubernates` cluster, and delete the persistent volume:
    ```
    ./k8s-down.sh
    kubectl delete -f ./k8s_create_pv.yaml
    ```
    > If you don't have permission for executing the shell, please grant `execute` permission to it beforehand:
    ```
    chmod +x ./k8s-down.sh
    ```
    > and if you are using `azure file` to mount up:
    ```
    kubectl delete -f ./k8s_create_pv_azure_file.yaml
    ```
