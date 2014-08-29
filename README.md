git-branchhealth
===============

* [![PyPI version](https://badge.fury.io/py/gitbranchhealth.svg)](http://badge.fury.io/py/gitbranchhealth)
* [![Build Status](https://travis-ci.org/jwir3/gitbranchhealth.svg)](https://travis-ci.org/jwir3/gitbranchhealth)

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

| Option Name |    Description    | Default Value |  Command Line Flag  |  Configuration File Option  |
| ----------- | ----------------- | ------------- | :-----------------: | :-------------------------: |
| Bad Branches Only | Show only branches that are identified as being "unhealthy". | N/A | -b, --bad-only | - |
| No Branch Ignoring    | Specify that no branches should be ignored. Normally, all branches titled "HEAD" or "master" are ignored, as these are considered "special", and reporting/deletion should not happen on them. If this option is specified, these branches are included in reporting and deletion with all of the other branches. | N/A | --no-ignore | noignore |
| No Color     | Specify not to use ANSI colors when printing the branch health results. | N/A | -n, --nocolor | nocolor |
| Remote Name  | Specify the name of a remote repository on which to operate. | `None` (Operate on local repository only) | -r `<remote name>` | - |
| Verbose Output | Make `gitbranchhealth` output as much information on the command line as possible. | N/A | -v | - |
