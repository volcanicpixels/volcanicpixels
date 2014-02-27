This repository contains all the code for the Volcanic Pixels website.

[![Build Status](https://travis-ci.org/volcanicpixels/volcanicpixels.png)](https://travis-ci.org/volcanicpixels/volcanicpixels)


[Staging site](https://staging.volcanicpixels.com) - when a commit passes tests it gets pushed automatically to staging server. Staging is completely isolated from production environment and you can use test credit cards e.g. 4242 4242 4242 4242

[Beta tier](https://beta.volcanicpixels.com) - 20% of traffic to www.volcanicpixels.com is transparently served from the beta tier. The beta tier is "live" and runs on production data and thus care must be taken before pushing to beta.

[Live tier](https://www.volcanicpixels.com) - The main website, should be very stable.

# Project structure

The project has been organised in a modular way - e.g. all the code relating to the SSL pages is in `/volcanicpixels/frontend/ssl/` (including js, css, templates and python).
This means reusing things like the credit-card module is very easy. Note that this is just an extension of MVC, rather than having all models in the same folder the model, view and controller for each module is contained within the module folder.

The `assets` folder contains compiled assets and should not be edited directly.

The `libs` folder contains all the python libraries used by Volcanic Pixels (many of which are our own packages).

## /volcanicpixels/

The `volcanicpixels` folder contains the main python package.

### /volcanicpixels/frontend/

The `frontend` folder contains all the code for the main website, including python, js (es6), css (less) and fonts.

 - **/modules/** contains reusable modules (not directly involved in handling URLs) that include jinja2 templates, es6 javascript, less etc.

### /volcanicpixels/ssl/

The `ssl` folder contains the backend SSL code:
 - creating SSL certificate signing requests - non trivial in pure python
 - SSLCertificate and KeyPair models for database

### /volcanicpixels/users/

The `users` folder contains all the code related to user accounts.

# Building project


To build the project completely run `grunt` from the project root.

Use `grunt watch` to watch for file changes and only rebuild the changed files.

Building does the following:

 - transpiles the es6 modules into regular javascript and wraps them in in AMD closure (puts result in assets)
 - builds requirejs config using bower components
 - compiles less files and creates a styles bundle

# Running application locally

## Requirements

To install the application locally you will need the following (other dependencies are installed automatically)

 - Python == 2.7
 - Google App Engine SDK >= 1.8.2


## Launching


Using the 'App Engine Launcher':

 - add the project folder as a new project
 - Select the application and click run

Using the Command line:

```
dev_appserver.py [path_to_project]
```

## Development

### Requirements

 - Node
 - Bower (`npm install -g bower`)
 - Grunt (`npm install -g grunt-cli`)
 - pep8 (`pip install pep8`)

Install the development dependencies by running `npm install`

### Testing

We use travis-ci for automated testing, you can manually run the testsuite by running `grunt test`
