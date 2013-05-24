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

###

Developer Toolkit
---

This project uses a couple of open-source tools. They include the following:

###Foundation

The [Zurb Foundation](http://foundation.zurb.com) CSS framework was very useful for quickly producing a clean layout that scales easily.

####Editing the CSS

It is inadvisable to edit the CSS directly. It would be better edit the SCSS provided as described in the [Zurb Documentation](http://foundation.zurb.com/docs/sass.html). To do so, you will need to install the compass gem. To get going, watch the SCSS files for changes by running `compass watch` in the project directoy. The `config.rb` file is set up so that you don't need to specify files to watch, etc.

###Angular JS

