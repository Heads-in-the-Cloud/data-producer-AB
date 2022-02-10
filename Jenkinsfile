#!groovy

def getCommitSha() {
    return sh(
        script: "git rev-parse HEAD",
        returnStdout: true
    ).trim()
}

void setBuildStatus(String message, String state) {
    repoUrl = sh(
        script: "git config --get remote.origin.url",
        returnStdout: true
    ).trim()

    step([
        $class: "GitHubCommitStatusSetter",
        reposSource: [$class: "ManuallyEnteredRepositorySource", url: repoUrl],
        commitShaSource: [$class: "ManuallyEnteredShaSource", sha: getCommitSha()],
        errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
        statusResultSource: [
            $class: "ConditionalStatusResultSource",
            results: [[$class: "AnyBuildResult", message: message, state: state]]
        ]
    ]);
}

pipeline {
    agent any

    environment {
        PROJECT_ID = "AB-utopia"
        VERSION = '0.0.5'

        SONARQUBE_ID = tool name: 'SonarQubeScanner-4.6.2'

        image = null
        built = false
    }

    stages {

        stage('SonarQube Analysis') {
            steps {
                withCredentials([
                    string(credentialsId: "SonarQube Token", variable: 'SONAR_TOKEN')
                ]) {
                    sh """
                        ${SONARQUBE_ID}/bin/sonar-scanner \
                            -Dsonar.login=$SONAR_TOKEN \
                            -Dsonar.projectKey=$PROJECT_ID-data-producer \
                            -Dsonar.host.url=http://jenkins2.hitwc.link:9000 \
                            -Dsonar.sources=./app
                    """
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    sh "docker context use default"
                    def image_label = "${PROJECT_ID.toLowerCase()}-data-producer"
                    image = docker.build(image_label)
                    sh "docker tag $image_label $image_label:${getCommitSha().substring(0, 7)}"
                    sh "docker tag $image_label $image_label:$VERSION"
                }
            }
        }

        stage('Push to registry') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "jenkins",
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    script {
                        def region = sh(
                            script:'aws configure get region',
                            returnStdout: true
                        ).trim()
                        def aws_account_id = sh(
                            script:'aws sts get-caller-identity --query "Account" --output text',
                            returnStdout: true
                        ).trim()
                        def ecr_uri = "${aws_account_id}.dkr.ecr.${region}.amazonaws.com"
                        docker.withRegistry(
                            "https://$ecr_uri/${PROJECT_ID.toLowerCase()}-data-producer",
                            "ecr:$region:jenkins"
                        ) {
                            image.push('latest')
                        }
                    }
                }
            }

            post {
                cleanup {
                    script {
                        def image_label = "${PROJECT_ID.toLowerCase()}-data-producer"
                        sh "docker rmi $image_label:${getCommitSha().substring(0, 7)}"
                        sh "docker rmi $image_label:$VERSION"
                        sh "docker rmi $image_label:latest"
                    }
                }
            }
        }

        stage("Deploy to EKS") {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "jenkins",
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    script {
                        def region = sh(
                            script: 'aws configure get region',
                            returnStdout: true
                        ).trim()
                        sh "aws eks --region $region update-kubeconfig --name $PROJECT_ID"
                        def aws_account_id = sh(
                            script: 'aws sts get-caller-identity --query "Account" --output text',
                            returnStdout: true
                        ).trim()
                        def image_url = "${aws_account_id}.dkr.ecr.${region}.amazonaws.com/${PROJECT_ID.toLowerCase()}-data-producer"
                        sh "kubectl -n microservices set image deployments/data-producer data-producer=https://$image_url:${getCommitSha().substring(0, 7)}"
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                if(built) {
                    setBuildStatus("Build complete", "SUCCESS")
                } else {
                    setBuildStatus("Build failed", "FAILURE")
                }
            }
        }
    }
}
