git-branchhealth
===============

[![PyPI version](https://badge.fury.io/py/gitbranchhealth.svg)](http://badge.fury.io/py/gitbranchhealth) [![Build Status](https://travis-ci.org/jwir3/gitbranchhealth.svg)](https://travis-ci.org/jwir3/gitbranchhealth)

A tool for determining the health of branches in a git repository. The tool will give you the amount of time since git branches have been modified.

Each git branch is also given a color indicating its health: green for healthy (the branch was updated recently), yellow for somewhat unhealthy (branch hasn't been updated lately, but it's unclear whether the branch is too old to be used), or red for stale (the branch hasn't been updated in a long time).

Installation
---------------
Using pip:
```
pip install gitbranchhealth
```

From source or release tarball:
```
cd gitbranchhealth
sudo python setup.py install
```

Usage
---------------
Basic usage:

```
git branchheath <path-to-repo>
```

Configuration/Options
---------------
`git-branchhealth` uses the `git` configuration file to specify most options,
but they are also available to be passed in on the command line.

If you choose to specify a configuration option, use the section header `[branchhealth]`.

| Option Name |    Description    | Command Line Flag | Configuration File Option |
| ----------- | ----------------- | ----------------- | ------------------------- |
| noColor     | Specify not to use ANSI colors when printing the branch health results. | -n, --nocolor | nocolor |
