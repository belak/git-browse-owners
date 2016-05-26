# owner

Crappy sample web ui which will display how many lines a user 'owns' in each
file of a git repo.

## Config

The only setting currently is `REPO_PATH` which should be set to the full path
to your repo on disk. Note that `DEBUG` may also be useful if you're having
issues with flask being strange.

## To Run

* `PYTHONPATH=. OWNER_SETTINGS=config.py python -m owner`

## Notes

I was having some problems with pygit2 crashing, so I ran everything in a while
loop. If pygit2 is more stable for you, feel free to not do that.

Also, performance wise, this is most likely very bad since it essentially does a
blame on every file in the repo for the root. Getting the totals is hard because
git doesn't have a concept of a directory outside of the tree objects.

