
Autonomous Vehicle Assessment Toolkit
=====================================

## Recommended system

* Intel i7 gen 9th - 11th / Intel i9 gen 9th - 11th / AMD ryzen 7 / AMD ryzen 9
* +16 GB RAM memory
* NVIDIA RTX 2070 / NVIDIA RTX 2080 / NVIDIA RTX 3070, NVIDIA RTX 3080
* Ubuntu 18.04

## Requirements
* Python 3.7
* CUDA-10.0 (https://docs.nvidia.com/cuda/archive/10.0/cuda-installation-guide-linux/index.html)
* Docker (19.03+) (https://github.com/autowarefoundation/autoware_ai_documentation/wiki/docker-installation)
* Nvidia docker (https://github.com/NVIDIA/nvidia-docker)
* carla-simulator 0.9.11 (https://github.com/carla-simulator/carla)
* carla-autoware 0.9.11 (https://github.com/Kailthen/carla-autoware)
* PySimpleGUI (https://pypi.org/project/PySimpleGUI)

# Environment Setup
## 1. Install Requirements

### 1.1 Python 3
```sh
sudo apt install -y python3-pip python3-setuptools python3-vcstools python3-tk
pip3 install -U setuptools
```

### 1.2 Install GIT LFS

```sh
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
git lfs install
```

### 1.3 Install CUDA-10.0 & CUDA-TOOLKIT-10.0
For installation instructions for CUDA 10.0, see https://docs.nvidia.com/cuda/archive/10.0/cuda-installation-guide-linux/index.html
```sh
sudo apt clean && sudo apt update && sudo apt purge cuda && sudo apt purge nvidia-* && sudo apt autoremove
sudo apt-get install freeglut3 freeglut3-dev libxi-dev libxmu-dev
wget https://developer.nvidia.com/compute/cuda/10.0/Prod/local_installers/cuda-repo-ubuntu1804-10-0-local-10.0.130-410.48_1.0-1_amd64.deb -P ~/Downloads/
wget -p http://developer.download.nvidia.com/compute/cuda/10.0/Prod/patches/1/cuda-repo-ubuntu1804-10-0-local-nvjpeg-update-1_1.0-1_amd64.deb -P ~/Downloads/
sudo dpkg -i ~/Downloads/cuda-repo-ubuntu1804-10-0-local-10.0.130-410.48_1.0-1_amd64.deb
sudo dpkg -i ~/Downloads/cuda-repo-ubuntu1804-10-0-local-nvjpeg-update-1_1.0-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo apt-get install -y cuda-10-0 cuda-toolkit-10-0
echo "export PATH=/usr/local/cuda-10.0/bin:$PATH" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}" >> ~/.bashrc
```

### 1.4 Install Carla-Simulator

Other requirements. Two Python modules: Pygame to create graphics directly with Python, and Numpy for great calculus.
To install both modules using pip3, run the following commands.
```sh
pip3 install --user pygame numpy
```

Set up the Debian repository in the system.
```sh
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1AF1527DE64CB8D9
sudo add-apt-repository "deb [arch=amd64] http://dist.carla.org/carla $(lsb_release -sc) main"
```
Install CARLA and check for the installation in the /opt/ folder.
```sh
sudo apt-get update # Update the Debian package index
sudo apt-get install carla-simulator=0.9.11 # Install the 0.9.11 CARLA version
cd /opt/carla-simulator # Open the folder where CARLA is installed
```

### 1.5 Install Carla-Autoware (and fix a few things)

```sh
cd & git clone --recurse-submodules https://github.com/av-toolkit/carla-autoware.git
cd & git clone https://github.com/ThiagoFelipeSandeiro/carla-autoware-mods.git
cd ~/carla-autoware
cp ~/carla-autoware-mods/patch_files/update_* ~/carla-autoware/
sed -i '/autoware-contents/d' .dockerignore # make sure autoware contents are copied over
mv update_my_mission_planning.patch update_my_mission_planning.launch.patch # rename file correctly
patch ~/carla-autoware/Dockerfile ~/carla-autoware/update_Dockerfile.patch
sed -i '85s/$/\//' Dockerfile # update trailing slash for COPY

./build.sh # build carla-autoware

patch ~/carla-autoware/run.sh ~/carla-autoware/update_run.sh.patch
```

### 1.6 Setup BASH Environment
```sh
echo "export CARLA_AUTOWARE_ROOT=/home/$(whoami)/carla-autoware" >> ~/.bashrc
echo "export CARLA_AUTOWARE_CONTENTS=/home/$(whoami)/carla-autoware/autoware-contents" >> ~/.bashrc
echo "export CARLA_SIM=/opt/carla-simulator" >> ~/.bashrc
```


# Tool-kit Setup
## 1. Install PySimpleGUI
```sh
pip3 install PySimpleGUI
```

## 2. Edit assessment_toolkit/config.json

```json
{
    "CARLA_SIMULATOR_PATH":"/opt/carla-simulator",
    "CARLA_AUTOWARE_PATH":"/home/$USER/carla-autoware/"
}
```

## Usage
1. Start Toolkit
```sh
cd assessment_toolkit/
python3 assessment_toolkit.py
```


## Creating New Scenarios

### 1. Create Files
- assessment_toolkit/backend/scenario/SCENARIO_NAME.py
- assessment_toolkit/backend/scenario/metamorphic_tests/SCENARIO_NAME.json
- assessment_toolkit/ros_patch/scenarios/SCENARIO_NAME.json

### 2. Edit Files
assessment_toolkit/assessment_toolkit.py
- setup_scenarios()

assessment_toolkit/frontend/views.py
- view_container()
- view_setup_scenarios()
- view_setup_scenarios_none()
- view_scenario_starter_SCENARIO_NAME()

assessment_toolkit/frontend/front_end_main.py
- start()
- change_view()

assessment_toolkit/backend/scenario/scenario.py
- __init__

results_toolkit/frontend/front_end_main.py
- change_view()

results_toolkit/frontend/views.py
- view_container()
