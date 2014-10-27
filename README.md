git-branchhealth
===============

* [![PyPI version](https://badge.fury.io/py/gitbranchhealth.svg)](http://badge.fury.io/py/gitbranchhealth)
* [![Build Status](https://travis-ci.org/jwir3/gitbranchhealth.svg)](https://travis-ci.org/jwir3/gitbranchhealth)

A tool for determining the health of branches in a git repository. The tool will give you the amount of time since git branches have been modified.

Each git branch is also given a color indicating its health: green for healthy (the branch was updated recently), yellow for somewhat stale (branch hasn't been updated lately, but it's unclear whether the branch is too old to be used), or red for stale (the branch hasn't been updated in a long time).

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
| Bad Branches Only | Show only branches that are identified as being stale. | N/A | -b, --bad-only | - |
| Delete Stale Branches | Remove branches that are marked as stale. __Note__: Be careful with this option, as it can remove branches from any remote, and once removed, these branches are not recoverable. | N/A | -D, --delete | - |
| Number of Healthy Days | Specify the number of days where a branch is considered "healthy" without any activity. After these number of days without activity, the branch will be marked as somewhat stale, and show up as yellow in the branch list. After 2*this number of days without activity, the branch will be marked as stale, and will be eligible for removal. | 14 | -d, --days | - |
| Ignore Specific Branches | Specify which branches should be ignored. Normally, all branches titled "HEAD" or "master" are ignored, as these are considered "special", and reporting/deletion should not happen on them. If this option is specified, only the branches listed are included in reporting and deletion. This should be a comma-separated list of branch names. | "HEAD, master" | -i, --ignore-branches | ignoredbranches |
| No Color     | Specify not to use ANSI colors when printing the branch health results. | N/A | -n, --nocolor | nocolor |
| Remote Name  | Specify the name of a remote repository on which to operate. | `None` (Operate on local repository only) | -r `<remote name>` | - |
| Repository Path | Specify the location of the repository on which to operate. | Current directory (works on any subdirectory within a git repository) | -R, --repo | - |
| Show All Remotes | Show branches from all remotes, including local repository. | False | --all-remotes | - |
| Trunk Branch Name | Specify the name of the 'trunk' branch, the main development line. | master | -t, --trunk | trunk |
| Verbose Output | Make `git-branchhealth` output as much information on the command line as possible. | N/A | -v | - |
