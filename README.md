
Autonomous Vehicle Assessment Toolkit
=====================================

## Recommended system

* Intel i7 gen 9th - 11th / Intel i9 gen 9th - 11th / AMD ryzen 7 / AMD ryzen 9
* +16 GB RAM memory 
* NVIDIA RTX 2070 / NVIDIA RTX 2080 / NVIDIA RTX 3070, NVIDIA RTX 3080
* Ubuntu 18.04

## Requirements
* Anaconda 4.13.0
* Python 3.7
* CUDA enabled GPU
* CUDA-10.0 & CUDA-TOOLKIT-10.0
* carla-simulator 0.9.11 (https://github.com/carla-simulator/carla)
* carla-autoware 0.9.11 (https://github.com/Kailthen/carla-autoware)
* ros-bridge 0.9.11 (https://github.com/carla-simulator/ros-bridge)

## Setup
1. Install Requirements
2. Edit assessment_toolkit/config.json 

```json
{
    "CARLA_SIMULATOR_PATH":"/home/riley/Desktop/CARLA_0.9.11/", 
    "CARLA_AUTOWARE_PATH":"/home/riley/Desktop/carla-autoware/"
}
```


## Usage
1. Start Toolkit 
```sh
python assessment_toolkit/assessment_toolkit.py
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


results_toolkit/frontend/front_end_main.py
- change_view()

results_toolkit/frontend/views.py 
- view_container()
