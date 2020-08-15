source ~/.zsh/zplug.zsh
source ~/.zsh/aliases.sh

export EDITOR=vi
export DOTFILES_HOME="$HOME/dotfiles"

export PATH=$HOME/bin:$PATH

# Add Toolbox to path if it exists
[[ -d "$HOME/.toolbox" ]] && export PATH=$HOME/.toolbox/bin:$PATH

# Add work specific config
[[ -s "$HOME/.zshrc.work.osx" ]] && source "$HOME/.zshrc.work.osx"

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
