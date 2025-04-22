pipeline {
    agent any 

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-key')
        APP_NAME = "aarooon16045/photo-album"
        CONTAINER_NAME = "photo-album"
	    IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages { 
        stage('SCM Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'git-key',
                    url: 'git@github.com:aaronesposito/photo-album.git'
            }
        }
        stage('Build docker images') {
            steps {  
                sh """
                export IMAGE_TAG=$BUILD_NUMBER
                docker build -t ${APP_NAME}:${BUILD_NUMBER} .
                """
            }
        }
        
        stage('login to dockerhub') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }
        
         stage('push image') {
            steps {
                sh """
                docker push ${APP_NAME}:${BUILD_NUMBER}
                """
            }
        }
    
        stage('Deploy to Server') {
            steps {
                script {
                    sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker pull ${APP_NAME}:${BUILD_NUMBER}
                    docker run -p 5010:5000 --name ${CONTAINER_NAME} ${APP_NAME}:${BUILD_NUMBER}
                    """
                }
            }
        }
    }
}