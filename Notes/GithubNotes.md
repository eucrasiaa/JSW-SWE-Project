## setup repository
1. setup
    - `git init .`
    - `git remote add origin git@github.com:eucrasiaa/JSW-SWE-Project.git`
    - `git remote set-url origin git@github.com:eucrasiaa/JSW-SWE-Project.git`

2. verify
- `git remote -v`
- should show:
    `origin	git@github.com:eucrasiaa/JSW-SWE-Project.git (fetch)
    origin	git@github.com:eucrasiaa/JSW-SWE-Project.git (push)`

3. validate ssh connection
- if you dont have ssh keys setup, do that first:
    - https://docs.github.com/en/authentication/connecting-to-github-with-ssh
    - ~ 1. gen key via ssh-keygen
    - ~ 2. add key to ssh agent on your machine
    - ~ 3. add public key to github account
    - ~ 4. test connection
- `ssh -T git@github.com
- should show:
    `Hi (USERNAME)! You've successfully authenticated, but GitHub does not provide shell access.`

4. quick git refresher:
    - ALWAYS check which branch you are on!!!
    - `git status` to check status of files, staged, unstaged, untracked, etc
    - `git pull` to pull latest changes from remote repository
        - do this before working on any changes
    - `git add <file>` to stage a file for commit
        - `git add .` to stage all files in the current & subdirectories
    - `git commit -m "commit message"` to commit a stage 
        - ALWAYS write a meaningful commit, briefly describe what you did
    - `git push` to push your commits to the remote repository
    - Branches:
        - basic git-flow style setup:
            - `main` branch = production ready, stable, fully tested verified
            - `prod` branch = development branch. features merged to here, should mostly be stable
            - `feature` branches = we branch off prod to work on features, then merge back to prod when done. 
                - naming convention: `feature/<feature-name>`
                - example: `feature/check-in-html`
        - create branch with `git checkout -b <branch-name>`
        - switch branches with `git checkout <branch-name>`
        - list branches with `git branch`

5. setup:
    - checkout prod branch: `git checkout prod`
    - implementing features? make new branch!
        - create feature branch: `git checkout -b feature/<feature-name>`
        - example: `git checkout -b feature/check-in-html`

    - push feature branch to remote: `git push -u origin feature/<feature-name>`
        - example: `git push -u origin feature/check-in-html`
    
    - when review passes, merge to prod:
        - switch to prod: `git checkout prod`
        - merge feature branch: `git merge feature/<feature-name>`
        - example: `git merge feature/check-in-html`
    - after merging, push changes to remote: `git push`

