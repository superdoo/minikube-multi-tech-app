pipeline {
    agent any

    environment {
        DOCKER_IMAGE_BACKEND = 'backend:latest'
        DOCKER_IMAGE_FRONTEND = 'frontend:latest'
        K8S_CLUSTER = 'minikube'
        K8S_NAMESPACE = 'default'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out the repository"
                git branch: 'main', url:'https://github.com/superdoo/minikube-multi-tech-app.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                   withCredentials([usernamePassword(credentialsId: 'DOCKER_USER', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')])  {
                        def backendImage = "${DOCKER_USER}/${DOCKER_IMAGE_BACKEND}"
                        def frontendImage = "${DOCKER_USER}/${DOCKER_IMAGE_FRONTEND}"
                        echo "Building backend: ${backendImage}"
                        docker.build(backendImage, 'backend')
                        echo "Building frontend: ${frontendImage}"
                        docker.build(frontendImage, 'frontend')
                    }
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials',
                                                      usernameVariable: 'DOCKER_USER',
                                                      passwordVariable: 'DOCKER_PASS')]) {
                        def backendImage = "${DOCKER_USER}/${DOCKER_IMAGE_BACKEND}"
                        def frontendImage = "${DOCKER_USER}/${DOCKER_IMAGE_FRONTEND}"
                        sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${backendImage}
                        docker push ${frontendImage}
                        docker logout
                        """
                    }
                }
            }
        }

        stage('Deploy Backend to Kubernetes') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials',
                                                      usernameVariable: 'DOCKER_USER',
                                                      passwordVariable: 'DOCKER_PASS')]) {
                        def backendImage = "${DOCKER_USER}/${DOCKER_IMAGE_BACKEND}"
                        sh """
                        kubectl set image deployment/backend backend=${backendImage} --namespace=${K8S_NAMESPACE}
                        kubectl rollout status deployment/backend --namespace=${K8S_NAMESPACE}
                        """
                    }
                }
            }
        }

        stage('Deploy Frontend to Kubernetes') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials',
                                                      usernameVariable: 'DOCKER_USER',
                                                      passwordVariable: 'DOCKER_PASS')]) {
                        def frontendImage = "${DOCKER_USER}/${DOCKER_IMAGE_FRONTEND}"
                        sh """
                        kubectl set image deployment/frontend frontend=${frontendImage} --namespace=${K8S_NAMESPACE}
                        kubectl rollout status deployment/frontend --namespace=${K8S_NAMESPACE}
                        """
                    }
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
