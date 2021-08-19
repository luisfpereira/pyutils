
`pyutils` contains small CLI tools I use to boost my productivy and/or perform boring tasks. It also contains recurrent no-brainers. Below a summary of a selection of the available tools and how to use them (you can always explore them by yourself in `pyutils.cli`).


Note: this repo is unstable. If you start using any of these tools and after a while you find out they've changed, remember that it's possible to install a selected commit (you will, of course, lose future updates). If this happens in a way that interferes with your workflow, please let me know.


## Installation

Install with

```bash
pip install git+https://github.com/lpereira95/pyutils.git@master
```


If you also want to install requirements, do

```bash
pip install git+https://github.com/lpereira95/pyutils.git@master#egg=pyutils
```


If you want to install any of the extra requirements (e.g. `integratedtests`), do

```bash
pip install git+https://github.com/lpereira95/pyutils.git@master#egg=pyutils[integratedtests]
```

Note: in `zsh` shell you have to escape `[` and `]`.

Check out `setup.cfg` to get a list of available extra requirements options.


## CLI tools

Note: only basic usage is explained below. You can get more information by doing `<method_name> --help>`.


### Integrated tests

**Includes**: `make-integrated-tests`

**Extra requirements (see `setup.cfg`)**: `integratedtests`.

**Motivation**: a common practice in Python projects is to split large libraries into several smaller ones. This modularity clearly simplifies development, as each of the packages deals with very specific problems. Nevertheless, it creates a set of intricate dependencies. `make-integrated-tests` looks to simultaneously test several packages (locally), allowing to choose which branches to use for each dependency.


**How to use it?**

```bash
make-integrated-tests <project-name>
```

It looks for a `json` configuration file in `~/.pyutils` named `integrated_tests.json`. The configuration file contains, for each project, a set of repos, for which a list containing the branch name and a boolean (which specificies if the library is to be tested or the repo should only be checked out) should be defined. e.g.

```json
# ~/.pyutils.integrated_tests.json (do not add this to your file as json does not allow comments)
{
    "kokiy":
    {
        "kokiy": ["master", false],
        "pyavbp": ["master", false],
        "oms": ["FEATURE/kokiy", true],
        "arnica": ["CLEAN/kokiy", false]
    }
}
```

It searches for repos in `~/Repos`, but you can control the path by passing `--search-dirname`.

It assumes each repo can be tested by `make test` or `pytest`.



### Repos management

**Includes**: `print-repos-active-branch`, `print-repo-branches`, `print-repos-branches`, `print-repos-dirty`, `checkout-repo`, `checkout-repos`, `pull-repo`, `pull-repos`

**Extra requirements (see `setup.cfg`)**: `git`

**Motivation**: fast way to have local repos updated. Starts to be relevant when you want to keep track of dozens of repos.


**How to use it?**

Most of the CLI tools are straightforward and self-explanatory. By default, it searches for repos in `~/Repos`, but `--search-dirname` overrides behavior.

`checkout-repos` and `pull-repos`, by default, look for repos in a `txt` configuration file in `~/pyutils` named `git_repos.txt`. e.g.

```
# ~/.pyutils.git_repos.txt
# repo, branch (if applicable), force checkout (if applicable) 
kokiy, master, False
pyavbp
arnica, CLEAN/kokiy
oms
```

Note: be careful with forcing checkout, as local changes are dismissed.



### [codecogs](https://latex.codecogs.com/)

**Includes**: `codecog-eq`

**Extra requirements (see `setup.cfg`)**: `git`

**Motivation**: add equations in `markdown`-based blog posts. Very powerful in combination with [mathpix](https://mathpix.com/).

**How does it work?** Add an equation to your clipboard and then do `codecog-eq`: your clipboard wil be updated with the url for rendering the equation via codecogs.











