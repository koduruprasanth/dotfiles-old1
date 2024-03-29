export ZPLUG_HOME=~/.zsh/zplug
source $ZPLUG_HOME/init.zsh

zplug 'zplug/zplug', hook-build:'zplug --self-manage'

# Supports oh-my-zsh plugins and the like
zplug "plugins/alias-finder", from:oh-my-zsh, ignore:oh-my-zsh.sh
zplug "plugins/aws", from:oh-my-zsh, ignore:oh-my-zsh.sh
zplug "plugins/common-aliases", from:oh-my-zsh, ignore:oh-my-zsh.sh
zplug "plugins/git", from:oh-my-zsh, ignore:oh-my-zsh.sh
zplug "plugins/sdk", from:oh-my-zsh, ignore:oh-my-zsh.sh
zplug "plugins/themes", from:oh-my-zsh, ignore:oh-my-zsh.sh
zplug "plugins/tmux", from:oh-my-zsh, ignore:oh-my-zsh.sh
zplug "plugins/vscode", from:oh-my-zsh, ignore:oh-my-zsh.sh
zplug "plugins/yum", from:oh-my-zsh, ignore:oh-my-zsh.sh, if:"[[ $OSTYPE != *darwin* ]]"

# TODO: Disable on unix until fzf installation on unix is configured
zplug "plugins/zsh-interactive-cd", from:oh-my-zsh, ignore:oh-my-zsh.sh, if:"[[ $OSTYPE == *darwin* ]]"

#zplug "b4b4r07/ultimate", as:theme
zplug "agkozak/agkozak-zsh-prompt" # https://github.com/agkozak/agkozak-zsh-prompt
AGKOZAK_BLANK_LINES=1
AGKOZAK_CUSTOM_SYMBOLS=( '⇣⇡' '⇣' '⇡' '+' 'x' '!' '>' '?' )



# Install plugins if there are plugins that have not been installed
if ! zplug check --verbose; then
    printf "Install? [y/N]: "
    if read -q; then
        echo; zplug install
    fi
fi

zplug load --verbose