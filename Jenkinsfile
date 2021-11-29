#!groovy

pipeline {
  agent any

  stages {
    stage('Build Image') {
      agent { dockerfile true }

      steps {
        docker.build("austinbaugh/utopia-data-producer-base:${env.BUILD_ID} -f base.Dockerfile")
        docker.build("austinbaugh/utopia-data-producer:${env.BUILD_ID}")
      }
    }
  }
}
