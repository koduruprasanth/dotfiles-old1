# Installation 
```
git clone https://github.com/koduruprasanth/dotfiles.git dotfiles
cd dotfiles
./install-profile osx.home
```

# Issues

## dotbot-brewfile
1. Expects python3 and uses string interpolation. OSX is setup with default python 2.7. Update the following code to run the setup on osx.
```
    #return f'{option}={value}'
    return "{0}={1}".format(option, value)
```

2. In order to see the progress of brew bundle update the following variables to `True`
```
    _default_stdout = False
    _default_stderr = False
```