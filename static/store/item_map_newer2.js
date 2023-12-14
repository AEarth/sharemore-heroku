const mediaUrl = "https://sharemore-media.s3.amazonaws.com/media/";

var selectedfid = "";

window.globalId = 2;
console.log(window.globalId);

var data = document.getElementById("points-data").textContent;

var geojsonData = JSON.parse(data);

console.log(geojsonData);

let currentlyHighlightedId = null;

function highlightMarker(layer) {
  layer.setStyle({
      radius: 7,
      fillColor: "#00f05f", // Red color for highlighting
      color: "#000",
      weight: 1,
      opacity: 1,
      fillOpacity: 0.8
  });
}

function resetMarkerStyle(marker) {
  marker.setStyle({
      radius: 7,
      fillColor: "#5645a1", // Original color
      color: "#000",
      weight: 1,
      opacity: 1,
      fillOpacity: 0.8
  });
}

let markersById = {};

function highlightMarkerById(featureId) {
let marker = markersById[featureId];
if (marker) {
    // Highlight style
    marker.setStyle({
        radius: 7,
        fillColor: "#00f05f", // Red color for highlighting
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    });
}
}

function resetHighlightById(featureId) {
let marker = markersById[featureId];
if (marker) {
    // reset style
    marker.setStyle({
        radius: 7,
        fillColor: "#5645a1", // Original color
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    });
}
}

function cycleHighlight(clicked_id){
if (currentlyHighlightedId) {
    resetHighlightById(currentlyHighlightedId);
}
console.log('clicked:', clicked_id);
console.log('previous:', currentlyHighlightedId);
highlightMarkerById(clicked_id);
currentlyHighlightedId = clicked_id;
}


function initMap() {
  var map = L.map("map").setView([37.54022, -77.45811], 11);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "© OpenStreetMap contributors",
  }).addTo(map);

  let pointLayer = L.geoJSON(geojsonData, {
  pointToLayer: function(feature, latlng) {
      return L.circleMarker(latlng, {
          radius: 7,
          fillColor: "#5645a1", // Original color
          color: "#000",
          weight: 1,
          opacity: 1,
          fillOpacity: 0.8
      });
  },


    onEachFeature: function (feature, layer) {
    
        markersById[feature.id] = layer;


      layer.on("click", function (e) {
        console.log(feature.properties.title);
        updateStore(feature);
        selectedfid = feature.id;
        console.log(selectedfid);

        if (currentlyHighlightedId) {
          resetHighlightById(currentlyHighlightedId);
          }

      highlightMarkerById(feature.id)
      currentlyHighlightedId = feature.id;


      });
    },
  }).addTo(map);

  map.fitBounds(pointLayer.getBounds());
}

document.addEventListener("alpine:init", () => {

  Alpine.store("mapStore", {
    data: geojsonData,

    highlighted: false,

    highlight(id) {
      if (feature.id === id) {
        this.highlighted = true;
      } else {
        this.highlighted = false;
      }
    },
  });
});

function updateStore(feature) {
  Alpine.store("myStore").id = feature.id;
  Alpine.store("myStore").title = feature.properties.title;
  Alpine.store("myStore").description = feature.properties.description;
  Alpine.store("myStore").imageUrl = mediaUrl + feature.properties.thumbnail;
  console.log(Alpine.store("myStore").imageUrl);
}

document.body.addEventListener("htmx:afterSwap", function (event) {
  if (event.target.id === "item-grid") {
    initMap();
  }
});

document.addEventListener("DOMContentLoaded", function () {
  if (document.getElementById("map")) {
    initMap();
  }
});

