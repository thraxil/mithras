workflow "on pull request merge, delete the branch" {
  on = "pull_request"
  resolves = ["branch cleanup"]
}

action "branch cleanup" {
  uses = "jessfraz/branch-cleanup-action@master"
  secrets = ["GITHUB_TOKEN"]
}

workflow "run tests" {
  on = "push"
  resolves = ["deploy"]
}

action "Build docker image" {
  uses = "actions/docker/cli@master"
  args = "build -t thraxil/mithras:$GITHUB_SHA ."
}

action "Deploy branch filter" {
  needs = "Build docker image"
  uses = "actions/bin/filter@master"
  args = "branch master"
}

action "docker login" {
  needs = "Deploy branch filter"
  uses = "actions/docker/login@master"
  secrets = ["DOCKER_USERNAME", "DOCKER_PASSWORD"]
}

action "docker push" {
  needs = ["docker login"]
  uses = "actions/docker/cli@master"
  args = ["push", "thraxil/mithras:$GITHUB_SHA"]
}

action "deploy" {
  needs = "docker push"
	uses = "thraxil/django-deploy-action@master"
	secrets = [
     "PRIVATE_KEY",
		 "PUBLIC_KEY",
		 "SENTRY_URL",
  ]
	env = {
    USER = "anders"
		APP = "mithras"
		WEB_HOSTS = "174.138.40.31 174.138.34.34"
  }
}
