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
		$scope.query = "";
		$scope.countryId = id;
	};

	$scope.mapInitialized = function() {
		$http.get('api/geojson/regions.json').success(function(data) {
			$scope.addGeoJsonLayer(data);
		});
	};

}]).
controller('HelpCtrl', ['$scope', '$http', function($scope, $http) {

}]).
controller('AboutCtrl', ['$scope', '$http', function($scope, $http) {

}]);
