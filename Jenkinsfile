pipeline {
    agent any

    environment {
        SCRIPT = 'get_uptime.py'
        PATH = "${HOME}/.local/bin:${env.PATH}"
        PYTHONPATH = "${HOME}/.local/lib/python3.10/site-packages"
    }

    stages {
        stage('Install Nornir and Dependencies') {
            steps {
                sh '''
                    echo "[INFO] Installing Python packages..."
                    if ! command -v pip3 > /dev/null; then
                        echo "[INFO] pip3 not found. Installing..."
                        wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py
                        python3 get-pip.py --user
                    fi

                    ~/.local/bin/pip3 install --user nornir nornir-netmiko nornir-utils netmiko
                '''
            }
        }

        stage('Run Nornir Script') {
            environment {
                CISCO_CREDS = credentials('cisco-ssh-creds')
            }
            steps {
                sh '''
                    echo "[INFO] Running Nornir uptime collection..."
                    export CISCO_CREDS_USR="${CISCO_CREDS_USR}"
                    export CISCO_CREDS_PSW="${CISCO_CREDS_PSW}"

                    python3 ${SCRIPT}
                '''
            }
        }

        stage('Check for Output Files') {
            steps {
                sh '''
                    echo "[INFO] Checking for generated uptime files..."
                    ls -lh *_uptime.txt || echo "[WARNING] No uptime output files were generated."
                '''
            }
        }

        stage('Archive Uptime Results') {
            steps {
                script {
                    def results = sh(script: "ls *_uptime.txt 2>/dev/null || true", returnStdout: true).trim()
                    if (results) {
                        echo "[INFO] Archiving uptime results..."
                        archiveArtifacts artifacts: '*_uptime.txt', allowEmptyArchive: false
                    } else {
                        echo "[WARNING] No files to archive."
                    }
                }
            }
        }
    }

    post {
        failure {
            echo "[ERROR] Pipeline failed."
        }
        always {
            echo "[INFO] Pipeline complete."
        }
    }
}
