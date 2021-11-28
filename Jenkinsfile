#!groovy

pipeline {
  agent { dockerfile true }

    stage('Build Image') {
      steps {
        docker.build("austinbaugh/utopia-data-producer-base:${env.BUILD_ID} -f base.Dockerfile")
        docker.build("austinbaugh/utopia-data-producer:${env.BUILD_ID}")
      }
    }
  }
}
