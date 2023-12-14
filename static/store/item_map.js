
const mediaUrl = 'https://sharemore-media.s3.amazonaws.com/media/'

function initMap() {
   
    window.selectedfid = 2;
    
    window.globalId = 2;
    console.log(globalId)
    
    var data = document.getElementById('points-data').textContent;

    console.log(data)
    
    var geojsonData = JSON.parse(data)
    
    console.log(geojsonData)


    var map = L.map('map').setView([37.54022, -77.45811], 11);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);


    let pointLayer = L.geoJSON(geojsonData, {
        onEachFeature: function (feature, layer) {
  
            if (feature.id) {
                layer.bindTooltip(feature.id.toString(), {permanent: true, direction: 'center'});
                }
            
        
            layer.on('click', function (e) {
                console.log(feature.properties.title);
                updateStore(feature);
                window.selectedfid = feature.id;
                console.log(selectedfid)

            });
        
        }
    }).addTo(map);

    map.fitBounds(pointLayer.getBounds());
}


document.addEventListener('alpine:init', () => {
    Alpine.store('darkMode', {
        on: false,

        toggle() {
            this.on = ! this.on
        }
    })

    Alpine.store('myStore', {
        title: 'Initial Title',
        description: 'Initial Description',
        imageUrl: 'Initial Image'
    });

    Alpine.store('mapStore', {
      data: geojsonData,

      highlighted: false,

      highlight(id) {
          if (feature.id === id) {
            this.highlighted = true;
          } else {
            this.highlighted = false;
          }
        }
    });


});

function updateStore(feature) {
    Alpine.store('myStore').id = feature.id;
    Alpine.store('myStore').title = feature.properties.title;
    Alpine.store('myStore').description = feature.properties.description;
    Alpine.store('myStore').imageUrl = mediaUrl + feature.properties.thumbnail;
    console.log(Alpine.store('myStore').imageUrl)
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