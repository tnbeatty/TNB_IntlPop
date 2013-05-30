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
controller('AppCtrl', ['$scope', '$location', function ($scope, $location) {
	$scope.isSimWindow = $location.path().split('/')[1] == 'sim';
}]).
controller('LaunchCtrl', ['$scope', '$http', function($scope, $http) {

	$http.get('api/countrylist.json').success(function(data) {
		$scope.countries = data;
	});

	// Default selection values
	$scope.countryId = 900; // Select the world
	$scope.countryName = 'World'; // Display the country name
	$scope.mapHoverName; // Should be blank to start
	$scope.query; // Should also be blank

	$scope.$watch('countryId', function() { 
		if (!$scope.countries) return;
		for (var i = $scope.countries.length - 1; i >= 0; i--) {
			if ($scope.countries[i].id == $scope.countryId) {
				$scope.countryName = $scope.countries[i].alias;
			}
		};
	});

	$scope.launchSim = function() {
		if ($scope.countryId) {
			console.log('Launching simulator with country id: ' + $scope.countryId);
			var simPath = '#/sim/' + $scope.countryId;
			window.open(simPath, '_blank', 'height=300, width=1000, location=no, menubar=no');
		} else {
			alert('Please select a region from the list or click on a location on the map before attempting to launch a simulation.');
		}
	}

	$scope.changeLayer = function(mapName) {
		$scope.removeCurrentLayer(); // In the directive
		var url = 'api/geojson/' + mapName.toLowerCase() + '.json';
		$http.get(url).success(function(data) {
			$scope.addGeoJsonLayer(data); // In the directive
		});
	};

	$scope.mapInitialized = function() {
		$scope.changeLayer('continents');
	};

}]).
controller('LicenseCtrl', ['$scope', '$http', function ($scope, $http) {
	$http.get('MIT-License.txt').success(function(data) {
		$scope.licenseText = data;
	});
}]).
controller('HelpCtrl', ['$scope', function ($scope) {

}]).
controller('AboutCtrl', ['$scope', function ($scope) {

}]).
controller('SimCtrl', ['$scope', '$http', '$routeParams', function ($scope, $http, $routeParams) {
	$scope.countryId = $routeParams.countryId;

	var dataPath = 'api/countrydata/2010_' + $scope.countryId + '.json';
	$http.get(dataPath).success(function(data) {
		$scope.country = data;
	}).
	error(function(data) {
		alert('There was a problem finding the country data that you requested. This app is still in development - sorry about that!');
	});
}]);

