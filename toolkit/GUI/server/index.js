const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const cors = require('cors')
const port = 3000
const fs = require('fs');



// We are using our packages here
app.use(bodyParser.json());       // to support JSON-encoded bodies

app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
    extended: true
}));
app.use(cors())

//You can use this to check if your server is working
app.get('/', (req, res) => {
    res.send("Welcome to your server")
})

app.post('/toolkit-result', (req, res) => {
    console.log("/toolkit-result");
    res.send({text:""});
});

//Route that handles login logic
app.post('/toolkit-run', (req, res) => {
    console.log('/toolkit-run');



    //import * as fs from './node_modules/fs-web/dist/fs.js';

    const metrics_environment_perception = {
        "metric_velocity_variance_value": req.body.metric_velocity_variance,
        "metric_position_variance_value": req.body.metric_position_variance,
        "metric_jaccard_variance_value": req.body.metric_jaccard_variance,
        "metric_iou_variance_value": req.body.metric_iou_variance,
        "metric_mota_variance_value": req.body.metric_mota_variance,
        "metric_motp_variance_value": req.body.metric_motp_variance,
    }

    const metrics_motion_planning = {
        "metric_opposite_longitudinal_value": req.body.metric_opposite_longitudinal,
        "metric_same_longitudinal_value": req.body.metric_same_longitudinal,
        "metric_lateral_distance_value":req.body.metric_lateral_distance,
    }

    const testing_scenarios = {
        "follow_leading_vehicle": req.body.follow_leading_vehicle,
        "close_proximity_pedestrian": req.body.close_proximity_pedestrian,
        "pedestrian_intersection": req.body.pedestrian_intersection,
    }

    const settings = {
        "metrics_environment_perception":metrics_environment_perception,
        "metrics_motion_planning":metrics_motion_planning,
        "testing_scenarios":testing_scenarios
    }
    var json = JSON.stringify(settings);
    console.log(json);

    fs.writeFile("../json-outputs/output.json", json, 'utf8', function (err) {
        if (err) {
            console.log("An error occured while writing JSON Object to File.");
            return console.log(err);
        }

    });

});

//Route that handles signup logic
app.post('/signup', (req, res) => {
    // console.log(req.body.fullname) 
    // console.log(req.body.username)
    // console.log(req.body.password) 



})

//Start your server on a specified port
app.listen(port, () => {
    console.log(`Server is runing on port ${port}`)
});


