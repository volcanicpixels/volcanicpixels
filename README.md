This repository contains all the code for the Volcanic Pixels website.

[![Build Status](https://travis-ci.org/volcanicpixels/volcanicpixels.png)](https://travis-ci.org/volcanicpixels/volcanicpixels)


[Staging site](https://staging.volcanicpixels.com) - when a commit passes tests it gets pushed automatically to staging server. Staging is completely isolated from production environment and you can use test credit cards e.g. 4242 4242 4242 4242

[Beta tier](https://beta.volcanicpixels.com) - 20% of traffic to www.volcanicpixels.com is transparently served from the beta tier. The beta tier is "live" and runs on production data and thus care must be taken before pushing to beta.

[Live tier](https://www.volcanicpixels.com) - The main website, should be very stable.

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

### Building

To build the project completely run `grunt` from the project root.

Use `grunt watch` to watch for file changes and only rebuild the changed files.

### Testing

We use travis-ci for automated testing, you can manually run the testsuite by running `grunt test`
