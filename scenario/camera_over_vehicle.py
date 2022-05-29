


import carla 
def camera_over_vehicle():

    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    ego_vehicle = None

    #Set the ego vehicle actor
    actor_list = world.get_actors()
    for actor in actor_list:
        try:
            if(actor.attributes['role_name'] == 'ego_vehicle'):
               ego_vehicle = actor
        except: 
            pass

    #Spectator Camera
    spectator = None
    SPEC_CAM_X = 301
    SPEC_CAM_Y = 327.049988
    SPEC_CAM_Z = 120
    SPEC_CAM_PITCH = -90
    SPEC_CAM_YAW = 0
    SPEC_CAM_ROLL = 0 

    spectator = world.get_spectator()
  
    spectator_transform =carla.Transform(carla.Location(ego_vehicle.get_transform().location.x, ego_vehicle.get_transform().location.y, SPEC_CAM_Z),carla.Rotation(SPEC_CAM_PITCH,SPEC_CAM_YAW,SPEC_CAM_ROLL))
    spectator.set_transform(spectator_transform)



camera_over_vehicle()