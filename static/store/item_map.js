               
function initMap() {
    var map = L.map('map').setView([37.54022, -77.45811], 11);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);


    const data = document.getElementById('points-data').textContent;
    geojsonData = JSON.parse(data)

    console.log(geojsonData)

    const mediaUrl = 'https://sharemore-media.s3.amazonaws.com/media/'
    

    let pointLayer = L.geoJSON(geojsonData, {
        onEachFeature: function (feature, layer) {
            if (feature.properties && feature.properties.title) {
                layer.bindPopup(
                    `<h3> ${feature.properties.title} </h3>
                    <p> ${feature.properties.description} </p>
                    <img src="${mediaUrl}${feature.properties.thumbnail}"></img>`);
            }
        }
    }).addTo(map);

    map.fitBounds(pointLayer.getBounds());
}

document.body.addEventListener('htmx:afterSwap', function(event) {
    if (event.target.id === 'item-grid') {
        initMap();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('map')) {
        initMap();
    }
});



    // .setContent(function (layer){
    //     return `${layer.feature.properties.title}`
    // })
    // .bindPopup(function (layer) {
    //     return layer.feature.properties.title;
  
    // pointLayer.addData(geojsonData);
    // Add other map features here

        
        // function (layer) {
        // var popupContent = 
        // <div>
        //     <h3>${feature.properties.title}</h3>
        // </div>;
        
        // return popupContent;
        // });

    // .on('mouseover', function (e) {
    //     var marker = e.target;
    //     var popupContent = "Title: " + marker.feature.properties.title + marker.feature.properties.description;
    //     marker.bindPopup(popupContent).openPopup();
    // })
    // .on('mouseout', function (e) {
    //     var marker = e.target;
    //     marker.closePopup();
    // })

    // .bindPopup(function (layer) {
    //     return layer.feature.properties.title;
    // })
            