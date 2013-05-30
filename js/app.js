/*
* app.js
*
* Written by Nate Beatty 
* for the IntlPop! project.
* May 2013
*/

'use strict';

// Declare app level module which depends on controllers
angular.module('IntlPopApp', ['IntlPopApp.controllers', 'IntlPopApp.directives', 'IntlPopApp.filters', 'IntlPopApp.services']).
config(['$routeProvider', function($routeProvider) {
	$routeProvider.
	when('/launch', {templateUrl: 'partials/launch.html', controller: 'LaunchCtrl'}).
	when('/about', {templateUrl: 'partials/about.html', controller: 'AboutCtrl'}).
	when('/help', {templateUrl: 'partials/help.html', controller: 'HelpCtrl'}).
	when('/license', {templateUrl: 'partials/license.html', controller: 'LicenseCtrl'}).
	when('/sim/:countryId', {templateUrl: 'partials/simulate.html', controller: 'SimCtrl'}).
	otherwise({redirectTo: '/launch'});
}]);
