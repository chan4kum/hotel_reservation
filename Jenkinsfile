pipeline{
    agent any

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                echo 'Cloning Github repo to Jenkins..........'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/chan4kum/hotel_reservation.git']])
            }

        }

    }
}