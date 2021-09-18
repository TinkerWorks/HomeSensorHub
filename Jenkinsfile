#!/usr/bin/env groovy

pipeline {
    agent none
    options {
        timeout(time: 10, unit: 'MINUTES')
    }
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
                            junit 'nosetests.xml'
                        }
                    }
                }
                stage('IntegrationTest') {
                    agent {
                        label 'raspberry-sensors'
                    }
                    environment {
                        PATH = "$HOME/.local/bin:$PATH"
                    }
                    steps {
                        ansiColor('xterm') {
                            echo '... Environment DEVICE ...'
                            sh "env"
                            echo '... Cleaning ...'
                            sh "git clean -xdf"
                            echo '... Testing ...'
                            sh "make real-nosetest"
                        }
                    }
                    post {
                        always {
                            junit 'nosetests.xml'
                        }
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploy ....'
            }
        }
    }
}
