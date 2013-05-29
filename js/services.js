'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('IntlPopApp.services', []).
  value('version', '3.1');