IntlPop! 3.0 - Test Version
===

This is a test version of IntlPop! 3.0 modified from [the original](https://github.com/cashaffer/IntlPop) by IntlPop! project collaborator, [Nate Beatty](http://natebeatty.com).

Overview
---

Project home for HTML5/JavaScript International Population simulation
for introductory geography courses.

Code Structure
---

Although the app is relatively simple, we use some of the basic features of Angular JS and a straightforward directory system to give the code some structure. Ultimately, this should be tremendously helpful as we add features and as other programmers continue to contribute to the development of IntlPop!.

### /api

This folder contains any "internal api" files - data files, country lists, GeoJSON, etc. Basically, any data that needs to be read into the simulator should be dropped in this directory.

### /img

Any images used on the site should be stored in this directory. They should be appropriately named for their function and the number of images should be very small. With lots of data and simulating going on, we don't need to slow things down with big images.

### /js

Javascripts go here. This directory contains the "controller" part of the MVC structure, along with the files that do the routing and angular-specific directives, etc. Look for third party JS libraries in /lib.

### /lib

This directory houses third party libraries - all javascript at the moment. AngularJS, Foundation, and Raphael have their own seperate sub-dirs to keep things organized while modernizr, jquery, and zepto are all in the "vendor" subdirectory.

### /partials

Views to be rendered within the index.html layout go in this directory. They're HTML files and should contain the code that needs to go in the place of the `<div ng-view></div>` code in /index.html.

### /sass

Contains all of the editable SASS `.scss` stylesheets. The actual CSS is generated from these files and placed in another directory. 

### /stylesheets

Don't edit anything in there... it's generated directly from the files in the SASS directory and any changes you make will be overwritten.

Developer Toolkit
---

This project uses a couple of open-source tools. They include the following:

### Foundation

The [Zurb Foundation](http://foundation.zurb.com) CSS framework was very useful for quickly producing a clean layout that scales easily.

#### Editing the CSS

It is inadvisable to edit the CSS directly. It would be better edit the SCSS provided as described in the [Zurb Documentation](http://foundation.zurb.com/docs/sass.html). To do so, you will need to install the compass gem. To get going, watch the SCSS files for changes by running `$ compass watch` in the project directoy. The `config.rb` file is set up so that you don't need to specify files to watch, etc.

### Angular JS

This version of IntlPop! is a SVA built on Google's [AngularJS](http://angularjs.org) framework. It is fast, organized, and has a structure that will be familiar to most modern web application developers. This means that it will be easily edited and new features can be added quickly in the future.

### Raphael

[Raphael](http://raphaeljs.com) seemed like the best Javascript graphics library to use for this project, although I am still researching possible alternatives. Their [graphs package](http://g.raphaeljs.com) looked particularly applicable and straightforward. 

Alternative options might include:

* [HighchartsJS](http://www.highcharts.com)
* [Dojo](http://dojotoolkit.org/features/graphics-and-charting)
