export DESKTOP="prasantk-al2.aka.corp.amazon.com"

function desktop_tunnel() {
    port=$1
    echo "Opening tunnel to $CLOUD_DEV_DESKTOP:$port"
    ssh -N -L $port\:localhost:$port $CLOUD_DEV_DESKTOP
}

alias desktop="ssh $DESKTOP"
alias odin-tunnel="desktop_tunnel 2009"
alias desktop-ui="dcv-cdd.py connect $DESKTOP"

