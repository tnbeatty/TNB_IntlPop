/*
* controllers.js
*
* Written by Nate Beatty 
* for the IntlPop! project.
* May 2013
*/

'use strict';

/* Controllers */
angular.module('IntlPopApp.controllers', []).
controller('LaunchCtrl', ['$scope', '$http', function($scope, $http) {

	$http.get('api/countrylist.json').success(function(data) {
		$scope.countries = data;
	});

	// Default selection values
	$scope.countryId = 900; // Select the world
	$scope.query = "";

	$scope.launchSim = function() {
		if ($scope.countryId && false) {
			// launch the simulator
			alert();
		} else {
			alert('Please select a region from the list or click on a location on the map before attempting to launch a simulation.');
		}
	}

	$scope.selectById = function(id) {
		console.log('Country selected: ' + id);
		$scope.query = "";
		$scope.countryId = parseInt(id);
	};

	$scope.changeLayer = function(mapName) {
		$scope.removeCurrentLayer();
		var url = 'api/geojson/' + mapName.toLowerCase() + '.json';
		$http.get(url).success(function(data) {
			$scope.addGeoJsonLayer(data);
		});
	};

	$scope.mapInitialized = function() {
		$scope.changeLayer('continents');
	};

	$scope.handleMapclick = function(e) {
		// Call a generic select function so the controller can handle
		// whatever future action is necessary to launch the simulator.
		$scope.selectById(parseInt(e.target.feature.properties.CountryID));
	};

}]).
controller('LicenseCtrl', ['$scope', '$http', function($scope, $http) {
	$http.get('MIT-License.txt').success(function(data) {
		$scope.licenseText = data;
	});
}]).
controller('HelpCtrl', ['$scope', '$http', function($scope, $http) {

}]).
controller('AboutCtrl', ['$scope', '$http', function($scope, $http) {

}]);

