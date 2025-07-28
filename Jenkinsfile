pipeline {
  agent any

  environment {
    // Virtualenv
    VENV_DIR  = 'venv'

    // GCP Settings
    GCP_PROJECT    = 'project-mlops-467111'
    REGION         = 'us-central1'
    AREGION        = 'us-docker.pkg.dev'
    REPO           = "${GCP_PROJECT}/ml-repo"
    TAG            = "${env.BUILD_NUMBER}"
    IMAGE_URI      = "${AREGION}/${REPO}/ml-project:${TAG}"

    // gcloud path if needed
    GCLOUD_PATH    = '/var/jenkins_home/google-cloud-sdk/bin'
  }

  stages {

    stage('Checkout') {
      steps {
        echo 'Cloning source...'
        checkout([
          $class: 'GitSCM',
          branches: [[name: '*/main']],
          userRemoteConfigs: [[
            url: 'https://github.com/chan4kum/hotel_reservation.git',
            credentialsId: 'github-token'
          ]]
        ])
      }
    }

    stage('Test') {
      steps {
        echo 'Running tests...'
        sh '''
          set -eux
          python -m venv ${VENV_DIR}
          . ${VENV_DIR}/bin/activate
          pip install --upgrade pip
          pip install -e .
          pytest --junitxml=reports/results.xml
        '''
        junit 'reports/results.xml'
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
