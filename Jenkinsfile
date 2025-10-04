pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }
    
    environment {
        PROJECT_NAME = '3d-ddf'
        PYTHON = 'python3'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📦 Checking out repository...'
                checkout scm
            }
        }
        
        stage('Validate Taxonomy') {
            steps {
                echo '🔍 Validating project taxonomy...'
                sh '''
                    ${PYTHON} scripts/validate_taxonomy.py
                '''
            }
        }
        
        stage('Check Broken Links') {
            steps {
                echo '🔗 Checking for broken links...'
                sh '''
                    ${PYTHON} scripts/validate_links.py
                '''
            }
        }
        
        stage('Validate JSON') {
            steps {
                echo '📄 Validating JSON files...'
                sh '''
                    ${PYTHON} scripts/validate_json.py
                '''
            }
        }
        
        stage('Check File Sizes') {
            steps {
                echo '📊 Checking file sizes...'
                sh '''
                    ${PYTHON} scripts/validate_file_sizes.py
                '''
            }
        }
        
        stage('Check Hardcoded Paths') {
            steps {
                echo '🔍 Checking for hardcoded paths...'
                sh '''
                    ${PYTHON} scripts/validate_paths.py
                '''
            }
        }
        
        stage('Generate Reports') {
            steps {
                echo '📈 Generating validation reports...'
                sh '''
                    ${PYTHON} scripts/generate_report.py
                '''
            }
        }
    }
    
    post {
        success {
            echo '✅ All validations passed!'
            // Optional: Send notification
            // emailext subject: "✅ ${PROJECT_NAME} Build #${BUILD_NUMBER} - SUCCESS",
            //          body: "All taxonomy validations passed.",
            //          to: "team@example.com"
        }
        
        failure {
            echo '❌ Validation failed!'
            // Optional: Send notification
            // emailext subject: "❌ ${PROJECT_NAME} Build #${BUILD_NUMBER} - FAILED",
            //          body: "Taxonomy validation failed. Check console output.",
            //          to: "team@example.com"
        }
        
        always {
            echo '🧹 Cleaning up...'
            // Archive validation reports
            archiveArtifacts artifacts: 'reports/*.txt', allowEmptyArchive: true
            // Clean workspace if needed
            // cleanWs()
        }
    }
}
