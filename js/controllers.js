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
	$scope.sayHello = "Hello World!";
}

function HelpCtrl($scope, $http) {
	$scope.isMobile = (detectMobile()) ? true : false;
}

function AboutCtrl($scope, $http) {
	$scope.isMobile = (detectMobile()) ? true : false;
}