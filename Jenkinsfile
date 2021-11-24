pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'docker build . -t austinbaugh/utopia-data-producer:0.0.3-SNAPSHOT' 
            }
        }
    }
}


