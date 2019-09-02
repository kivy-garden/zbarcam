Generating the Docs
===================

Basic instructions for how to generate the flower docs and upload to github.
This needs to be done in either powershell or linux shell, not windows cmd.

The generated docs can be found at https://kivy-garden.github.io/flower/ after this
process.

Please use these instructions with care and don't copy paste without understanding
what the commands do as they create and delete folders. Make sure the repo is
fully pushed to github before doing this because this **deletes** all local changes.

You may want to do the following commands in a copy of the flower directory.

Install sphinx::

    python -m pip install sphinx

In a shell make sure to be in the flower directory. Then::

    cd doc
    # (in powershell do ./make.bat html)
    make html
    cd ..
    
    mkdir ~/docs_temp
    # copy generated docs to temp path
    cp -r doc/build/html/* ~/docs_temp
    # gh-pages is the branch for the docs that github will display
    git checkout --orphan gh-pages
    # **CAUTION** be sure the following commands is executed in the flower directory
    # we take no responsibility if you delete all the files in your computer :)
    git rm -rf .
    # on a linux shell do
    rm -fr $(ls -1 --ignore=.git .)
    # in powershell instead do
    Remove-Item -recurse * -exclude .git
    # copy the docs back to the repo
    cp -r ~/docs_temp/* .
    echo "" > .nojekyll

    git add .
    git commit -a -m "Docs update"
    git push origin gh-pages -f

    # Finally, get back to master
    git checkout master