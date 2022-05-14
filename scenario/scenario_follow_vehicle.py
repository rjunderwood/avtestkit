
import carla 


class ScenarioFollowVehicle:

    #Carla World
    world = None
    WEATHER = carla.WeatherParameters()
    #Ego Vehicle
    ego_vehicle = None 
    EGO_X = 301
    EGO_Y = 327.049988
    EGO_Z = 0.036313
    EGO_PITCH = 0
    EGO_YAW = 0
    EGO_ROLL = 0
    #Lead Vehicle
    lead_vehicle = None
    LEAD_VEHICLE_MODEL = 'vehicle.toyota.prius'
    LEAD_VEHICLE_ROLENAME = 'lead_vehicle'
    LEAD_X = 280
    LEAD_Y = 327.049988
    LEAD_Z = 0.2
    LEAD_PITCH = 0
    LEAD_YAW = 0
    LEAD_ROLL = 0
    #Spectator Camera
    spectator = None
    SPEC_CAM_X = 301
    SPEC_CAM_Y = 327.049988
    SPEC_CAM_Z = 120
    SPEC_CAM_PITCH = -90
    SPEC_CAM_YAW = 0
    SPEC_CAM_ROLL = 0 


    #Set the world and ego vehicle from ScenarioBase call
    def __init__(self,world,ego_vehicle):
        self.world = world 
        self.ego_vehicle = ego_vehicle

     

    





    def setup_world(self):
        self.world.set_weather(self.WEATHER) #Set the weather

    
    def setup_ego_vehicle(self):
        ego_transform = carla.Transform(
            carla.Location(self.EGO_X, self.EGO_Y, self.EGO_Z),
            carla.Rotation(self.EGO_PITCH,self.EGO_YAW,self.EGO_ROLL)
        ) 
        self.ego_vehicle.set_transform(ego_transform)  


    def setup_lead_vehicle(self):
        #Clear Previous Leading Vehicle
        actor_list = self.world.get_actors()
        for actor in actor_list:
            try:
                if(actor.attributes['role_name'] == 'lead_vehicle'):
                    actor.destroy()
            except: 
                pass
        
        lead_transform = carla.Transform(
            carla.Location(self.LEAD_X,self.LEAD_Y,self.LEAD_Z),
            carla.Rotation(self.LEAD_PITCH,self.LEAD_YAW,self.LEAD_ROLL)
        )
            
        #Library that is used for spawning actors
        blueprint_library = self.world.get_blueprint_library()
        #Select a blueprint for our lead vehicle
        lead_vehicle_bp = next(bp for bp in blueprint_library if bp.id == self.LEAD_VEHICLE_MODEL)
        lead_vehicle_bp.set_attribute('role_name', self.LEAD_VEHICLE_ROLENAME)
        #Spawn Vehicle
        self.lead_vehicle = self.world.spawn_actor(lead_vehicle_bp, lead_transform)
        self.lead_vehicle.apply_physics_control(carla.VehiclePhysicsControl(max_rpm = 5000.0, center_of_mass = carla.Vector3D(0.0, 0.0, 0.0), torque_curve=[[0,400],[5000,400]]))

        
    
    def setup_spectator(self):
      
        spectator = self.world.get_spectator()
        spectator_transform = carla.Transform(carla.Location(self.SPEC_CAM_X, self.SPEC_CAM_Y, self.SPEC_CAM_Z),carla.Rotation(self.SPEC_CAM_PITCH,self.SPEC_CAM_YAW,self.SPEC_CAM_ROLL))
        spectator.set_transform(spectator_transform)
        self.spectator = spectator
        

    #Run the Scenario
    def run(self):

        #1 Setup World
        self.setup_world()

        #2 Setup Ego Vehicle 
        self.setup_ego_vehicle()

        #3 Setup Lead Vehicle
        self.setup_lead_vehicle()

        #4 Setup Spectator
        self.setup_spectator()
 
    
        self.lead_vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0))
       
            
            
    





   




