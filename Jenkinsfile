#!/usr/bin/env groovy

pipeline {
    agent any

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
        stage('UnitTest') {
            agent {label 'master'}
            steps {
                ansiColor('xterm') {
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
            agent { label 'raspberry-sensors' }
            steps {
                ansiColor('xterm') {
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
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
