pipeline {
  agent any

  options {
    skipDefaultCheckout()
  }

  tools {
    git 'Default'           // matches the Git installation name in Global Tool Config
  }

  environment {
    VENV_DIR    = 'venv'
    GCP_PROJECT = 'project-mlops-467111'
    GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
  }

  stages {

    stage('Checkout Source') {
      steps {
        git(
          url: 'https://github.com/chan4kum/hotel_reservation.git',
          branch: 'main',
          credentialsId: 'github-token'
        )
      }
    }

    stage('Setup & Test') {
      steps {
        sh '''
          set -eux
          python -m venv ${VENV_DIR}
          . ${VENV_DIR}/bin/activate
          pip install --upgrade pip
          pip install -e .
          pytest --maxfail=1 --disable-warnings -q
        '''
      }
    }

    stage('Build & Push Image') {
      steps {
        withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
          retry(2) {
            sh '''
              set -eux

              export PATH=$PATH:${GCLOUD_PATH}
              gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
              gcloud config set project ${GCP_PROJECT}

              # Configure Docker for Artifact Registry
              gcloud auth configure-docker ${AREGION} --quiet

              # Buildx for linux/amd64
              docker buildx create --use --driver docker-container
              docker buildx build \
                --platform linux/amd64 \
                -t ${IMAGE_URI} \
                --push .
            '''
          }
        }
      }
    }

    stage('Deploy to Cloud Run') {
      steps {
        withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
          retry(2) {
            sh '''
              set -eux

              export PATH=$PATH:${GCLOUD_PATH}
              gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
              gcloud config set project ${GCP_PROJECT}
              gcloud config set run/region ${REGION}
              gcloud config set run/platform managed

              gcloud run deploy ml-project \
                --image=${IMAGE_URI} \
                --region=${REGION} \
                --platform=managed \
                --allow-unauthenticated \
                --quiet

              # Fetch and echo URL
              URL=$(gcloud run services describe ml-project \
                --format="value(status.url)")
              echo "Service URL: ${URL}"
            '''
          }
        }
      }
    }

  } // stages
}
