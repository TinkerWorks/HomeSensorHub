#!/usr/bin/env groovy

pipeline {
    agent any

    stages {
        stage('... Environment preparation ...') {
            steps {
                echo "... preparing python environment required for project ..."
                sh "make prepare-test"
            }
        }
        stage('UnitTest') {
            steps {
                ansiColor('xterm') {
                    echo '... Testing ...'
                    sh "make nosetest"
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
