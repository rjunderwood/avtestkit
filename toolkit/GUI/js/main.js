



function run_test(){
    

    document.getElementById("running_button").innerHTML = "Processing";
    document.getElementById("running_button").style.backgroundColor = "white";
    document.getElementById("window").style.cursor = "wait";
    

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

