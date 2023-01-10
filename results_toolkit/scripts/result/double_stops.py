        # source_stopping_distance_list = []
        # for test, frames in source_frames.items():
        #     recorded_test_frames=0
        #     if(not self.test_contains_crash(frames)):
        #         first_stop = False
        #         second_stop = False
        #         for frame in frames:
        #             velocity = float(frame.get_mag_vel())
        #             distance = float(frame.get_dist_to_actor())
        #             if(velocity == 0.0):
        #                 if(recorded_test_frames < 1 and not first_stop):
        #                     first_stop = True
        #                     recorded_test_frames += 1
        #                     source_stopping_distance_list.append(distance)
        #             if(first_stop and velocity > 0.0):
        #                 second_stop = True
        #                 recorded_test_frames = 0
                        
                    
        #             if(first_stop and second_stop and velocity == 0.0):
        #                 if(recorded_test_frames < 1):
        #                     recorded_test_frames += 1
        #                     source_stopping_distance_list.pop()
        #                     source_stopping_distance_list.append(distance)
                    


        # stopping_distances.append(source_stopping_distance_list)
        
        # print("source_stopping_distance_list",source_stopping_distance_list)

        # for follow_up in follow_up_frames:
        #     follow_up_stopping_distance_list = []
        #     for test, frames in follow_up.items():
        #         recorded_test_frames =0
        #         if(not self.test_contains_crash(frames)):
        #             first_stop = False
        #             second_stop = False
        #             for frame in frames:
        #                 velocity = float(frame.get_mag_vel())
        #                 distance = float(frame.get_dist_to_actor())
        #                 if(velocity == 0.0):
        #                     if(recorded_test_frames < 1):
        #                         first_stop = True
        #                         recorded_test_frames += 1   
        #                         follow_up_stopping_distance_list.append(distance)
        #                 if(first_stop and velocity > 0.0):
        #                     second_stop = True
        #                     recorded_test_frames = 0
                        

        #                 if(first_stop and second_stop and velocity == 0.0):
        #                     if(recorded_test_frames < 1):
        #                         recorded_test_frames += 1
        #                         follow_up_stopping_distance_list.pop()
        #                         follow_up_stopping_distance_list.append(distance)
                                