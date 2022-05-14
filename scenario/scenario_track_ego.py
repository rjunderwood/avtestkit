from re import A
import time
import carla 
import time





client = carla.Client('localhost', 2000)
client.set_timeout(2.0)



world = client.get_world()
spectator = world.get_spectator()
world_snapshot = world.wait_for_tick() 


actor_list = world.get_actors()

ego_actor = None

for actor in actor_list:
    try:
       
        if(actor.attributes['role_name'] == 'ego_vehicle'):
       
            ego_actor = actor

    except: 
        pass
        
    #print(actor.attributes.role_name == 'ego_vehicle')
    # if( == 'vehicle.toyota.prius'):
    #     ego_actor = actor








while True:
    print(ego_actor.get_location())



# spectator.set_transform(ego_vehicle.get_transform())











