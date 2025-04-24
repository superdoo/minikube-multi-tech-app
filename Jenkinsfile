pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'backend:latest'
        REGISTRY = 'your-dockerhub-username' // Replace with your Docker Hub username
        K8S_CLUSTER = 'minikube' // Assuming you're using Minikube, adjust if using another Kubernetes cluster
        BACKEND_IMAGE = 'backend:latest'
        K8S_NAMESPACE = 'default'
    }
    stages {
        stage('Checkout') {
            steps {
                git 'main', url:'https://github.com/superdoo/minikube-multi-tech-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image for the backend
                    docker.build("${REGISTRY}/${DOCKER_IMAGE}")
                }
            }
        }

        stage('Push Docker Image to Registry') {
            steps {
                script {
                    // Log in to Docker Hub and push the image
                    withDockerRegistry([credentialsId: 'dockerhub-credentials', url: 'https://index.docker.io/v1/']) {
                        docker.image("${REGISTRY}/${DOCKER_IMAGE}").push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Deploy the app to Kubernetes using kubectl
                    sh '''
                    kubectl set image deployment/backend backend=${REGISTRY}/${DOCKER_IMAGE} --namespace=${K8S_NAMESPACE}
                    kubectl rollout status deployment/backend --namespace=${K8S_NAMESPACE}
                    '''
                }
            }
        }
    }
    post {
        success {
            echo "Deployment successful!"
        }
        failure {
            echo "Something went wrong with the pipeline."
        }
    }
}
