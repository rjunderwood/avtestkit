



class ResultData:
 #(t,loc.x,loc.y,loc.z,mag(vel),mag(acc),collision,lane_invasion,dist_to_actor))

    time=None
    location_x=None
    location_y=None
    location_z=None 
    mag_vel=None
    mag_acc=None
    collision=None
    lane_invasion=None
    dist_to_actor=None
    
    def __init__(self,time,location_x,location_y,location_z,mag_vel,mag_acc,collision,lane_invasion,dist_to_actor):
        self.time = time
        self.location_x = location_x
        self.location_y = location_y
        self.location_z = location_z,
        self.mag_vel = mag_vel
        self.mag_acc = mag_acc
        self.collision = collision
        self.lane_invasion = lane_invasion
        self.dist_to_actor = dist_to_actor
    
    
    def get_time(self):
        return self.time
    
    def get_location_x(self):
        return self.location_x
    
    def get_location_y(self):
        return self.location_y
    
    def get_location_z(self):
        return self.location_z
    
    def get_mag_vel(self):
        return self.mag_vel
    
    def get_mag_acc(self):
        return self.mag_acc
    
    def get_collision(self):
        return self.collision
    
    def get_lane_invasion(self):
        return self.lane_invasion
    
    def get_dist_to_actor(self):
        return self.dist_to_actor

        