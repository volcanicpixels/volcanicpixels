This repository contains all the code for the Volcanic Pixels website.

[![Build Status](https://travis-ci.org/volcanicpixels/volcanicpixels.png)](https://travis-ci.org/volcanicpixels/volcanicpixels)
[![Build Status](https://drone.io/github.com/volcanicpixels/volcanicpixels/status.png)](https://drone.io/github.com/volcanicpixels/volcanicpixels/latest)

## Installation requirements

To install the application you will need the following (other dependencies are installed automatically)

 - Python 2.7
 - PIP 1.3 or newer
 - Git
 - Google App Engine SDK


## How to run application locally

Download the source.

### Install Dependencies

```
pip install -r requirements.txt --target=libs
```

This will install the required dependencies in the 'libs' folder (app engine provides no dependency management system so all libraries must be pushed with the code).

### Launch application using App Engine SDK

Either add the application folder to the GUI and click 'start' or do it from the command line using:

```
dev_appserver.py [path to project]
```
