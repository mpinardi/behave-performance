# Behave_Performance

A concurrent behavior driven testing(CBDT) tool and performance testing framework for Behave.

## What is Behave Performance?
Behave_Performance is a tool to simulate concurrent user behavior using gherkin features as runner specification.

### What is Behave?
Behave is a implementation of [Behavior Driven Development](https://en.wikipedia.org/wiki/Behavior-driven_development) [(BDD)](https://cucumber.io/docs/bdd/).
Which uses simple natural language scripts to define a software feature.
These executable specifications are written in a language called [Gherkin](https://cucumber.io/docs/gherkin/).
Example:
```
#beer.feature
Feature: Beer
  Scenario: Jeff dinks a beer
	  Given: Jeff is of age and has a beer
	  And: Jeff opens his beer.
	  When: Jeff takes a sip.
	  Then: Verify he enjoyed it.
```

These scripts can be used to develop the features themselves but also drive [automated tests](https://cucumber.io/docs/guides/10-minute-tutorial)

### The issue?
So, you now have a working functional automation test suite.
But you want to run a performance test. Generally, this would require either rewriting your existing functional tests or copying a bunch of code.
Also, you would need to create or implement a performance test harness.

Most likely each team will end up with something that is project specific and doesn't use the existing functional code base.

### The fix?
Behave Performance provides a level of automation on top of Behave.
And is an implementation of a oncept called Concurrent Behavior Driven Testing (CBDT).

## What is Concurrent Behavior Driven Testing?
Concurrent Behavior Driven Testing (CBDT) is the concept of using BDD features to simulate real world concurrent events. 

Most systems have multiple concurrent users who may be using different but complementary features, which been previously defined in [Gherkin](https://cucumber.io/docs/gherkin/).
CBDT allows you to document these real world situations in a simple human readable domain-specific scripting language.

CBDT requires an automation team to follow strict guidelines when coding functional test cases.
Being careful to avoid static variables and race conditions that will cause failures in a multiple-threaded world.
This of course requires a larger understanding of programming or at least team leadership that can enforce these guidelines.

## How does Behave Performance work?
Behave Performance provides a means to use your existing functional tests without writing a single line of code.
It provides the ability to run performance simulations with support for common load testing features:
* Timed Tests
* Multi-Processing/Threading
* Thread Count Limits
* Ramp Up/Down
* Data replacing
* Random Wait
* Statistics
* Console reporting
And creates a number of outputs
* Data Points (csv)
* Logging
* Summary Report
* Taurus Final Stats

It uses a new type of script called Salad.
Salad is a re-implementation of Gherkin with the focus on performance simulations.

```
Plan: Bar visit

Simulation: Jeff drinks 3 beers.
  Group: beer.feature
  Runners: 1
  Count: 3
```
## Plans:
Here is an example plan
```
Plan: test
Simulation: simulation 1
Group test.feature
	#slices
	#these values will replace property "value out"
	|value out|
	|changed value 1|
	|changed value 2|
	#number of threads
	Runners: 2
	#total number of threads to run.
	Count: 2
#a optional random wait mean for before thread runs tests.
#thread will wait between +-50% of this mean
RandomWait: 00:00:02

#Will run all groups for the period below
Simulation Period: simulation 2 period
Group test.feature
	|value out|
	|changed value |
		Threads: 5
		#count is ignored in a simulation period
		Count: 1
#run time
Time: 00:00:30
RampUp: 00:00:10
RampDown: 00:00:10
```

## Getting Started
It takes some planning to implement Behave Perf.

Your functional automation should follow these rules:
* Use a non specific test harness. This should standardize all your common functions.
* Thread safety should always be in mind
* Properly comment your features and scenarios. You want to keep track of what scenarios can be run multithreaded.

Follow directions in [wiki](https://github.com/mpinardi/behave-performance/wiki) to get up and running.

## Install
  From pip:
  > pip install behave_performance

  You can install with Pip from file:
  wheel
  >  pip install behave_performance-0.5.0-py3-none-any.whl

  Tar.gz
  >  pip install behave_performance-0.5.0.tar.gz

## Dev 
  ### Install
    From Pipfile
    > pipenv install
    or
    > pipenv sync

    Pip from requirements:
    >  pip install -r requirements.txt
  
  ### Build
    You can build with setup.py
    >  python setup.py sdist bdist_wheel

  ### Test
    You can run unit tests using pytest
    >  pytest

## Versioning
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details