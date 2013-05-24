/*
* controllerss.js
*
* Written by Nate Beatty 
* for the IntlPop! project.
* May 2013
*/

'use strict';

/* Controllers */
function LaunchCtrl($scope, $http) {
	$http.get('api/countrylist.json').success(function(data) {
		$scope.countries = data;
	});

	// Default selection values
	$scope.selectedCountry = {"countryId" : 900};
	$scope.query = ""; 

	$scope.selectById = function(id) {
		$scope.query = "";
		$scope.selectedCountry.countryId = id;
	};
}

function HelpCtrl($scope, $http) {

}

function AboutCtrl($scope, $http) {

}