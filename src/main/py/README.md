### Installation

#### On Ubuntu

(Tested on Codeanywhere container)

<mark>TODO: Switch to Python **3**</mark>

```bash
sudo apt-get update
sudo apt-get install python-numpy cython
# cython should be optional
sudo apt-get install pandas
sudo pip2 install --upgrade numpy
sudo pip2 install --upgrade pandas
sudo pip2 install --upgrade matplotlib
```

#### On MacOS

##### Prerequisites

Automatic configuration is based on python 3.7.0, pyenv, and virtualenv:

```bash
brew install python # i.e. python3
pip3 install --upgrade pip
pip3 install pyenv
pyenv install 3.7.0
pip3 install virtualenv
```

##### Project dependencies

Assuming `{WORKDIR_ROOT}` is the root of the git workdir:

```bash
cd {WORKDIR_ROOT}
source .venv/bin/activate
```
