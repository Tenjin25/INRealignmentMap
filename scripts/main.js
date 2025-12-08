mapboxgl.accessToken = 'pk.eyJ1Ijoic2hhbWFyZGF2aXMiLCJhIjoiY21kcW8yeDB2MDhvbTJzb29qeGp1aDZmZCJ9.Zw_i6U-dL7_bEKRHTUh7yg'; // Replace with your Mapbox token
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v11',
  center: [-83.5, 32.9], // Centered on Georgia
  zoom: 6.5
});

// Add navigation controls
map.addControl(new mapboxgl.NavigationControl());
