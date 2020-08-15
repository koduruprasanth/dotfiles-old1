source ~/.zsh/zplug.zsh
source ~/.zsh/aliases.sh

export EDITOR=vi


# Add Toolbox to path if it exists
[[ -d "$HOME/.toolbox" ]] && export PATH=$HOME/.toolbox/bin:$PATH


#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
