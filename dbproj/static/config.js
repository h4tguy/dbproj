requirejs.config({
  "baseUrl": "../static/lib",
  "paths": {
    "~": "..",
    "app": ".."
  },
  "map": {
    "*": {
      "jquery": "jquery-2.0.0",
      "css": "css-0.0.1",
      "is": "is-0.0.1",
      "json": "json-0.0.1",
      "selector": "selector-0.0.1",
      "zest": "zest-0.0.2",
      "zoe": "zoe-0.0.1"
    },
    "json-0.0.1": {
      "is": "is-0.0.1"
    },
    "selector-0.0.1": {
      "is": "is-0.0.1"
    },
    "zest-0.0.2": {
      "json": "json-0.0.1",
      "css": "css-0.0.1",
      "zoe": "zoe-0.0.1",
      "selector": "selector-0.0.1"
    }
  },
  "packages": [
    {
      "name": "jquery-2.0.0",
      "main": "./index"
    },
    {
      "name": "css-0.0.1",
      "main": "./css"
    },
    {
      "name": "is-0.0.1",
      "main": "./is"
    },
    {
      "name": "json-0.0.1",
      "main": "./json"
    },
    {
      "name": "selector-0.0.1",
      "main": "./selector"
    },
    {
      "name": "zest-0.0.2",
      "main": "./zest"
    },
    {
      "name": "zoe-0.0.1",
      "main": "./zoe"
    }
  ]
});