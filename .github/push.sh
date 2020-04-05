#!/bin/sh

setup_git() {
  git config --global user.email "gustrimaille@yahoo.fr"
  git config --global user.name "3Liz bot"
}

commit_website_files() {
  git checkout -b master
  git add ../QuickOSM/i18n/*.qm
  git commit --message "Update translations from Transifex version : $TRAVIS_TAG"
}

upload_files() {
  git remote add origin-push https://"${GH_TOKEN}"@github.com/"${TRAVIS_REPO_SLUG}".git > /dev/null 2>&1
  git push --quiet --set-upstream origin-push master
}

setup_git
commit_website_files
upload_files
