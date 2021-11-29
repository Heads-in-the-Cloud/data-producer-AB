#!groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh "docker build . -t austinbaugh/utopia-data-producer:${env.BUILD_ID}"
            }
        }
    }
}
