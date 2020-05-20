#!/usr/bin/env groovy

pipeline {
    agent any

    stages {
        stage('... Environment preparation ...') {
            steps {
                echo "... preparing python environment required for project ..."
                sh "pip3 install -r requirements.txt"
                sh "pip3 install -r test/requirements.txt"
            }
        }
        stage('UnitTest') {
            steps {
                ansiColor('xterm') {
                    echo '... Testing ...'
                    sh "~/.local/bin/nosetests . --with-xunit"
                }
            }
            post {
                always {
                    junit 'nosetests.xml'
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
