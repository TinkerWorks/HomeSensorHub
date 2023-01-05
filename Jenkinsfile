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
                            yamlFile 'kubepods.yaml'
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
