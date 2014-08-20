gitbranchhealth
===============

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
