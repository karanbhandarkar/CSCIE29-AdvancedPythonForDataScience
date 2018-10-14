# Pset 2

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Problems (80 points)](#problems-80-points)
  - [Including pset_utils (15 points)](#including-pset_utils-15-points)
    - [Docker/pipenv prep](#dockerpipenv-prep)
    - [Create a Github API token](#create-a-github-api-token)
    - [Install the utils!](#install-the-utils)
    - [Including the utils tests](#including-the-utils-tests)
  - [Student Embeddings (40 points)](#student-embeddings-40-points)
    - [Loading the data (5 points)](#loading-the-data-5-points)
    - [Embedding (20 points)](#embedding-20-points)
    - [Cosine similarity (5 points)](#cosine-similarity-5-points)
    - [Find your friends (10 points)](#find-your-friends-10-points)
  - [Atomic (re)writes (15 points)](#atomic-rewrites-15-points)
  - [Feedback (10 points)](#feedback-10-points)
    - [How many hours did this assignment take?  Too hard/easy/just right? (2 points)](#how-many-hours-did-this-assignment-take--too-hardeasyjust-right-2-points)
    - [What did you find interesting? Challenging? Tedious? (8 points)](#what-did-you-find-interesting-challenging-tedious-8-points)
- [Python Quality (10 points)](#python-quality-10-points)
- [Git History (10 points)](#git-history-10-points)
- [Total Grade](#total-grade)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Problems (80 points)

Before you create a local repo for this pset, skim through the problems and
decide how much of the work to include in your cookiecutter template first or
`pset_utils`, vs just in this repo.  Justify each decision.

Initiate a new local project folder using your cookiecutter repo, then manually
link to this remote origin as you did last time.  This project stub should be
named `pset_02`.  You may structure the interior as you like, so long as
anything you add and call from your `main.py` is importable from the top, eg:
`from pset_02 import WordEmbedding`.

### Including pset_utils (15 points)

Normally, we can pip/pipenv install straight from github to any Docker image or
Travis build.  However, we have a few hoops to jump through since `pset_utils`
is a private repo and we're not managing all of the deploy keys.  Inside a
company with a private VPN/version control/build system, best practice is just
to make everything publicly readable behind the VPN and not deal with deploy
authentication.

We have a few choices:

1. Create a deploy/user key for SSH.  This is preferred, but is a bit trickier
   to manage, especially on windows.
2. Hard code your git username/password into your dockerfile (no, we are not
   going to do that!)
3. Provide an API token through the environment.  This will allow us to clone
   via https without altering our Pipfile.  This option should be the easiest
   for this class.

You can decide how to capture this process in your cookiecutter repo.  
Technically, it would be poor form to automatically install a package you may
not need, but that is ok for this course.  You can also just capture the token
aspects without preinstalling pset_utils.  Document your decisions here.

#### Docker/pipenv prep

Oh no! We made a slight mistake last time with our `Dockerfile`.  According to
[this
post](https://stackoverflow.com/questions/46503947/how-to-get-pipenv-running-in-docker),
best practices indicate that we should only install the locked requirements
(`--ignore-pipfile`) and also enable the `--deploy` flag.  While we're editing,
let's add some of those `ENV` arguments linked in the
[template](https://github.com/wemake-services/wemake-django-template/blob/master/%7B%7Bcookiecutter.project_name%7D%7D/docker/django/Dockerfile)
there:

```docker
ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PIPENV_HIDE_EMOJIS=true \
  PIPENV_COLORBLIND=true \
  PIPENV_NOSPIN=true \
  PYTHONPATH="/app:${PYTHONPATH}"

WORKDIR /build

...

RUN pipenv install --system --deploy --ignore-pipfile --dev
WORKDIR /app
```

Also note the new WORKDIR directive before we start copying files into the Docker
image, and the revert back to the app dir after we're done.  This will prevent
some issues between the editable repo installs when we're mounting the local
folder into /app when we're running.

Be sure to update this part in your cookiecutter!

#### Create a Github API token

See Travis docs
[here](https://docs.travis-ci.com/user/private-dependencies/#api-token). Note:
To access personal tokens, on the GitHub Applications page, you need to click
Developer Settings, or directly navigate
[here](https://github.com/settings/tokens).

DO NOT SHARE THIS TOKEN WITH ANYONE.  It gives access to all your github repos.
If it becomes compromised, delete it from github and generate a new one.  You
will be uploading this token to Travis, but it is private only to you.

For more reference on security, see [Travis Best
Practices](https://docs.travis-ci.com/user/best-practices-security/#recommendations-on-how-to-avoid-leaking-secrets-to-build-logs)
and [Removing Sensitive
Data](https://help.github.com/articles/removing-sensitive-data-from-a-repository/).

Add the following lines to your Dockerfile, just below the `FROM` line:
```docker
ARG CI_USER_TOKEN
RUN echo "machine github.com\n  login $CI_USER_TOKEN\n" >~/.netrc
```

And modify the build section in your `docker-compose.yml`:
```
build:
  context: .
  args:
    - CI_USER_TOKEN=${CI_USER_TOKEN}
```

You then need to set `CI_USER_TOKEN` as an environment variable, either in your
`~/.bashrc` or `~/.bash_profile` on Mac/Linux, or create a
[dotenv](https://docs.docker.com/compose/env-file/) file in the project
directory (you ***must*** add files like this to your `.gitignore`), or
similarly with a [docker-compose
override](https://docs.docker.com/compose/extends/#multiple-compose-files).  Note
that environment variables can be tricky if you aren't familiar with how to use
them; the `.env` file may be the easiest approach, but will need to be copied
to each new project, since you can't commit it to your cookiecutter repo
(although, you could keep the file in your local cookiecutter repo, so long
as it is ignored by git!).

You must then add the variable to the Travis environment as well; you can do
that via navigating to the settings, eg
https://travis-ci.com/csci-e-29/your_repo/settings, via the [Travis
CLI](https://github.com/travis-ci/travis.rb), or encrypting into the
`.travis.yml` as instructed on the first Travis link above.  The token should
NOT be committed to your repo in plain text anywhere.  You could automate the
encryption via cookiecutter, but it would take a bit of experimentation with
your hooks - you would need to run something like `travis encrypt -r {{ owner
}}/{{ repo }} CI_USER_TOKEN=123 --add`.  You are not required to automate this
for the purpose of this pset!

#### Install the utils!

You can now install your `pset_utils` as below.  Note that the #egg part is
important, it is not a comment!

```bash
./drun_app pipenv install -e git+https://github.com/csci-e-29/pset_utils-you#egg=pset_utils
```

This will include the latest master commit (presumably tagged) and will be
automatically updated whenever you run `pipenv update`.  If you want to be more
specific about the version, you can use the `@v1.2.3` syntax when you install,
or add `ref='v1.2.3` to the specification in the `Pipfile`.  Leaving this to
automatically check out the latest master is easiest and a good reason to have
merge-only master releases!

#### Including the utils tests

In your `setup.cfg`, update the `addopts` section to include `--pyargs`.  At
this point, after building the docker image, `pytest pset_utils` should run all
the tests in your utils package!

You can run them by default if you like, by adding `pset_utils` to `testpaths`
in the [config
file](https://docs.pytest.org/en/documentation-restructure/how-to/customize.html#confval-testpaths).

Otherwise, you should update your `.travis.yml` to explicitly run them.  You
can do so in the same test stage, or you could create a separate test stage
just to test your utils.  Normally, the latter is preferred - it gives nice
isolation.  However, it will require travis to rebuild your docker image, which
is suboptimal.

### Student Embeddings (40 points)

Note: The below includes a good amount of markdown math embedded between "$"'s.
If it doesn't render well for you, try copying into [CodeCogs](https://www.codecogs.com/latex/eqneditor.php).

In this repository, we have included three files:

1. `data/words.txt` contains  a list of 9844 common words
2. `data/vectors.npy.gz` is a 9844x300 embedding matrix. Each row of the matrix
is the 300-dimensional vector representation for the word at the same position in
the vocab list (first row <-> first word in list, ... etc).  You can load this
with `numpy.load`.
3. `data/hashed.xlsx`, a tablular dataframe containing hashed github user ids,
data from the demographics survey on what students hope to learn in the course,
and answers from pset 0 about a python project you have completed

(Note that we should not have committed these to the repo... we fill fix that
later!)

You will likely need to install a few packages into your pipenv to make this
work: `pandas`, `numpy`, and `xlrd`.

#### Loading the data (5 points)

You will need to write functions to load the three datasets:

```python

def load_words(filename):
    """Load a file containing a list of words as a python list

    :param str filename: path/name to file to load
    :rtype: list
    """
    ...


def load_vectors(filename):
    """Loads a file containing word vectors to a python numpy array

    :param filename:

    :returns: 2D matrix with shape (m, n) where m is number of words in vocab
        and n is the dimension of the embedding

    :rtype: ndarray
    """
    ...

def load_data(filename):
    """Load student response data

    :param str filename:

    :returns: dataframe indexed on a hashed github id
    :rtype: DataFrame
    """
    # You will probably need to fill a few NA's and set/sort the index via
    # pandas
    ...

```

#### Embedding (20 points)

You will need to perform basic tokenization.  You can do something like:

```python
import re
def tokenize(text):
    # Get all "words", including contractions
    # eg tokenize("Hello, I'm Scott") --> ['Hello', "I'm", "Scott"]
    return re.findall("\w[\w']+", text)
```

Be sure to test your implementation!  You may want to add things like ensuring
all tokens are lowercase (eg `some_str.lower()`) to ease lookup into the
vectors.

You then need a class to perform the mapping.  Create a class called
`WordEmbedding`, that is initialized with two arguments: the word list and the
vectors.  Implement the embedding as the `__call__` method as well as a helper
constructor to load from files (we do this to help with testing):

```
class WordEmbedding(object):
    def __init__(self, words, vecs):
        ...

    def __call__(self, word):
        """Embed a word

        :returns: vector, or None if the word is outside of the vocabulary
        :rtype: ndarray
        """

        # Consider how you implement the vocab lookup.  It should be O(1).
        ...

    @classmethod
    def from_files(cls, word_file, vec_file):
        """Instanciate an embedding from files

        Example::

            embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')

        :rtype: cls
        """
        return cls(load_words(word_file), load_vectors(vec_file))
```

Finally, we need a way to combine embeddings for multiple words into a 'document
embedding', aka a single vector for an entire body of text.  We'll take the
simple approach of just adding the vectors:

```python
class WordEmbedding(object):
    ...
    def embed_document(self, text):
        """Convert text to vector, by finding vectors for each word and combining

        :param str document: the document (one or more words) to get a vector
            representation for

        :return: vector representation of document
        :rtype: ndarray (1D)
        """
            # Use tokenize(), maybe map(), functools.reduce, itertools.aggregate...
            # Assume any words not in the vocabulary are treated as 0's
            # Return a zero vector even if no words in the document are part
            # of the vocabulary
            ...
```

To wrap it all up, you can use [Pandas apply](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.apply.html?highlight=apply#pandas.Series.apply)
to execute your code in a functional way:

```python
embedding = ...
data = ...

vecs = data['learn'].apply(embedding.embed_document) \
    + data['project'].apply(embedding.embed_document)
df = pandas.DataFrame([v for v in vectors.values], index=vectors.index)
```

Note the initial result will be a Series object preserving the index with vectors
inside, which is why we transformed it back into DataFrame with float types.

Write the final data frame to `data/embedded.csv` using `df.to_csv()` and your
atomic writer.  Do not commit the file!  Ensure `data/` is in your `.gitignore`.


#### Cosine similarity (5 points)

Since words are being represented as vectors, we can compute a distance metric
to  represent how "similar" two words are. There are a couple of distance
metrics we can use - [cosine
similiarity](https://en.wikipedia.org/wiki/Cosine_similarity) is a  commonly
used one. Cosine similarity is defined as:

$$
similarity(A, B)
= cos(\theta)
= \frac {A \cdot B} {\left\| A \right\| \left\| B \right\| }
= \frac {\sum A_i B_i} { \sqrt{\sum A_i^2} \sqrt{\sum B_i^2} }
$$

Implement a method
`cosine_similarity(a, b)` that computes cosine similiarity for two vector
inputs. Be sure to test it.  Hint: look at `numpy.dot` and `numpy.linalg.norm`.

#### Find your friends (10 points)

Because we committed the salt to our repository last time, we cannot actually
use it!  The id's in this set were generated with a different salt viewable
in the canvas assignment:

```bash
# This is the hexrep of bytes, can be read with bytes.fromhex("123abc...")
SALT=123abc....
```

You must inject this into your environment, load it at run time using
`os.environ` or a command line arg, and find the new hash of your github ID to
find yourself in this set.  DO NOT COMMIT THE NEW SALT TO ANY REPO.

The hashed ids were taken with a lower-case version of the github id.

You can encapsulate a distance function for yourself, something like:

```python
# Load vecs back from your written data/embedded.csv, and set the index
vectors = ...
my_vec = vectors[my_hashed_id]
def my_distance(vec):
    return 1 - cosine_similarity(vec, my_vec)

distances = vectors.apply(my_distance)
```

Note the comment above to load your data back - do not just continue using the
same in-memory dataframe.  The reasoning will become clear in future psets.
You can use `pandas.read_csv`.

Find the 5 students closest to you and the 5 students furthest from you in
document space.  Consider tools like `numpy.argsort` and `DataFrame.sort_values`
etc.  Be sure to exclude students with no answers or where `distance == 1`

For each student in the nearest/furthest, print their hashed id, the distance,
and their responses.

Discuss the results - do they look meaningful?

### Atomic (re)writes (15 points)

During a late-night reading session, you notice that someone else has implemented
an [atomic writer](https://pypi.org/project/atomicwrites/) for python!  Almost
certainly they have done a better job of ensuring it works correctly, and we
don't want the responsibility of maintaining this kind of thing!  However, we
have already written code using our `pset_utils.io:atomic_write` manager.

To maintain backwards compatibility, you should ***rewrite your atomic_write***
function to use the published package in the backend, without your code knowing.
Note that this package may not implement every feature you did, such as
preserving the extension.  You must find a way to ensure they are still
implemented!

Here are a few tips you can use:

```python

# You can import and rename things to work with them internally,
# without exposing them publicly or to avoid naming conflicts!
from atomicwrites import atomic_write as _backend_writer, AtomicWriter

# You probably need to inspect and override some internals of the package
class SuffixWriter(AtomicWriter):

    def get_fileobject(self, dir=None, **kwargs):
        # Override functions like this
        ...

@contextmanager
def atomic_write(file, mode='w', as_file=True, new_default='asdf', **kwargs):

    # You can override things just fine...
    with _backend_writer(some_path, writer_cls=SuffixWriter, **kwargs) as f:
        # Don't forget to handle the as_file logic!
        yield f
```

Since you already wrote tests for the writer, they should still all pass when
you appropriately achieve backwards compatibility (assuming you have tested
all the features!)

Ensure that the `atomicwrites` package is appropriately added to your
`pset_utils` `setup.py`, and when you update in this project, you should notice
that pipenv has installed it here too via the dependency chain.

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
environment and install all packages specified in Pipefile.lock:
   $ cd /path/to/project
   $ pipenv install
   $ pipenv check

Then, run the following command to test:
   $ cd pset_02
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
