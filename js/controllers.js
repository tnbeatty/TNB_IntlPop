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
	$scope.countryId = 900;
	$scope.query = ""; 

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

}]).
controller('HelpCtrl', ['$scope', '$http', function($scope, $http) {

}]).
controller('AboutCtrl', ['$scope', '$http', function($scope, $http) {

}]);
