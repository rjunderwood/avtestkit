
//import * as fs from './node_modules/fs-web/dist/fs.js';

const metrics_environment_perception = {
"metric_velocity_variance_value":0.5,
"metric_position_variance_value":0.5,
"metric_jaccard_variance_value":0.5,
"metric_iou_variance_value":0.5,
"metric_mota_variance_value":0.5,
"metric_motp_variance_value":0.5,

}

const metrics_motion_planning = {
    "metric_opposite_longitudinal_value":0.5,
    "metric_same_longitudinal_value":0.5,
    "metric_lateral_distance_value":0.5,
}
    
const testing_scenarios = {
   "follow_leading_vehicle": true,
   "close_proximity_pedestrian": true,
   "pedestrian_intersection": true,
   
}

// const scenario_settings = {
//     "follow_leading_vehicle": true,
    
    
//  }


// function changeScenarioSettings(){
    
// }
 
function run_test(){
    document.getElementById("running_button").innerHTML = "Processing";
    document.getElementById("running_button").style.backgroundColor = "white";
    document.getElementById("window").style.cursor = "wait";    


    saveToolkitSettingsToJson();

    //Wait 3 seconds 
    setTimeout(function () {
        navigate_to_results_page();
    }, 3000);

}

function navigate_to_results_page(){
    window.location = 'results.html';
}


function navigate_to_home_page(){
    window.location = 'home.html';
}



function changeMetricValue(event){
    console.log(event.target.id);
    metrics_environment_perception[event.target.id+"_value"] = event.target.value / 100; 
    setAllMetricValues();
}


function changeMotionMetricValue(event){
    console.log(event.target.id);
    metrics_motion_planning[event.target.id+"_value"] = event.target.value;
    console.log(event.target.value);
}



function setAllMetricValues(){

    for (const [key, value] of Object.entries(metrics_environment_perception)) {
        console.log("key ",key);
        document.getElementById(key).innerHTML = value;
        console.log(key, value);
      }
  
}


function changeTestingScenarios(event){
    testing_scenarios[event.target.id] = !testing_scenarios[event.target.id];
    console.log(testing_scenarios)
}




function saveToolkitSettingsToJson(){

    const settings = {
        "metrics_environment_perception":metrics_environment_perception,
        "metrics_motion_planning":metrics_motion_planning,
        "testing_scenarios":testing_scenarios
    }
    var json = JSON.stringify(settings);
    
    // writeFile('../json/toolkit_settings.json', json, 'utf8', callback);

    fs.writeFile('../json/toolkit_settings.json', json).then(function() {
        // All done! File has been saved.
      });

}











