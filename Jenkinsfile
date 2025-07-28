pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "project-mlops-467111"
        // Ensure GCLOUD_PATH points to the directory containing gcloud executable
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        // Define the full Artifact Registry image path as an environment variable
        // DOCKER_IMAGE_NAME = "us-docker.pkg.dev/${GCP_PROJECT}/gcr/ml-project:latest"
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
                        # Add gcloud to PATH for the current shell
                        export PATH=$PATH:${GCLOUD_PATH}

                        # Check gcloud version (good for debugging path issues)
                        gcloud --version

                        # Explicitly set the service account and project for this operation
                        # gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS} --project=${GCP_PROJECT}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        # Ensure the project is set for subsequent gcloud commands
                        gcloud config set project ${GCP_PROJECT}

                        # IMPORTANT: Configure Docker to use gcloud as a credential helper.
                        # This command writes to ~/.docker/config.json of the user running this process.
                        # Using --quiet to suppress interactive prompts.
                        # gcloud auth configure-docker us-docker.pkg.dev --quiet
                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                        # Correct
                        docker push gcr.io/project-mlops-467111/ml-project:latest


                        # Verify Docker login status (optional, but helpful for debugging)
                        # This might show "Login Succeeded" if configured correctly.
                        # You might need to install 'docker-credential-gcloud' for this specific check to work cleanly.
                        # If you see "login succeeded" it means creds are being picked up.
                        # docker login us-docker.pkg.dev

                        # Build the Docker image with the fully qualified tag
                        # echo "Building Docker image: ${DOCKER_IMAGE_NAME}"
                        # docker build -t ${DOCKER_IMAGE_NAME} .

                        # Push the Docker image to Artifact Registry
                        # echo "Pushing Docker image: ${DOCKER_IMAGE_NAME}"
                        #docker push ${DOCKER_IMAGE_NAME}
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