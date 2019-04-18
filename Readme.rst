pyreaver
-----------------------------

.. image:: https://travis-ci.org/XayOn/pyreaver.svg?branch=master
    :target: https://travis-ci.org/XayOn/pyreaver

.. image:: https://coveralls.io/repos/github/XayOn/pyreaver/badge.svg?branch=master
 :target: https://coveralls.io/github/XayOn/pyreaver?branch=master

.. image:: https://badge.fury.io/py/pyreaver.svg
    :target: https://badge.fury.io/py/pyreaver

Python reaver bindings.


Usage
-----

This library exports a basic aircrack-ng API aiming to keep always a small readable codebase.

This has led to a simple library that executes each of the aircrack-ng's suite commands
and auto-detects its usage instructions. Based on that, it dinamically builds
classes inheriting that usage as docstring and a run() method that accepts
keyword parameters and arguments, and checks them BEFORE trying to run them.

With context managers::

        async def do_scan(session, args, kwargs):
            async with pyreaver.Wash() as reavo:
                await reavo.run(*args, **kwargs)
                while True:
                    await asyncio.sleep(1)
                    with suppress(KeyError):
                        session.scan.results.update(
                            {a.bssid: asdict(a)
                             for a in reavo.sorted_aps()})


::

        async def do_crack(session, args, kwargs):
            """
            async with pyreaver.Reaver() as reavo:
                await reavo.run(*args, **kwargs)
                # TODO: we need to have some way to stop the process.
                while True:
                    with suppress(KeyError):
                        session.crack.results = reavo.meta['result']['lines']
                    await asyncio.sleep(1)

Distributing
------------

Distribution may be done in the usual setuptools way.
If you don't want to use pipenv, just use requirements.txt file as usual and
remove Pipfile, setup.py will auto-detect Pipfile removal and won't try to
update requirements.

Note that, to enforce compatibility between PBR and Pipenv, this updates the
tools/pip-requires and tools/test-requires files each time you do a *dist*
command


Generating documentation
------------------------

This package contains a extra-requires section specifiying doc dependencies.
There's a special hook in place that will automatically install them whenever
we try to build its dependencies, thus enabling us to simply execute::

        pipenv run python setup.py build_sphinx

to install documentation dependencies and buildd HTML documentation in docs/build/


Passing tests
--------------

Running tests should always be done inside pipenv.
This package uses behave for TDD and pytest for unit tests, you can execute non-wip
tests and behavioral tests using::

        pipenv run python setup.py test
