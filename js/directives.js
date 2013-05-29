/*
* directives.js
*
* Written by Nate Beatty 
* for the IntlPop! project.
* May 2013
*/

'use strict';

/* Directives */

angular.module('IntlPopApp.directives', []).
directive('appVersion', ['version', function(version) {
	return function(scope, elm, attrs) {
		elm.text(version);
	};
}]).
directive('uiMap', ['$http', '$log', function($http, $log) {
	return {
		restrict: 'EAC',
		link: function(scope, element, attrs) {

			// Perform basic setup of the map
			var map = L.map('map', {
				center: [40.0, attrs.uiMapCenterLong], 
				zoom: 1.2,
				minZoom: 1.2,
				maxZoom: 3
			});

			// Define functions that allow the controller
			// to interact with the map.
			angular.extend(scope, {
				addGeoJsonLayer: function(geoJson) {
					scope.currentLayer = L.geoJson(geoJson, {
						style: map_style,
						onEachFeature: onEachFeature
					});
					scope.currentLayer.addTo(map);
				},
				removeCurrentLayer: function() {
					if (scope.currentLayer) {
						map.removeLayer(scope.currentLayer);
					}
				}
			});

			// Call a generic initialize method so the controller
			// can perform any setup needed such as adding data to 
			// display the map.
			scope.mapInitialized();

			/* Map Helper Methods */
			var map_style = function(feature) {
				return {
					color: "#000000",
					weight: 1,
					opacity: 1,
					fillColor: "#BBB",
					fillOpacity: 1
				}
			};

			function onEachFeature(feature, layer) {
				layer.on({
					mouseover: highlightFeature,
					mouseout: resetHighlight,
					click: handleMapclick
				});
			};

			function highlightFeature(e) {
				var layer = e.target;

				layer.setStyle({
					fillColor: '#C02702',
					fillOpacity: 0.8
				});

				if (!L.Browser.ie && !L.Browser.opera) {
					layer.bringToFront();
				}
			};

			function resetHighlight(e) {
				scope.currentLayer.resetStyle(e.target);
			};

			function handleMapclick(e) {
				// Call a generic select function so the controller can handle
				// whatever future action is necessary to launch the simulator.
				scope.selectById(parseInt(e.target.feature.properties.CountryID));
			};
			
		}
	};
}]);