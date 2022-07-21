import os

class PatchRos:
    
    __rospatch__ = None
    directory = os.getcwd() 
    directory = directory.replace("/backend/interface","")

    def __init__(self):
        self.setup_patch_files()
        script_path = self.directory +"/ros_patch/setup_carla_autoware_docker_container.sh"
        # self.__rospatch__ = os.system("gnome-terminal -e 'bash -c \"" + script_path +" -s; exec bash\"'")

        self.__rospatch__ = os.system("gnome-terminal -e 'bash -c \"" + script_path +" -s;\"'")
    
    def apply_ros_patch(self):
        self.setup_patch_files()
        return self.__rospatch__



    #Setting up the patch files is important for the bash scripts copying files from the correct system directory.
    def setup_patch_files(self):


        ros_patch = open(self.directory+'/ros_patch/setup_carla_autoware_docker_container.sh')
        ros_patch_lines = ros_patch.readlines()
        ros_patch.close()
        line_number=1

        ros_patch_new = open(self.directory+'/ros_patch/setup_carla_autoware_docker_container.sh', 'w')
        edit_ros_patch_file=""
        
        for line in ros_patch_lines:
            if line_number == 18:
                line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp "+ self.directory +"/ros_patch/patch_files/update_vehicle_model.launch.patch %%:/home/autoware/Documents\n"
            if line_number == 26:
                line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp "+ self.directory +"/ros_patch/patch_files/update_my_mission_planning.patch %%:/home/autoware/Documents\n"
            if line_number == 34:
                line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp "+ self.directory +"/ros_patch/create_ego_car_csv.sh %%:/home/autoware/Documents\n"
            if line_number == 46:
                line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp "+ self.directory +"/ros_patch/run-simulation.bash %%:/home/autoware/Documents\n"
            ros_patch_new.write(line)
            line_number+=1
            