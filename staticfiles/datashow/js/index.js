
function handleBtns(btnID) {
    if (btnID == "explore") {
      console.log("explore button clicked");
      window.location.href = "explore/";
    } else if (btnID == "upload") {
      console.log("upload button clicked");
      window.location.href = "upload/";
    }
}
  

//  a function to show the range option below when a feature from the dropdown is selected
function showGeoFeatureRange() {
    f_options = ['Bed Mat Thickness', 'Bed Material', 'Bed Slope', 'Channel Width', 'Channel Depth', 'Cx Area', 'Mannings n']
    let selectedFeature = document.getElementById("geographic-features").options[document.getElementById("geographic-features").selectedIndex].value;
    console.log(selectedFeature);

    const features = document.getElementById("geographic-features");
    features.addEventListener("change", () => {
        let feature = features.options[features.selectedIndex];
        if (f_options.includes(feature.value)) {
            document.getElementById("more-feature-data").style.display = "block";
        }
    });
}
showGeoFeatureRange();

function getExploreFormData() {
    const form = document.getElementById("explore-form");
    const formData = {};
    
    form.addEventListener("submit", (event) => {
        console.log("it's form data");
        event.preventDefault();

        for (const element of form.elements) {
            console.log(element.name, element.value);
            formData[element.name] = element.value;
        }
    });
    // localStorage.setItem("formData", JSON.stringify(formData));
    return formData;
}
// getExploreFormData();



// function manage google map api, display map and marker and info window on map
function setMarkers(map) {
    const image = {
        url: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
        size: new google.maps.Size(20, 32),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32)
    };
    const shape = {
        coords: [1, 1, 1, 20, 18, 20, 18, 1],
        type: 'poly'
    };
    const infowindow = new google.maps.InfoWindow();
    for (let i = 0; i < locations.length; i++) {
        const marker = new google.maps.Marker({
            position: locations[i].latlng,
            map: map,
            icon: image,
            shape: shape,
            title: locations[i].name,
            zIndex: locations[i].zIndex
        });
        google.maps.event.addListener(marker, 'click', (function (marker, i) {
            return function () {
                infowindow.setContent(locations[i].name);
                infowindow.open(map, marker);
            }
        })(marker, i));
    }
}

function testmap() {   
    console.log("testmap"); 
    div = document.getElementsByClassName("mapmap")[0];
    // change the divs content to "hello world"
    div.innerHTML = "hello world";
}

// const searchBtn = document.getElementById("search-btn");
// searchBtn.addEventListener("click", () => {
//     // Get search query and other relevant data from the form inputs
//     const searchQuery = document.getElementById("search-input").value;

//     // Make an AJAX request to a Django endpoint
//     fetch("/search-endpoint", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ query: searchQuery }),
//     })
//         .then(response => response.json())
//         .then(data => {
//             // Process the received data and update the HTML accordingly
//             // For example, populate a result container with the fetched data
//             const resultContainer = document.getElementById("result-container");
//             resultContainer.innerHTML = ""; // Clear previous results
//             data.forEach(item => {
//                 const listItem = document.createElement("li");
//                 listItem.textContent = item.name;
//                 resultContainer.appendChild(listItem);
//             });
//         })
//         .catch(error => {
//             console.error("An error occurred:", error);
//         });
// });


// DOWNLOAD
function downloadData() {
    const checkboxes = document.querySelectorAll('input[name="data-choice"]:checked');
    const selectedData = Array.from(checkboxes).map(checkbox => checkbox.value);

    selectedData.forEach(dataType => {
        // Handle each dataType appropriately
        if(dataType === "timeseries") {
            // Download timeseries data
        }
        // ... Handle other data types
    });
}



// LOADING
function showLoading() {
    document.getElementById('loading-indicator').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loading-indicator').style.display = 'none';
}
