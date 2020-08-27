#!/usr/bin/env groovy

pipeline {
    agent {
        label 'master'
    }
    options {
        timeout(time: 10, unit: 'MINUTES')
    }
    stages {
        stage('... Environment preparation ...') {
            steps {
                echo " ... cleaning up git repo ... "
                sh "git clean -xdf"
            }
        }
        stage('Testing') {
            parallel {
                stage('UnitTest') {
                    agent {
                        label 'master'
                    }
                    environment {
                        PATH = "$HOME/.local/bin:$PATH"
                    }
                    steps {
                        ansiColor('xterm') {
                            echo '... Environment HOST ...'
                            sh "env"
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
                echo 'Deploying....'
            }
        }
    }
}
