pipeline {
    agent any

    environment {
        SCRIPT = 'napalm_backup.py'
        PATH = "${HOME}/.local/bin:${env.PATH}"
        PYTHONPATH = "${HOME}/.local/lib/python3.10/site-packages"
    }

    stages {
        stage('Install pip and NAPALM') {
            steps {
                sh '''
                    echo "[INFO] Checking for pip..."
                    if ! command -v pip3 > /dev/null; then
                        echo "[INFO] pip3 not found. Installing..."
                        wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py
                        python3 get-pip.py --user
                    fi

                    echo "[INFO] Installing NAPALM and dependencies..."
                    ~/.local/bin/pip3 install --user --upgrade pip
                    ~/.local/bin/pip3 install --user napalm netmiko
                '''
            }
        }

        stage('Run NAPALM Backup Script') {
            environment {
                CISCO_CREDS = credentials('cisco-ssh-creds')
            }
            steps {
                sh '''
                    echo "[INFO] Executing NAPALM backup script..."
                    export CISCO_CREDS_USR="${CISCO_CREDS_USR}"
                    export CISCO_CREDS_PSW="${CISCO_CREDS_PSW}"

                    python3 ${SCRIPT}
                '''
            }
        }

        stage('List Backup Files') {
            steps {
                sh 'ls -lh backups || echo "[WARN] No backup directory found."'
            }
        }

        stage('Archive Config Backups') {
            steps {
                script {
                    def backups = sh(script: "ls backups/*.txt 2>/dev/null || true", returnStdout: true).trim()
                    if (backups) {
                        echo "[INFO] Archiving configuration backups..."
                        archiveArtifacts artifacts: 'backups/*.txt', allowEmptyArchive: false
                    } else {
                        echo "[WARNING] No backup files to archive."
                    }
                }
            }
        }
    }

    post {
        success {
            echo '[✅] NAPALM backup pipeline completed successfully.'
        }
        failure {
            echo '[❌] Pipeline failed. Check logs above for details.'
        }
        always {
            echo '[ℹ️] Pipeline execution complete.'
        }
    }
}
