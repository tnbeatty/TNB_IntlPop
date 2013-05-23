/*
* app.js
*
* Written by Nate Beatty 
* for the IntlPop! project.
* May 2013
*/

'use strict';

// Declare app level module which depends on filters, and services
angular.module('IntlPopApp', []).
config(['$routeProvider', function($routeProvider) {
	$routeProvider.
	when('/launch', {templateUrl: 'partials/launch.html', controller: 'LaunchCtrl'}).
	when('/about', {templateUrl: 'partials/about.html', controller: 'AboutCtrl'}).
	when('/help', {templateUrl: 'partials/help.html', controller: 'HelpCtrl'}).
	otherwise({redirectTo: '/launch'});
}]);
