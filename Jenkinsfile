pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "mlops-460914"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/chan4kum/hotel_reservation.git']])
                }
            }
        }

        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and Pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing Docker Image to Artifact Registry...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        # Activate service account
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        # Set the project
                        gcloud config set project ${GCP_PROJECT}

                        # Configure Docker to authenticate with Artifact Registry
                        gcloud auth configure-docker us-docker.pkg.dev --quiet

                        # Build and tag the Docker image
                        docker build -t us-docker.pkg.dev/${GCP_PROJECT}/gcr/ml-project:latest .

                        # Push the Docker image to Artifact Registry
                        docker push us-docker.pkg.dev/${GCP_PROJECT}/gcr/ml-project:latest
                        '''
                    }
                }
            }
        }


        // stage('Deploy to Google Cloud Run'){
        //     steps{
        //         withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
        //             script{
        //                 echo 'Deploy to Google Cloud Run.............'
        //                 sh '''
        //                 export PATH=$PATH:${GCLOUD_PATH}


        //                 gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

        //                 gcloud config set project ${GCP_PROJECT}

        //                 gcloud run deploy ml-project \
        //                     --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
        //                     --platform=managed \
        //                     --region=us-central1 \
        //                     --allow-unauthenticated
                            
        //                 '''
        //             }
        //         }
        //     }
        // }
        
    }
}