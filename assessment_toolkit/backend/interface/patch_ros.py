import os
import json



class PatchRos:
    
    __rospatch__ = None
    directory = os.getcwd() 
    directory = directory.replace("/backend/interface","")
    ROSLAUNCH_CONFIG = json.load(open(directory + '/ros_patch/scenarios/roslaunch_config.json'))


    def __init__(self, scenario):
        if(len(scenario) > 1):
            self.setup_patch_files(scenario)
            script_path = self.directory +"/ros_patch/setup_carla_autoware_docker_container.sh"
        # self.__rospatch__ = os.system("gnome-terminal -e 'bash -c \"" + script_path +" -s; exec bash\"'")

        self.__rospatch__ = os.system("gnome-terminal -e 'bash -c \"" + script_path +" -s;\"'")
    
    def apply_ros_patch(self):
        self.setup_patch_files()
        return self.__rospatch__



    #Setting up the patch files is important for the bash scripts copying files from the correct system directory.
    def setup_patch_files(self, scenario):

        print("Setup patch files SCENARIO ::: "+scenario)
        ros_patch = open(self.directory+'/ros_patch/setup_carla_autoware_docker_container.sh')
        ros_patch_lines = ros_patch.readlines()
        ros_patch.close()
        line_number=1

        ros_patch_new = open(self.directory+'/ros_patch/setup_carla_autoware_docker_container.sh', 'w')
    
        
        for line in ros_patch_lines:
            if line_number == 18:
                line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp "+ self.directory +"/ros_patch/patch_files/update_vehicle_model.launch.patch %%:/home/autoware/Documents\n"
            if line_number == 26:
                line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp "+ self.directory +"/ros_patch/patch_files/update_my_mission_planning.patch %%:/home/autoware/Documents\n"
            if line_number == 34:
                # OLD General 2dnav 2dpose patch file that is setup for the first scenario 
                #line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp "+ self.directory +"/ros_patch/create_ego_car_csv.sh %%:/home/autoware/Documents\n"
                # NEW 2dnav, 2dpose that is setup for the given scenario.
                line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp "+ self.directory +"/ros_patch/scenarios/" + scenario + ".sh %%:/home/autoware/Documents\n"
            if line_number == 37:
                line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker exec --user autoware -i %% bash /home/autoware/Documents/"+scenario+".sh\n"
            if line_number == 40:
                line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker exec %% chmod +x /home/autoware/Documents/"+ scenario+".sh\n"
            if line_number == 43: 
                line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker exec --user autoware -i %% /home/autoware/Documents/" + scenario + ".sh\n"
            if line_number == 46:
                line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp "+ self.directory +"/ros_patch/run-simulation.bash %%:/home/autoware/Documents\n"
            ros_patch_new.write(line)
            line_number+=1
        
        ros_patch_new.close()
        
        
        #Adjust the run-simulation.bash 
        run_simulation_bash = open(self.directory+'/ros_patch/run-simulation.bash')
        run_simulation_bash_lines = run_simulation_bash.readlines()
        run_simulation_bash.close()

        run_simulation_new = open(self.directory+'/ros_patch/run-simulation.bash', 'w')
        line_number = 1
        for line in run_simulation_bash_lines:
            print("READLINE LINE " + line)
            if line_number == 1:
                run_simulation_new.write(line)
            
            elif line_number == 2:
                line = self.ROSLAUNCH_CONFIG[scenario]
                run_simulation_new.write(line)
                run_simulation_new.write('\n')
            else:
                run_simulation_new.write(line)
       
            line_number+=1
        run_simulation_new.close()
