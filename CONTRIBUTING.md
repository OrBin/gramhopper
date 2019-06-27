# Contributing to gramhopper
Thanks for getting interested in contributing to gramhopper! :clap::clap:

This document is a set of guidelines to help you contribute the project.

## Reporting bugs
Bug reports are the easiest contributions one can do, and maybe the most important ones.

Before [reporting a bug](https://github.com/OrBin/gramhopper/issues/new), please make sure (as much as you can) that
this is really an issue caused by a bug in gramhopper.

When reporting a bug, please provide as much information as possible, to help us identify and solve it easily.
Please follow the bug report template (which appears when creating an issue) and fill all applicable fields

## Contributing code

### Find an issue to work on
Look at issues tagged with [good first issue](https://github.com/OrBin/gramhopper/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22+) label and find one you'd like to work on.

### How to build and test
We use [Invoke](http://docs.pyinvoke.org) CLI to execute development tasjs like test, build, lint, etc.

#### Building
To build, run:
```bash
invoke build
```
You can also use flags with this command:
* Use `--no-package` to avoid building the package.
* Use `--no-docker-image` to avoid building the docker image.
* Use `--docs` to build the documentation, too.
* You can combine these flags however you want.

#### Testing
To run tests, run:
```bash
invoke test
```
Testing Telegram bots require a bot token, so we provide a pre-created token that's already configured for you.<br>
To override this token, set the environment variable `TOKEN` before running tests.

The same applies for a chat ID to test with, which you can override with the environment variable `CHAT_ID`.

### Follow the style guide
Our code generally follows PEP8, with some exceptions.
We use some linters to make sure we keep following the required style. To run them all, run:
```bash
invoke lint
```
If you have a lint error, fix it; don't add a comment to ignore it.

### Submit a pull request
TODO

## Improving documentation
Improving documentation is a great way to contribute, too!

Our documentation is built using [Sphinx](http://www.sphinx-doc.org/).
It is based on RST files located in [`docs/`](https://github.com/OrBin/gramhopper/tree/dev/docs/source) directory, and on docstrings in the python code.<br>
Find [here](https://github.com/OrBin/gramhopper/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3Adocumentation+) issues related to documentation.

#### Building the documentation
To build the documentation, run:
```bash
invoke build-docs
```
The build output will be in `docs/build` directory.<br>
To clear the documentation build outputs, run:
```bash
invoke clean --docs
```

## Code of conduct
This project is governed by the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to follow this code.
