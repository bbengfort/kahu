/*
 * geo.js
 * Implements wrapper functionality for creating Google maps with markers
 */
var geo = {
 Map: function Map(elem) {

   // Constructor function
   this.init = function(elem) {
     this.map = new google.maps.Map($(elem)[0]);
     this.bounds = new google.maps.LatLngBounds();
     this.markers = [];
     this.clusters = null;
   }

   // Add markers to the map
   this.add_markers = function(markers) {
     self = this;

     $.each(markers, function(_, location) {
       const content = `
         <h6>${location.title}</h6>
         <p>${location.replicas.length} Replicas:</p>
         <ul>
           ${location.replicas.map(replica => `<li>${replica}</li>`).join("\n")}
         </ul>
       `

       var position = new google.maps.LatLng(location.lat, location.lng)
       var info = new google.maps.InfoWindow({content: content})

       var marker = new google.maps.Marker({
         position: position, map: self.map, title: location.title
       })
       marker.addListener('click', function() { info.open(map, marker)});

       self.markers.push(marker)
       self.bounds.extend(position);
     })

     // Update cluseters and automatically fit the map
     self.clusters = new MarkerClusterer(self.map, self.markers);
     self.map.fitBounds(self.bounds);
     self.map.panToBounds(self.bounds);

   }

   // Call the constructor
   this.init(elem);
 }
}
