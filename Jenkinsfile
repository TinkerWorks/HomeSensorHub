#!/usr/bin/env groovy

String daily_cron_string = BRANCH_NAME == "master" ? "@daily" : ""

pipeline {
    agent none
    options {
        timeout(time: 10, unit: 'MINUTES')
    }

    triggers { cron(daily_cron_string) }

    stages {
        stage('Testing') {
            parallel {
                stage('UnitTest') {
                    agent {
                        kubernetes {
                            yaml '''
apiVersion: v1
kind: Pod
metadata:
  label: pythontest
  namespace: jenkins
spec:
  containers:
  - name: pythontest
    image: python:latest
    command:
    - sleep
    args:
    - infinity
'''
                            defaultContainer 'pythontest'
                        }
                    }
                    environment {
                        PATH = "$HOME/.local/bin:$PATH"
                    }
                    steps {
                        ansiColor('xterm') {
                            sh "env"
                            sh "pip install -r requirements.txt"
                            sh "pip install -r tests/requirements.txt"
                            echo '... Cleaning ...'
                            sh "git clean -xdf"
                            echo '... Testing ...'
                            sh "make mock-nosetest"
                        }
                    }
                    post {
                        always {
                            junit 'nose2-junit.xml'
                        }
                    }
                }
            }
        }
    }
}
