#!/usr/bin/env groovy

// Orchestrator pipeline for the "monorepo".
//
// Runs on two kinds of head, discovered by the GitHub Branch Source plugin:
//   - Pull requests          (CHANGE_ID / CHANGE_TARGET are set)
//   - Merge-queue branches   (gh-readonly-queue/*, a plain branch, no CHANGE_*)
//
// For a merge-queue branch the checkout already contains the base branch plus
// this PR plus any PRs ahead of it in the queue, so building it here validates
// exactly the state that is about to land on the base branch.

// Return the list of changed files relative to the base branch.
// PR build: diff against CHANGE_TARGET. Merge-queue / branch build: no
// CHANGE_TARGET, so diff against main.
def changedPaths() {
    def base = env.CHANGE_TARGET ?: 'main'
    sh "git fetch -q origin ${base}"
    return sh(returnStdout: true, script: "git diff --name-only origin/${base}...HEAD").trim()
}

pipeline {
    agent any   // swap for a docker-capable label, e.g. agent { label 'docker' }
    options { timestamps() }

    stages {
        stage('Detect changes') {
            steps {
                script {
                    env.CHANGED = changedPaths()
                    echo "BRANCH_NAME   = ${env.BRANCH_NAME}"
                    echo "CHANGE_ID     = ${env.CHANGE_ID ?: 'none (branch / merge_group build)'}"
                    echo "CHANGE_TARGET = ${env.CHANGE_TARGET ?: 'none (diffing against main)'}"
                    echo "Changed files:\n${env.CHANGED}"
                }
            }
        }

        stage('Build & test sub-projects') {
            parallel {
                stage('simple_calculator') {
                    when { expression { env.CHANGED.contains('simple_calculator/') } }
                    steps { script { buildAndTest('simple_calculator') } }
                }
                stage('advanced_calculator') {
                    when { expression { env.CHANGED.contains('advanced_calculator/') } }
                    steps { script { buildAndTest('advanced_calculator') } }
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: '*/reports/*.xml'
            sh 'docker image prune -f >/dev/null 2>&1 || true'
        }
    }
}

// Build the sub-project image and run its unit tests inside the container.
// The sub-project Dockerfile's CMD runs pytest and writes JUnit XML to
// /app/reports, which we bind-mount out so the parent can publish it.
def buildAndTest(String service) {
    // Tag per commit so parallel queue-branch builds do not collide.
    // Build numbers are per-branch, so every branch's first build is #1.
    def image = "${service}:${env.GIT_COMMIT.take(12)}"
    sh """
        docker build -t ${image} ${service}
        mkdir -p ${service}/reports
        docker run --rm -v "\$PWD/${service}/reports:/app/reports" ${image}
        docker rmi ${image} || true
    """
}
