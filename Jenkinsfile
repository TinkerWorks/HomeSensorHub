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
