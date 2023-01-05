#!/usr/bin/env groovy

String daily_cron_string = BRANCH_NAME == "master" ? "@daily" : ""

pipeline {
    agent {
        kubernetes {
            yamlFile 'kubepods.yaml'
            defaultContainer 'python'
        }
    }
    options {
        timeout(time: 10, unit: 'MINUTES')
    }

    triggers { cron(daily_cron_string) }

    stages {
        stage('flake8') {
            steps{
                container('flake8') {
                    sh "flake8"
                }
            }
        }

        stage('pylint duplication') {
            steps{
                container('pylint') {
                    sh "pylint --disable=all --enable=duplicate-code homesensorhub"
                }
            }
        }

        stage('Testing') {
            parallel {
                stage('Local Test') {
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
                            sh "nose2 --with-coverage --junit-xml"
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
