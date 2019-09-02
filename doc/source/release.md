# How to release

This is documenting the release process.


## Git flow & CHANGELOG.md

Make sure the CHANGELOG.md is up to date and follows the http://keepachangelog.com guidelines.
Start the release with git flow:
```sh
git flow release start YYYYMMDD
```
Now update the [CHANGELOG.md](/CHANGELOG.md) `[Unreleased]` section to match the new release version.
Also update the `version` string from the
[src/kivy_garden/zbarcam/version.py](https://github.com/kivy-garden/zbarcam/blob/develop/src/kivy_garden/zbarcam/version.py)
file.
Then commit and finish release.
```sh
git commit -a -m "YYYYMMDD"
git flow release finish
```
Push everything, make sure tags are also pushed:
```sh
git push
git push origin master:master
git push --tags
```

## Publish to PyPI

Build it:
```sh
python setup.py sdist bdist_wheel
```
Check archive content:
```sh
tar -tvf dist/kivy_garden.zbarcam-*.tar.gz
```
Twine check and upload:
```sh
twine check dist/*
twine upload dist/*
```
Also publish the alias meta package `setup_meta.py`.

## Check Read the Docs

Make sure <https://readthedocs.org/projects/zbarcam/> is up to date.

## GitHub

Got to GitHub [Release/Tags](https://github.com/kivy-garden/zbarcam/tags), click "Add release notes" for the tag just created.
Add the tag name in the "Release title" field and the relevant CHANGELOG.md section in the "Describe this release" textarea field.
Finally, attach the generated APK release file and click "Publish release".
