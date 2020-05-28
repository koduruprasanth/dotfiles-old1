source ~/.zsh/zplug.zsh

export EDITOR=code
alias reload='source ~/.zshrc'

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="/Users/prasanthk/.sdkman"
[[ -s "/Users/prasanthk/.sdkman/bin/sdkman-init.sh" ]] && source "/Users/prasanthk/.sdkman/bin/sdkman-init.sh"
