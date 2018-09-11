evee
=====
 
[![Build Status](https://travis-ci.org/onema/evee.svg?branch=master)](https://travis-ci.org/onema/evee)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/51bb12b95a434798b8044e301659ea85)](https://www.codacy.com/app/onema/evee?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=onema/evee&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/51bb12b95a434798b8044e301659ea85)](https://www.codacy.com/app/onema/evee?utm_source=github.com&utm_medium=referral&utm_content=onema/evee&utm_campaign=Badge_Coverage)
[![Code Climate](https://codeclimate.com/github/onema/evee/badges/gpa.svg)](https://codeclimate.com/github/onema/evee)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/onema/evee/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/onema/evee/?branch=master)

Summary
_______

This is a port for Python `v3.6+` of the Symfony Event Dispatcher.

This event dispatcher follows a pattern called the ["Mediator" pattern](https://sourcemaking.com/design_patterns/mediator).

> In software engineering, the mediator pattern defines an object that encapsulates how a set of objects interact. This pattern is considered to be a behavioral pattern due to the way it can alter the program's running behavior.

Install
--------
`pip install evee`

Usage
--------

### Dispatching simple events

```python
from evee import EventDispatcher
from evee import Event

def pre_foo(self, event: Event, event_name: str):
    print("pre_foo was called")

def post_foo(self, event: Event, event_name: str):
    print("post_foo was called")
        
dispatcher = EventDispatcher()
dispatcher.add_listener('pre.foo', pre_foo)
dispatcher.add_listener('post.foo', post_foo)
dispatcher.dispatch('pre.foo')
print('Doo Foo work')
dispatcher.dispatch('post.foo')
```
