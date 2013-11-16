This repository contains all the code for the Volcanic Pixels website.

[![Build Status](https://travis-ci.org/volcanicpixels/volcanicpixels.png)](https://travis-ci.org/volcanicpixels/volcanicpixels)


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
