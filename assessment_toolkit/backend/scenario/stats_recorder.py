
import time
import os
import sys
import glob
import math
import json 
CWD = os.getcwd() 

CONFIG = json.load(open(CWD+'/config.json'));


try:
    sys.path.append(glob.glob(CONFIG['CARLA_SIMULATOR_PATH']+'PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

class StatsRecorder():

    world = None
    running_time = None
    def __init__(self, carla_world, running_time):
        self.running_time = running_time
        self.world = carla_world 
 
  
    def record_stats(self, role_name_to_track, accessory_rolename, filename):
        #records various stats about an actor and optionally logs to file in the following format
        # simulation time, location x, location y, location z, velocity mag, acceleration mag, collision sensor, distance between this actor and another actor(optional)

        actor_to_track = self.find_actor_by_rolename(self.world,role_name_to_track)

        if(actor_to_track == None):
            print("No actor with that rolename exists") 
        

        #setup collision sensor
        collision_flag = []
        collision_bp = self.world.get_blueprint_library().find('sensor.other.collision')
        collision_sensor = self.world.spawn_actor(collision_bp, carla.Transform(), attach_to=actor_to_track)
        collision_sensor.listen(lambda event: self.on_collision(collision_flag, event))

        lane_inv_flag = []
        lane_inv_bp = self.world.get_blueprint_library().find('sensor.other.lane_invasion')
        lane_inv_sensor = self.world.spawn_actor(lane_inv_bp, carla.Transform(), attach_to=actor_to_track)
        lane_inv_sensor.listen(lambda event: self.on_lane_invasion(lane_inv_flag, event)) 

        if(filename):
            print("OPENED FILE :::: " + filename)
            f = open(filename,"w+")
        
        start_t = self.current_time()
        end_time = start_t + self.running_time

        print("StatsRecorder record_stats()")
        loop_count = 0
        while(actor_to_track != None and self.current_time() < end_time):
            try:
                t=time.time() - start_t
                loc=actor_to_track.get_location()
                vel = actor_to_track.get_velocity()
                acc = actor_to_track.get_acceleration()

                #retrieve distance to other actor data 
                dist_to_actor = -10
                accessory_actor = self.find_actor_by_rolename(self.world, accessory_rolename)
                if(accessory_actor != None):#lane_invasion
                    dist_to_actor = self.calc_dist(actor_to_track, accessory_actor)
                
                #retrieve collision data
                collision = 0 
                if(len(collision_flag) > 0): #sensor has flagged a collision 
                    collision = self.mag(collision_flag[0])
                    collision_flag = [] # reset collision flag 
                    print("COLLISION !!!!!")
                    collision = 1
              
                
                #retrieve lane invasion data 
                lane_invasion = 0 # 0 means no lane invasions detected 
                if(len(lane_inv_flag)>0):
                    lane_invasion = 1 #lane invasion has occurred 
                    lane_inv_flag = [] #reset collision flag
                    print("LANE INVASION !!!!!")

                
                # #write data to file
                # if(filename):
                
            
                #print("Time: %0.2f | Loc: %0.2f,%0.2f,%0.2f | Vel: %0.2f | Acc: %0.2f | Collision: %s | Lane Invasion: %s | Dist to Other Actor: %0.2f" %(t,loc.x,loc.y,loc.z,self.mag(vel),self.mag(acc),collision,lane_invasion,dist_to_actor))
                # print("Acceleration:: " + str(self.mag(acc)))
                # print("Velocity:: " + str(self.mag(vel)))
                # print("Acceleration::++++ %0.2f" %(self.mag(acc)))
                # print("Velocity::++++ %0.2f" %(self.mag(vel)))
                # print("Acceleration::++++ %0.2f" %(acc))
                # print("Velocity::++++ %0.2f" %(vel))
                f.write("%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f\r" % (t,loc.x,loc.y,loc.z,self.mag(vel),self.mag(acc),collision,lane_invasion,dist_to_actor))
                #f.write("%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f\r" % (t,loc.x,loc.y,loc.z,str(self.mag(vel)),str(self.mag(acc)),collision,lane_invasion,dist_to_actor))



                #Check the actor we are tracking still exists
                actor_to_track = self.find_actor_by_rolename(self.world, role_name_to_track) #check actor still exists
           
            except KeyboardInterrupt:
                print("")

                if(filename):
                    f.close()
                
                return 
        
        if(filename):
            f.close()

        print("\nrecord_stats : COMPLETE") 
        
        return 
    


    #Gets the current time 
    def current_time(self): 
        return time.time()

    def find_actor_by_rolename(self, world, role_name_tofind):
        
        actors = world.get_actors()
        actors = actors.filter('vehicle.*') #filter out only vehicle actors

        if(actors):
            for actor in actors:
                role_name = "None"
                if 'role_name' in actor.attributes:
                    if(actor.attributes['role_name'] == role_name_tofind):
                        
                        return actor
            
            return None
        
        else:
            return None

    def on_collision(self,flag,event):
        print("on_collision()")
        flag.append(event.normal_impulse)

    def on_lane_invasion(self,flag,event):
        print("on_lane_invasion()")
        flag.append(True)

    # euclidean distance
    def calc_dist(self,actor_a, actor_b):
        loc_a = actor_a.get_location()
        loc_b = actor_b.get_location()
        
        dist_return_value = 0
        try:
            dist = math.sqrt((loc_a.x - loc_b.x)**2 + (loc_a.y - loc_b.y)**2 +(loc_a.y - loc_b.y)**2 )
            dist_return_value = dist 
        finally:
            return dist_return_value
            

    def mag(self,vec): #return magnitude of Carla 3D vector
        mag_return_value = 0
        
        #Catch math domain errors 
        try: 
            print("Vector :")
            print(vec.x)
            print(vec.y)
            print(vec.z)
            
            mag = math.sqrt(vec.x**2 + vec.y**2 + vec.z**2)
            mag_return_value = mag
        finally:
            return mag_return_value
        # return math.sqrt(vec.x**2 - vec.y**2 + vec.z**2)