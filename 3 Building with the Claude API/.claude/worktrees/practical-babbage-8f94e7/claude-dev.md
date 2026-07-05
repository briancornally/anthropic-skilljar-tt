# 2026-03-15-claude-code-safely

https://jerome-ng.com/articles/2026-03-15-claude-code-safely

# Create and start

brew install lima
limactl create --name=claude-dev claude-dev.yaml
limactl start claude-dev

# Enter the VM

limactl shell claude-dev
limactl show-ssh claude-dev

~/.ssh/config
Include ${LIMA_HOME:-$HOME/.lima}/claude-dev/ssh.config

/home/brian.guest
LIMA_VM=lima-claude-dev
code --folder-uri vscode-remote://ssh-remote+$LIMA_VM/home/$(whoami).guest

# Run Claude and log in (if using a Max subscription)

alias ccd="claude --dangerously-skip-permissions"
ccd

# then use /login inside the session

# When things go sideways

limactl delete claude-dev -f

# start fresh

---

git init

mkdir repo
git clone git@github.com:org/service-core.git repo/service-core
git clone git@github.com:org/service-integrations.git repo/service-integrations

echo "repo/" >> .gitignore
mkdir -p shared issues .claude/skills
