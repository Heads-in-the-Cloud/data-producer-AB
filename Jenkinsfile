#!groovy
node {
  def base_image, image

  stage('Clone repository') {
    checkout scm
  }

  stage('Build images') {
    base_image = docker.build("austinbaugh/utopia-data-producer-base:${env.BUILD_ID} -f base.Dockerfile")
    image = docker.build("austinbaugh/utopia-data-producer:${env.BUILD_ID}")
  }

  stage('Push images') {
    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
      base_image.push("${env.BUILD_NUMBER}")
      base_image.push("latest")

      image.push("${env.BUILD_NUMBER}")
      image.push("latest")
    }
  }
}
