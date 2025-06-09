pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'}
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                echo 'Cloning Github repo to Jenkins..........'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/chan4kum/hotel_reservation.git']])
            }

        }

        stage('Setting Up Our Virtual Environment and installing dependencies'){
            steps{
                echo 'Setting Up Our Virtual Environment and installing dependencies..........'
                sh '''
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }

        }

    }
}