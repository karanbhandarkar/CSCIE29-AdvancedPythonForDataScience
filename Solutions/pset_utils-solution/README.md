# pset_utils_starter
Common utilities for psets

A common practice is to keep isolated work in its own repo or python package,
especially if you plan on reusing it across projects.

However, this can be burdensome if you need a new package for *every little
thing.*  Here, we will explore a compromise paradigm that will simultaneously
give us isolation and repeatability without creating needless boilerplate.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Preface](#preface)
  - [Cookiecutter](#cookiecutter)
  - [Git flow](#git-flow)
- [Problems (80 points)](#problems-80-points)
  - [Adapt cookiecutter-pypackage for this course (25 points)](#adapt-cookiecutter-pypackage-for-this-course-25-points)
    - [Defaults (5 points)](#defaults-5-points)
    - [Pytest/Coverage (5 points)](#pytestcoverage-5-points)
    - [Versioning (5 points)](#versioning-5-points)
    - [Convert to docker and pipenv (10 points)](#convert-to-docker-and-pipenv-10-points)
      - [Switching Travis to docker](#switching-travis-to-docker)
  - [Initialize your pset_utils repo (5 points)](#initialize-your-pset_utils-repo-5-points)
  - [Atomic writes (20 points)](#atomic-writes-20-points)
    - [Implement an atomic write (10 points)](#implement-an-atomic-write-10-points)
    - [Test it! (10 points)](#test-it-10-points)
  - [Hashed strings (20 points)](#hashed-strings-20-points)
    - [Implement a standardized string hash (10 points)](#implement-a-standardized-string-hash-10-points)
      - [Proving your work](#proving-your-work)
    - [Test it! (10 points)](#test-it-10-points-1)
  - [Feedback (10 points)](#feedback-10-points)
    - [How many hours did this assignment take?  Too hard/easy/just right? (2 points)](#how-many-hours-did-this-assignment-take--too-hardeasyjust-right-2-points)
    - [What did you find interesting? Challenging? Tedious? (8 points)](#what-did-you-find-interesting-challenging-tedious-8-points)
- [Python Quality (10 points)](#python-quality-10-points)
- [Git History (10 points)](#git-history-10-points)
- [Total Grade](#total-grade)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Preface

**DO NOT CLONE THIS REPO LOCALLY YET**.  We will manually create a repo and link
it.  If you have cloned this repo locally, simply delete
it (it's fine if it's already forked on github).

### Cookiecutter

We will leverage the templating system
[CookieCutter](https://cookiecutter.readthedocs.io/en/latest/)
to give us a head start on best python practices.  Please see the docs for
installation.

On Mac with [Homebrew](https://brew.sh/):
```bash
brew install cookiecutter
```

Cookiecutter has many template projects for various systems, and they are worth
exploring.  For now, we'll use the most common one designed by the author of
cookiecutter: cookiecutter-pypackage.

Cookiecutter uses the templating language
[Jinja2](http://jinja.pocoo.org/docs/2.10/).  When you see something like
`My name is {{ name }}` it means it will be rendered using the variable `name`
when the project is created.

### Git flow

For a package/library, it is especially important that your branching workflow
reflect the 'production' status of your library.

After your initial tag commit of this repo, you ***must*** conform to a formal
git workflow.  This means:

1. Pick [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/) or
   the simplified [Github Flow](https://guides.github.com/introduction/flow/)
   or some similar variant
   * Git Flow has a 'development' branch that is good for quick iterative work,
     but is slightly more complicated otherwise.  Sourcetree has built in tools
     for using it, including automatic tagging.
   * Github Flow means everything is a branch off master.
2. Your `master` branch should be merge-only.  That is, never commit work to it
   directly, only merge from `feature/*`, `develop`, `hotfix/*`, or similar
3. Each new merged commit on master must have a
   [Semantic Versioning](https://semver.org/) release version with an
   accompanying tag.  TL;DR:
   * `major.minor.patch`
   * Patch is for bugfix
   * Minor is for new features
   * Major is for backwards-incompatible changes
   * Don't worry about high version numbers
   * tags should be of the form `v0.1.2`
4. Your work will be graded on your latest tagged version, which should be
   the same as your `master`

## Problems (80 points)

### Adapt cookiecutter-pypackage for this course (25 points)

Fork the cookiecutter-pypackage repo into this classroom by
[accepting this paired assignment](https://classroom.github.com/a/ceaxPcoh).

Be sure to push changes in the template to your fork.  You may continue to
develop that repository throughout the course.  If you make any changes
beyond those instructed, please ensure to mention them in the problem set you
are actively working on.

As you develop the template, be careful to distinguish the top-level files in
the template repo from those of the rendered project, eg:

    cookiecutter-something/
    ├── {{ project_slug }}/
    │   └── setup.py       # Becomes the setup.py in the ***rendered project***
    └── setup.py           # Setup ***this template*** as a package

Refer to the
[cookiecutter docs](https://cookiecutter.readthedocs.io/en/latest/usage.html)
for additional instructions.

#### Defaults (5 points)
Inspect `cookiecutter.json`.  This contains all the defaults and variables for
your project template.  Note that the default value from a list is the first
element; you can reorder as you wish.  You may want to tweak some things:

1. Your name and email
2. `github_username` is the namespace of the repo on github: `csci-e-29`
3. 'project_slug' is overloaded in the template.  It is used for the foldername,
   github repo url, and the package name.  Add in a new option for
   `project_repo` with the same defaults.  Then, search for all uses of
   `project_slug` in the repo and determine if they should be `project_repo`
   instead.  Eg:

       https://github.com/{{ github_username }}/{{ project_repo }}.git

       cookiecutter-something/
       ├── {{ project_repo }}/
       │   ├── {{ project_slug }}/
       │   │   └── __init__.py
       │   └── setup.py
       └── cookiecutter.json

4. Use pytest, don't deploy with travis, don't use click, not open source, no
   pyup badge
5. Remove the weird file `{{project_slug}}/{{project_slug}}.py` and fix the
   import in `tests/test_{{project_slug}}.py`
6. You can remove python 2 and versions below 3.6 from `tox.ini`, `setup.py`,
   and `.travis.yml`.  You can keep 3.7 if you like.

#### Pytest/Coverage (5 points)
Tweak `setup.cfg` for pytest and coverage, to include something like:

```
[tool:pytest]
addopts=--cov={{ cookiecutter.project_slug }} --cov-branch
collect_ignore = ['setup.py']
testpaths = {{ cookiecutter.project_slug }} tests
python_files = test.py tests.py test_*.py tests_*.py *_test.py *_tests.py

[coverage:run]
omit:
    */test.py
    */tests.py
    */test_*.py
    */tests_*.py
    */*_test.py
    */*_tests.py
    */test/*
    */tests/*
```

#### Versioning (5 points)
The default relies on [Bumpversion](https://pypi.org/project/bumpversion/) to
set versions, but I don't find it to work very well.  We will configure the
template to use [setuptools_scm](https://github.com/pypa/setuptools_scm/) to
automatically get your package version from your git repo, a nice automation.

1. Delete all references to bumpversion in `setup.cfg` and the manual version
   specifiers it lists.
2. Update your `setup.py` and requirements_dev as specified in the help docs.

Add the following to `{{ project_slug }}/__init__.py` instead of `__version__`:

```python
from pkg_resources import get_distribution, DistributionNotFound

...

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    from setuptools_scm import get_version
    import os
    __version__ = get_version(
        os.path.dirname(os.path.dirname(__file__))
    )

```

When you later pip install a rendered project, if installed from a clean repo
with a tag version, you'll get a nice version like `0.1.2`.  If, however, you
inspect the `__version__` in your package from your git repo, you'll get a nice
'dirty' version number like `'0.2.1.dev0+g850a76d.d20180908'`.  This is useful
for debugging, building sphinx docs in dev, etc, and you never have to specify
a version except via tagging your commit.

#### Convert to docker and pipenv (10 points)

The default project template relies on [travis](https://travis-ci.com/) and
[tox](https://tox.readthedocs.io/en/latest/) for repeatable testing of a matrix
of libraries, which is nice.  For local development though, we'll want something
more straightforward: docker and pipenv.

Start with the `docker-compose.yml` from Pset0 and the following tweaked
`Dockerfile`:

```docker
FROM python:3.6 AS base
ENV PIP_NO_CACHE_DIR off
ENV PYTHONPATH="/app:${PYTHONPATH}";
RUN pip3 install pipenv

WORKDIR /app
```

If you'd like, create a shortcut executable `drun_app`:

```bash
touch drun_app
chmod +x drun_app
```
with the content:
```bash
#!/usr/bin/env bash

docker-compose run app "$@"
```

This is just a nice shortcut so the following are equivalent:

```bash
docker-compose run app python somefile.py
./drun_app python somefile.py
```

Now we need to initialize the Pipfile.  This will not work in the template
directly; you need to render it:

```bash
cookiecutter your_template_repo/  # Accept all the defaults
cd python_boilerplate # or whatever the new project is called

# Build the docker image in the new project
docker-compose build

# Create the Pipfile's

# We can either start from scratch...
# Include ipython if you want, at the cost of a larger/slower image
./drun_app pipenv install pytest pytest-runner pytest-cov sphinx setuptools_scm --dev

# Or you can use what's in the existing requirements_dev, although it's outdated
./drun_pap pipenv install -r requirements_dev.txt --dev

# Now we need to copy those back
mv Pipfile ../cookiecutter-csci-package-gorlins/\{\{cookiecutter.project_repo\}\}/
mv Pipfile.lock ../cookiecutter-csci-package-gorlins/\{\{cookiecutter.project_repo\}\}/
```

Finally, we must tell Docker to use that pipenv!  Add this to the end of the
`Dockerfile` in your template:

```docker
COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --dev
```

And finally...

```bash
# Delete the boilerplate project if you need to
cookiecutter your_template_repo
cd python_boilerplate
docker-compose build
./drun_app pytest # Should work!
```

Note that as you develop a new app, to include packages, you must rebuild, eg:

```bash
./drun_app pipenv install numpy          ## For an actual requirement, or
./drun_app pipenv install ipython --dev  ## if only needed for development

docker-compose build
./drun_app ipython
```

Be sure to include the reqs in your `setup.py` as well!

Feel free to update the `CONTRIBUTING.rst` or any other documentation files
for the generated project to help you remember how to use the newly templated
projects.

##### Switching Travis to docker

Finally, let's tell Travis to use our docker environment instead of tox for
testing.  We may revist the matrix features in tox/travis later; we don't need
them now.  This way, travis will test code identically to how you do so via
docker.

Update your `.travis.yml` to look something like:

```yaml
# Config file for automatic testing at travis-ci.org

sudo: required
language: minimal
services:
  - docker

# Command to install dependencies, e.g. pip install -r requirements.txt --use-mirrors
install: docker-compose build

jobs:
  include:
    - stage: test
      # Command to run tests, e.g. python setup.py test
      script: ./drun_app <SCRIPT>
```
where you must replace `<SCRIPT>` with the appropriate Jinja logic to run
`pytest` or `python setup.py test` as requested by the template variables.  See
other parts of the original template for hints to handle Jinja templating.

### Initialize your pset_utils repo (5 points)

Let's create a new repo from CookieCutter:

```bash
cookiecutter cookiecutter-csci-package-yourname/
```

Name the folder so it matches your fork of this repo, and the project slug
should be `pset_utils`.

Ensure docker and pytest are working for this repo locally.

Now we'll manually create and merge this with your github repo.  Initialize the
new project folder as a git repo, eg via:

```bash
cd <pset_utils folder>
git init
git remote add origin git@github.com:csci-e-29/your_repo.git
git fetch
git merge origin/master
```

If you have any issues, you can try
 `git merge origin/master --allow-unrelated-histories`

**Commit the rendered project files now** and push to github.

Because of the `.travis.yml` file, TravisCI should queue up a build.  You
can see this on your commits page in your repo - there may be a yellow circle,
green check, or red 'X' next to your commit depending on the status of the build.
Click on it and look through the logs and ensure it is running your tests.

Note that you should NOT rely solely on Travis to run tests.  They are there as
a trusted runner and failsafe, but you should ideally get tests to pass locally
before pushing new builds.

If you find travis runs too many builds, you can further set up [Conditional
Builds](https://docs.travis-ci.com/user/conditional-builds-stages-jobs/) so
that tests only run on master or develop, or on pull requests to them.

**[Add a build badge](https://docs.travis-ci.com/user/status-images/)** to the
top of this README, using the markdown template for your master branch.  Add
one for the develop branch too if you're using Git Flow.

**Tag your master `v0.1.0` (or whatever initial version you chose)**.
From here on, you should conform to a formal workflow for this repo.

### Atomic writes (20 points)

Create a package within your `pset_utils.io`.  We will implement an
atomic writer.

Atomic writes are used to ensure we never have an incomplete file target.
Basically, they perform the operations:

1. Create a temporary file which is unique (possibly involving a random file
   name)
2. Allow the code to take its sweet time writing to the file
3. Rename the file to the target destination name.

If the target and temporary file are on the same filesystem, the rename
operation is ***atomic*** - that is, it can only completely succeed or
fail entirely, and you can never be left with a bad file state (assuming the
code writes the data you wanted without failing).

See notes in
[Luigi](https://luigi.readthedocs.io/en/stable/luigi_patterns.html#atomic-writes-problem)
and the [Thanksgiving Bug](https://www.arashrouhani.com/luigi-budapest-bi-oct-2015/#/21)

#### Implement an atomic write (10 points)

**Nota Bene**: We are now starting a feature.  Be sure to commit this work on
a feature branch.

Start with the following:

```python
@contextmanager
def atomic_write(file, mode='w', as_file=True, **kwargs):
    """Write a file atomically

    :param file: str or :class:`os.PathLike` target to write
    :param bool as_file:  if True, the yielded object is a :class:File.
        Otherwise, it will be the temporary file path string
    :param kwargs: anything else needed to open the file

    :raises: FileExistsError if target exists

    Example::

        with atomic_write("hello.txt") as f:
            f.write("world!")

    """
    ...
```

 Key considerations:

 * You can use [tempfile](https://docs.python.org/3.6/library/tempfile.html),
   write to the same directory as the target, or both.
   What are the tradeoffs?  Document in your code.
 * Ensure the file is deleted if the writing code fails
 * Ensure the temporary file has the same extension(s) as the target.  This is
   important for any code that may infer something from the path (eg, `.tar.gz`)
 * If the writing code fails and you try again, the temp file should be new -
   you don't want the context to reopen the same temp file.

***From now on, use this function whenever writing a file for this class.***

#### Test it! (10 points)

Write some unittests.  They should live next to the module, eg
`pset_utils.io.tests:AtomicWriteTestCase`.

### Hashed strings (20 points)

It can be extremely useful to ***hash*** a string or other data for various
reasons - to distribute/partition it, to anonymize it, or otherwise conceal the
content.

#### Implement a standardized string hash (10 points)

Use `sha256` as the backbone algorithm from
[hashlib](https://docs.python.org/3.6/library/hashlib.html).

A `salt` is a prefix that may be added to increase the randomness or otherwise
change the outcome.  It may be a `str` or `bytes` string, or empty.

Implement it in `pset_utils.hashing:hash_str`, where the return value is the
`.digest()` of the hash, as a `bytes` array:

```python
def hash_str(some_val, salt=''):
    ...
```

Note you will need to `.encode()` string values.

As an example, `hash_str('world!', salt='hello, ').hex()[:6] == '68e656'`

To help us deal with private data later, here is a special random salt I captured
from [random.org](https://www.random.org):

```python
CSCI_SALT = bytes.fromhex(
    "d4 b5 1b 2a 6c e0 2b b8 e8 29 ce 45 18 b0 f9 c0"
    "a8 f4 ec 6b 59 36 01 89 b1 be 69 26 1e 05 75 bc"
    )
```

##### Proving your work
It's great to have answers in this README, but we can also make Travis run
answers even if they are not part of a formal test suite.  Create a `main.py`
at the top level of this repo (ie it's not part of your installable package)
and add the following stage to your `.travis.yml` jobs:

```
    - stage: deploy
      if: branch = master
      script: ./drun_app python main.py
```
Note: only do this for fast-running jobs in the future, and only if their
data is self-contained.  We can't overload Travis.  You don't need to use this
approach for every answer.

See [Build Stages](https://docs.travis-ci.com/user/build-stages/) for reference.

**What is the hash of the instructor's github username (`gorlins`)**, in hex,
using the `CSCI_SALT`?

**What is the hash of your (lowercase) github username**, in hex, using
the `CSCI_SALT`?

#### Test it! (10 points)

Write some unittests for your hashing functions.

### Feedback (10 points)

#### How many hours did this assignment take?  Too hard/easy/just right? (2 points)

#### What did you find interesting? Challenging? Tedious? (8 points)

## Python Quality (10 points)
Notes from TA may go here

## Git History (10 points)
Notes from TA may go here

## Total Grade
Notes from TA may go here

## Solution
The following is a list of notes about the published solution:

1. The .git directory is stripped off.

2. All the code are peoperly commented whenever necessary.

3. The username is solution. The author name is Solution Solution.

4. To test in local pipenv enviroment, run the following commands to set up pipenv
environment and install all packages specified in Pipefile:
   $ cd /path/to/project
   $ pipenv install
   $ pipenv check

Then, run the following command to test:
   $ cd pset_utils
   $ pipenv run pytest

5. To test in Docker container, run the following commands to build image and launcg 
container:
   $ cd /path/to/project
   $ docker-compose build
   $ ./drun_app python main.py

You can start a Python interactive interpreter to troubleshoot:
   $ ./drun_app python

You also can start a bash shell to troubleshoot:
   $ ./drun_app bash

6. To test in Travis CI, run the following command to create a local repo:
   $ cd /path/to/project
   $ git init

Then, creare an empty remote repo in your own GitHub account. 

Then, link up your local repo with the remote repo.

Note that you need to replace the placehold (username solution) with your own GitHub username. 
