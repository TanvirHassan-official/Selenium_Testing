# Git & GitHub Complete Reference Guide

---

## Table of Contents

1. [What is Version Control?](#1-what-is-version-control)
2. [Git vs GitHub](#2-git-vs-github)
3. [Installation & First-Time Setup](#3-installation--first-time-setup)
4. [Setting Up GitHub Account & SSH](#4-setting-up-github-account--ssh)
5. [Core Concepts](#5-core-concepts)
6. [The Three States of Git](#6-the-three-states-of-git)
7. [Starting a Repository](#7-starting-a-repository)
8. [Staging Changes — `git add`](#8-staging-changes--git-add)
9. [Saving Snapshots — `git commit`](#9-saving-snapshots--git-commit)
10. [Inspecting the Repository](#10-inspecting-the-repository)
11. [Comparing & Undoing Changes](#11-comparing--undoing-changes)
12. [Branching](#12-branching)
13. [Merging](#13-merging)
14. [Merge Conflicts](#14-merge-conflicts)
15. [Branching Strategies](#15-branching-strategies)
16. [Remote Repositories](#16-remote-repositories)
17. [Pull Requests](#17-pull-requests)
18. [Forking & Open Source Contribution](#18-forking--open-source-contribution)
19. [GitHub Beyond Code](#19-github-beyond-code)
20. [.gitignore](#20-gitignore)
21. [Advanced Commands](#21-advanced-commands)
22. [Disconnecting GitHub from Your Local Device](#22-disconnecting-github-from-your-local-device)
23. [Best Practices](#23-best-practices)
24. [Cheat Sheet](#24-cheat-sheet)

---

## 1. What is Version Control?

**The Problem** — Without version control, you end up with this nightmare:

```
report_final.docx
report_final_v2.docx
report_FINAL_FINAL.docx
report_FINAL_FINAL_fixed.docx
```

**The Solution** — A Version Control System (VCS) tracks every change to your files over time. You can:

- Revert to any previous version
- See who changed what and when
- Collaborate without overwriting each other's work
- Work on features in parallel

---

## 2. Git vs GitHub

| | Git | GitHub |
|---|---|---|
| **What it is** | A distributed version control system | A cloud platform built around Git |
| **Runs** | Locally on your machine | On the internet (Microsoft's servers) |
| **Purpose** | Tracks changes in a repository | Hosts repos + adds collaboration features |
| **Works offline?** | Yes | No |
| **Created by** | Linus Torvalds (2005) | Founded 2008, acquired by Microsoft 2018 |
| **Cost** | Free & open source | Free for public repos |
| **Key features** | Branching, commits, history | Pull Requests, Issues, Actions, Pages |

> **Summary:** Git is the tool. GitHub is the service. You can use Git without GitHub, but GitHub requires Git.

---

## 3. Installation & First-Time Setup

### Installation

**Windows:** Download from [git-scm.com](https://git-scm.com)

**macOS:**
```bash
brew install git
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install git
```

**Verify installation:**
```bash
git --version
```

---

### First-Time Configuration

Run these once after installing Git. These values are attached to every commit you make.

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (use the same one as your GitHub account)
git config --global user.email "you@email.com"

# Set default branch name to 'main' (modern standard)
git config --global init.defaultBranch main

# Set preferred editor (optional; default is vim)
git config --global core.editor "code --wait"   # VS Code
git config --global core.editor "nano"          # Nano

# View all your configuration settings
git config --list

# View a specific setting
git config user.name
```

---

## 4. Setting Up GitHub Account & SSH

### Create a GitHub Account

1. Go to [github.com/signup](https://github.com/signup)
2. Enter your email, password, and username
3. Verify your account via email
4. Choose the **Free** plan

> **Student Tip:** Apply for the GitHub Student Developer Pack at [education.github.com](https://education.github.com) for free Pro features!

---

### SSH Key Setup (Recommended)

SSH lets you push/pull without typing your password every time. Set it up once and you're done.

**Step 1 — Generate a key pair (works on Windows Git Bash, macOS, and Linux):**
```bash
ssh-keygen -t ed25519 -C "you@email.com"
```
Press Enter to accept the default file location. Optionally set a passphrase.

**Step 2 — Copy your public key:**

```bash
# macOS
cat ~/.ssh/id_ed25519.pub | pbcopy

# Linux
cat ~/.ssh/id_ed25519.pub

# Windows (Git Bash)
cat ~/.ssh/id_ed25519.pub | clip
```

**Step 3 — Add it to GitHub:**
Go to **GitHub → Settings → SSH and GPG Keys → New SSH Key**, paste your key, and save.

**Step 4 — Test the connection:**
```bash
ssh -T git@github.com
# Expected: Hi username! You've successfully authenticated...
```

---

## 5. Core Concepts

**Repository (Repo)**
A folder tracked by Git. Contains your project files plus a hidden `.git` directory that stores the entire change history.

**Working Directory**
The actual files you see and edit on your computer — your project folder as it currently looks.

**Staging Area (Index)**
A preparation zone. You "stage" specific changes before committing them. Think of it as a draft of your next snapshot.

**Commit**
A permanent snapshot of staged changes. Each commit has:
- A unique ID (SHA hash, e.g. `a1b2c3d`)
- Author name and email
- Timestamp
- A commit message

**Branch**
An independent line of development. The default branch is called `main`.

**Remote**
A copy of your repository hosted on a server (like GitHub).

**HEAD**
A pointer to your current position in the repository — usually the latest commit on the active branch.

---

## 6. The Three States of Git

Every file in your project is in one of three states:

```
Working Directory  →(git add)→  Staging Area  →(git commit)→  Local Repository
   (Modified)                    (Staged)                        (Committed)
```

| State | Meaning |
|---|---|
| **Modified** | You changed the file but haven't staged it yet |
| **Staged** | Marked to go into the next commit snapshot |
| **Committed** | Safely stored in your local database |

---

## 7. Starting a Repository

### `git init` — Start from Scratch

```bash
# Create a new project folder
mkdir my-project
cd my-project

# Initialize Git tracking
git init
# Output: Initialized empty Git repository in /path/to/my-project/.git/
```

This creates a hidden `.git` folder — your repository is born!

---

### `git clone` — Copy an Existing Repo

```bash
# Clone using HTTPS
git clone https://github.com/username/project.git

# Clone using SSH (requires SSH setup from Section 4)
git clone git@github.com:username/project.git

# Clone into a custom folder name
git clone https://github.com/username/project.git my-folder

# Clone a specific branch only
git clone -b branch-name https://github.com/username/project.git
```

Cloning downloads the full repository including all history.

---

## 8. Staging Changes — `git add`

```bash
# Stage a specific file
git add index.html

# Stage multiple specific files
git add index.html style.css

# Stage an entire folder
git add src/

# Stage ALL changes in the current directory (use carefully!)
git add .

# Stage parts of a file interactively (advanced)
git add -p file.txt
```

> **Real-World Tip:** You've edited `index.html`, `style.css`, and created a `debug.log`. Use `git add index.html style.css` to stage only what matters — not `git add .` which would include the log file.

---

## 9. Saving Snapshots — `git commit`

```bash
# Standard commit with a message
git commit -m "Add login page"

# Stage all tracked files AND commit in one step
# (does NOT stage new/untracked files)
git commit -am "Update styles"

# Open the default editor to write a detailed message
git commit

# Amend the last commit (fix message or add forgotten files)
# Only do this BEFORE pushing!
git commit --amend -m "Corrected commit message"
```

### Writing Good Commit Messages

Use imperative mood — write what the commit *does*, not what you *did*.

```
✓ "Add user authentication middleware"
✓ "Fix #42: cart total rounding error"
✓ "Refactor database connection logic"
✗ "fixed stuff"
✗ "asdfgh"
✗ "changes"
✗ "final fix hopefully"
```

### Anatomy of a Commit

```
SHA Hash: a1b2c3d  |  Author: Jane Doe  |  Date: 2025-03-28  |  Message: "Add login page"
```

---

## 10. Inspecting the Repository

### `git status` — Current State

```bash
git status

# Short/compact output
git status -s
```

Example output:
```
On branch main
Changes to be committed:
  modified:   index.html
Changes not staged for commit:
  modified:   style.css
Untracked files:
  debug.log
```

---

### `git log` — Commit History

```bash
# Full log with all details
git log

# Compact one-line format
git log --oneline

# Visual branch graph
git log --graph --oneline

# Show last N commits
git log -5

# Show commits by a specific author
git log --author="Jane"

# Show commits that changed a specific file
git log -- filename.txt

# Show commits within a date range
git log --after="2024-01-01" --before="2024-12-31"
```

---

### `git show` — Inspect a Commit

```bash
# Show details of the latest commit
git show

# Show details of a specific commit
git show a1b2c3d
```

---

## 11. Comparing & Undoing Changes

### `git diff` — See What Changed

```bash
# Show unstaged changes (working directory vs staging area)
git diff

# Show staged changes (staging area vs last commit)
git diff --staged

# Compare two branches
git diff main feature-login

# Compare two specific commits
git diff a1b2c3d e4f5g6h
```

---

### Undoing Changes

```bash
# Discard changes in a file (restore to last commit)
git restore file.txt

# Unstage a file (keep changes in working directory)
git restore --staged file.txt

# Restore a deleted file
git restore deleted-file.txt
```

---

### Advanced Undo (Use with Caution!)

| Command | What it does | Safe for shared branches? |
|---|---|---|
| `git revert <hash>` | Creates a NEW commit that undoes a previous one | ✅ Yes |
| `git reset --soft HEAD~1` | Undoes last commit, keeps changes staged | ⚠️ Only local |
| `git reset --mixed HEAD~1` | Undoes last commit, keeps changes unstaged | ⚠️ Only local |
| `git reset --hard HEAD~1` | Permanently discards last commit AND all changes | ❌ Destructive |

```bash
# Safely undo a commit (creates a new "undo" commit)
git revert a1b2c3d

# Undo last commit but keep changes staged
git reset --soft HEAD~1

# Undo last commit, keep changes but unstage them
git reset --mixed HEAD~1

# DANGER: permanently delete the last commit and all its changes
git reset --hard HEAD~1
```

> **Rule of thumb:** If you've already pushed the commit, use `git revert`. If it's only local, `git reset` is fine.

---

## 12. Branching

A branch is an independent line of development. It lets you work on features without affecting the main codebase.

### Branch Commands

```bash
# List all local branches (* marks current branch)
git branch

# List all branches including remote-tracking branches
git branch -a

# Create a new branch
git branch feature-login

# Switch to a branch (classic syntax)
git checkout feature-login

# Switch to a branch (modern syntax — preferred)
git switch feature-login

# Create AND switch to a new branch in one step
git switch -c feature-login

# Rename the current branch
git branch -m new-name

# Delete a branch (only if it has been merged)
git branch -d feature-login

# Force delete a branch (even if unmerged — data loss risk)
git branch -D feature-login
```

---

### Branching Naming Conventions

A common pattern used in industry teams:

```
<initials>/feature_<feature_name>
<initials>/bugfix_<bug_name>
```

**Example:** John Doe (initials: JD) working on the login feature:
```
JD/feature_login
JD/bugfix_login
```

Other common naming patterns:

```
feature/user-auth
fix/cart-total
hotfix/payment-crash
release/v2.3
chore/update-dependencies
```

---

## 13. Merging

Merging combines the history of one branch into another.

```bash
# Step 1: Switch to the receiving branch (the one you want to merge INTO)
git switch main

# Step 2: Merge your feature branch in
git merge feature-login

# Step 3: Delete the branch after merging (optional but recommended)
git branch -d feature-login
```

### Types of Merges

**Fast-Forward Merge**
When `main` hasn't changed since you branched off. Git simply moves the pointer forward — no merge commit is created. Results in a clean, linear history.

**Three-Way Merge**
When both branches have new commits since they diverged. Git creates a special merge commit with two parents. This is the most common scenario in teams.

---

## 14. Merge Conflicts

Conflicts happen when two branches edit the **same line(s)** of the same file. Git can't decide which version to keep, so it marks the conflict and asks you to resolve it.

### What a Conflict Looks Like

```
<<<<<<< HEAD
  background: blue;
=======
  background: red;
>>>>>>> feature-redesign
```

- Everything above `=======` is **your** current branch (HEAD)
- Everything below `=======` is the **incoming** branch

### How to Resolve

1. Open the conflicted file in your editor
2. Decide which code to keep (or combine both)
3. Remove the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
4. Stage and commit the resolution:

```bash
git add .
git commit -m "Resolve merge conflict in style.css"
```

> **Tip:** Modern IDEs (VS Code, IntelliJ) highlight conflicts with color-coded buttons: **Accept Current**, **Accept Incoming**, or **Accept Both**.

---

## 15. Branching Strategies

### Git Flow

Best for: Enterprise, mobile apps, scheduled release cycles.

| Branch | Type | Purpose |
|---|---|---|
| `main` | permanent | Production-ready code only |
| `develop` | permanent | Integration branch — "next release" |
| `initials/feature_*` | temporary | One per feature; branch from develop |
| `release/*` | temporary | Prep a release: version bumps, final fixes |
| `hotfix/*` | temporary | Emergency fix; branches from main |

---

### GitHub Flow

Best for: Web apps, SaaS, startups, continuous deployment.

Simple model: only `main` + short-lived feature branches.

```bash
# 1. Create branch from main
git switch -c JD/feature_dark-mode

# 2. Commit your work
git commit -m "Add dark mode toggle"

# 3. Push and open a Pull Request
git push -u origin JD/feature_dark-mode

# 4. Review → Approve → Merge → Deploy

# 5. Delete the branch
git branch -d JD/feature_dark-mode
```

Why teams love it: `main` is always deployable, fast feedback via PRs, simple to learn.

---

### Trunk-Based Development

Best for: Large-scale teams (e.g. Google), strong CI/CD pipelines.

- Everyone commits directly to `main` (the "trunk")
- Branches (if any) live for less than a day
- Incomplete features hidden behind **feature flags** in code
- Automated tests run on every commit

---

## 16. Remote Repositories

A remote is a copy of your repo hosted on a server like GitHub.

```bash
# Connect a local repo to a GitHub remote
git remote add origin https://github.com/username/project.git

# Or with SSH
git remote add origin git@github.com:username/project.git

# List connected remotes (with URLs)
git remote -v

# Remove a remote
git remote remove origin

# Rename a remote
git remote rename origin upstream

# Change the URL of a remote
git remote set-url origin git@github.com:username/project.git
```

---

### Push & Pull

```bash
# First push: set the upstream tracking branch
git push -u origin main

# Subsequent pushes (once upstream is set)
git push

# Push a specific branch
git push origin feature-login

# Push all branches
git push --all

# Force push (NEVER on shared branches!)
git push --force

# Download + merge remote changes into current branch
git pull

# Download remote changes WITHOUT merging (safer)
git fetch

# Fetch then merge manually
git fetch origin
git merge origin/main
```

### The Full Push/Pull Workflow

```
YOUR MACHINE                        GITHUB (REMOTE)
─────────────                       ───────────────
Working Directory
     ↓  git add
Staging Area
     ↓  git commit
Local Repository  ──git push──→   Remote Repository
                  ←──git pull──
                  ←──git fetch── (without merge)
```

---

## 17. Pull Requests

A Pull Request (PR) is a proposal to merge your branch into another. It enables code review, discussion, and automated checks before changes go live.

### PR Workflow

```bash
# 1. Create and switch to a feature branch
git switch -c feature/search-bar

# 2. Write code, test locally, commit regularly
git add .
git commit -m "Add search component"
git commit -m "Add search API integration"
git commit -m "Add search results styling"

# 3. Push your branch to GitHub
git push -u origin feature/search-bar

# 4. Go to GitHub → "Compare & Pull Request"
# 5. Add a title and description, assign reviewers
# 6. Team reviews → Approves → Merges into main

# 7. Clean up locally
git switch main
git pull
git branch -d feature/search-bar
```

### GitHub Workflow Golden Rules

- `main` is **always** deployable
- Branch names are descriptive: `feature/user-auth`, `fix/cart-total`
- **Never commit directly to `main`**
- PRs get at least 1 review before merging
- Delete branches after merge

---

## 18. Forking & Open Source Contribution

A **fork** is your own copy of someone else's repository on GitHub. You can freely experiment without affecting the original project.

```bash
# 1. Fork the repo on GitHub (click the "Fork" button)

# 2. Clone YOUR fork locally
git clone https://github.com/YOU/project.git

# 3. Add the ORIGINAL repo as "upstream"
git remote add upstream https://github.com/ORIGINAL/project.git

# 4. Create a branch, make changes, push to YOUR fork
git switch -c fix/typo-in-readme
git commit -m "Fix typo in README"
git push origin fix/typo-in-readme

# 5. Open a PR from YOUR fork → ORIGINAL repo on GitHub

# 6. Keep your fork in sync with the original
git fetch upstream
git merge upstream/main
```

---

## 19. GitHub Beyond Code

**Issues** — Track bugs, feature requests, and tasks. Link to PRs with keywords like `Closes #42`.

**GitHub Actions (CI/CD)** — Automate tests, builds, and deployments. Runs on every push or PR.

**GitHub Pages** — Host static websites directly from a repo for free. Perfect for portfolios and docs.

**README.md** — The front page of your repository. Write in Markdown. Include setup instructions, usage examples, and badges.

---

## 20. .gitignore

A `.gitignore` file tells Git which files and folders to never track.

### Example `.gitignore`

```gitignore
# Dependencies
node_modules/
venv/
__pycache__/

# Build output
dist/
build/
*.pyc
*.class

# Environment & secrets — NEVER commit these!
.env
.env.local
*.key
*.pem
secrets.json

# OS-generated files
.DS_Store
Thumbs.db

# IDE/editor files
.vscode/
.idea/
*.swp
```

### Key Rules

```bash
# Files to NEVER commit:
# ✗ Passwords, API keys, tokens
# ✗ node_modules/ (can be 500MB+; regenerate with npm install)
# ✗ Compiled or build output files
# ✗ OS-generated files (.DS_Store, Thumbs.db)
```

> **Pro tip:** [github.com/github/gitignore](https://github.com/github/gitignore) has ready-made templates for every language and framework.

### Set up `.gitignore` before your first commit — removing already-tracked files later is painful.

```bash
# Stop tracking a file that's already committed
git rm --cached filename.txt
git commit -m "Remove tracked file that should be ignored"
```

---

## 21. Advanced Commands

### `git stash` — Save Work for Later

Need to switch branches but have uncommitted changes? Stash them temporarily.

```bash
# Stash all uncommitted changes
git stash

# Stash with a descriptive name
git stash push -m "WIP: login form"

# View all stashed items
git stash list

# Apply the most recent stash AND remove it from the list
git stash pop

# Apply the most recent stash but KEEP it in the list
git stash apply

# Apply a specific stash by index
git stash apply stash@{2}

# Delete a stash without applying it
git stash drop

# Clear all stashes
git stash clear
```

> **Scenario:** You're mid-feature but need an urgent bug fix on `main`. Stash → switch → fix → switch back → pop!

---

### `git rebase` — Rewrite History

```bash
# Rebase current branch on top of main
git rebase main

# Interactive rebase: edit, squash, reorder last 3 commits
git rebase -i HEAD~3
```

| | `git merge` | `git rebase` |
|---|---|---|
| History | Preserves complete history | Creates linear history |
| Commits | Adds a merge commit | Rewrites commit hashes |
| Safety | Safe on shared branches | **NEVER rebase shared branches!** |
| Use case | Team collaboration | Cleaning up local commits |

---

### `git cherry-pick` — Grab a Single Commit

Copy a specific commit from one branch and apply it to another without merging the entire branch.

```bash
# 1. Find the commit hash you want
git log --oneline JD/feature_payments
#   a1b2c3d Fix currency rounding bug
#   e4f5g6h Add payment gateway

# 2. Switch to the target branch
git switch main

# 3. Apply the specific commit
git cherry-pick a1b2c3d

# Cherry-pick multiple commits
git cherry-pick a1b2c3d e4f5g6h
```

**When to use it:**
- Hotfix needed on `main` but the fix lives on a feature branch
- Backporting a fix to an older release branch (e.g. `v2.x`)
- Picking select commits from a branch you don't want to merge fully

---

### `git tag` — Mark Releases

```bash
# Create a lightweight tag
git tag v1.0.0

# Create an annotated tag (recommended for releases)
git tag -a v1.0.0 -m "Release version 1.0.0"

# List all tags
git tag

# Push a tag to remote
git push origin v1.0.0

# Push all tags
git push origin --tags

# Delete a tag locally
git tag -d v1.0.0

# Delete a tag on remote
git push origin --delete v1.0.0
```

---

### Other Useful Commands

```bash
# Show who last modified each line of a file
git blame filename.txt

# Search for a string across all commits (find when a bug was introduced)
git bisect start
git bisect bad          # Current commit has the bug
git bisect good v1.0.0  # This older commit was fine
# Git will binary search through commits for you

# Clean up untracked files from the working directory
git clean -n   # Dry run: show what would be deleted
git clean -f   # Actually delete untracked files
git clean -fd  # Delete untracked files AND directories
```

---

## 22. Disconnecting GitHub from Your Local Device

There are several levels of "disconnecting" — choose based on what you need.

---

### Remove a Remote from a Project

Unlinks a specific local repository from a GitHub remote. The local repository and all commits remain intact.

```bash
# View current remotes
git remote -v

# Remove the remote named "origin"
git remote remove origin

# Verify it's gone
git remote -v
```

---

### Remove Saved GitHub Credentials (HTTPS)

If you authenticated via HTTPS and want Git to stop remembering your credentials:

**Windows — Git Credential Manager:**
```
Control Panel → User Accounts → Credential Manager → Windows Credentials
→ Find "git:https://github.com" → Remove
```

Or via terminal:
```bash
git credential reject
# Then type: protocol=https, host=github.com, and press Enter twice

# Or reset the credential helper
git config --global --unset credential.helper
```

**macOS — Keychain:**
```
Open "Keychain Access" app
→ Search for "github.com"
→ Delete the entry
```

Or via terminal:
```bash
git credential-osxkeychain erase
# Then type: host=github.com, protocol=https, and press Enter twice
```

**Linux:**
```bash
# If using the store helper
git config --global --unset credential.helper

# Delete stored credentials file
rm ~/.git-credentials

# If using libsecret
git credential reject <<EOF
protocol=https
host=github.com
EOF
```

---

### Remove an SSH Key

To stop SSH-based authentication with GitHub:

**Step 1 — Remove the key from GitHub:**
Go to **GitHub → Settings → SSH and GPG Keys** → click **Delete** next to the key.

**Step 2 — Delete the key files from your machine:**
```bash
# List all SSH keys
ls ~/.ssh/

# Delete the key pair (replace with your actual filename)
rm ~/.ssh/id_ed25519
rm ~/.ssh/id_ed25519.pub

# Or delete ALL SSH keys (careful if you use SSH for other services)
rm ~/.ssh/id_*
```

**Step 3 — Remove from SSH agent (current session):**
```bash
# List keys loaded in the agent
ssh-add -l

# Remove a specific key
ssh-add -d ~/.ssh/id_ed25519

# Remove all keys from the agent
ssh-add -D
```

**Step 4 — Verify disconnection:**
```bash
ssh -T git@github.com
# Expected: Permission denied (publickey)
```

---

### Sign Out of GitHub CLI (if installed)

If you use the `gh` CLI tool:

```bash
# Check login status
gh auth status

# Log out
gh auth logout

# Log out from a specific account
gh auth logout --hostname github.com
```

---

### Sign Out of GitHub Desktop (if installed)

**GitHub Desktop → File → Options → Accounts → Sign Out**

---

### Remove Git Globally (Nuclear Option)

If you want to completely remove Git identity from your machine:

```bash
# Remove global name and email
git config --global --unset user.name
git config --global --unset user.email

# Or delete the entire global config file
rm ~/.gitconfig       # macOS / Linux
# Windows: Delete C:\Users\YourName\.gitconfig
```

---

## 23. Best Practices

**Commit Often** — Small, focused commits are easier to review, revert, and understand.

**Write Good Messages** — Use imperative mood ("Add feature" not "Added feature"). Explain WHY, not just what.

**Pull Before Push** — Always `git pull` before pushing to avoid conflicts and rejected pushes.

**Never Force Push Main** — `git push --force` rewrites remote history. Only use on your own feature branches, and only when necessary.

**Use .gitignore Early** — Set it up before your first commit. Removing already-tracked files later is painful.

**Review Before Commit** — Use `git diff` and `git status` to verify what you're about to commit.

**Never Commit Secrets** — API keys, passwords, and `.env` files must be in `.gitignore`. If you accidentally commit one, rotate it immediately — deleted commits can still be recovered from history.

**Keep Branches Short-Lived** — Long-lived branches diverge significantly and create massive merge conflicts.

**Delete Merged Branches** — Clean up after yourself with `git branch -d branch-name`.

---

## 24. Cheat Sheet

### Setup

```bash
git config --global user.name "Name"    # Set username
git config --global user.email "email"  # Set email
git config --list                        # View config
```

### Starting a Repo

```bash
git init                   # Initialize a new repo
git clone <url>            # Clone a remote repo
```

### Core Workflow

```bash
git status                 # Check working state
git add <file>             # Stage a file
git add .                  # Stage all changes
git commit -m "message"    # Save a snapshot
git commit -am "message"   # Stage tracked + commit
```

### Inspecting

```bash
git log --oneline          # View compact history
git log --graph --oneline  # Visual branch graph
git diff                   # View unstaged changes
git diff --staged           # View staged changes
git show <hash>            # View a specific commit
git blame <file>           # See who wrote each line
```

### Branching

```bash
git branch                 # List branches
git branch <name>          # Create branch
git switch <name>          # Switch branch (modern)
git switch -c <name>       # Create + switch (modern)
git branch -d <name>       # Delete merged branch
git branch -D <name>       # Force delete branch
```

### Merging & Rebasing

```bash
git merge <branch>         # Merge branch into current
git rebase <branch>        # Rebase onto branch
git cherry-pick <hash>     # Apply a specific commit
```

### Remote

```bash
git remote -v              # List remotes
git remote add origin <url> # Add a remote
git push -u origin main    # First push
git push                   # Push commits
git pull                   # Fetch + merge
git fetch                  # Fetch only
```

### Undoing

```bash
git restore <file>         # Discard working changes
git restore --staged <file> # Unstage a file
git revert <hash>          # Safe undo (new commit)
git reset --soft HEAD~1    # Undo commit, keep staged
git reset --hard HEAD~1    # Undo commit + discard changes
```

### Stash

```bash
git stash                  # Stash changes
git stash pop              # Apply + remove stash
git stash list             # View stashes
git stash drop             # Delete a stash
```

### Tags

```bash
git tag v1.0.0             # Create a tag
git push origin v1.0.0     # Push a tag
git tag                    # List all tags
```

### Disconnecting from GitHub

```bash
git remote remove origin               # Remove remote link
git config --global --unset user.name  # Remove global name
git config --global --unset user.email # Remove global email
ssh-add -D                             # Remove all SSH keys from agent
gh auth logout                         # Log out of GitHub CLI
```

---

*Reference: Git official documentation at [git-scm.com/doc](https://git-scm.com/doc)*