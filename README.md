Packaging Mu for macOS: Experiments
===================================

Requisites
----------

* XCode command line tools installed.
* XCode not installed.
* `brew`'s OpenSSL 1.1 installed.


Building CPython 3.7.5
----------------------

* Clone of https://github.com/python/cpython.
* Checkout the `v3.7.5` tag.
* Configure with:

```
$ ./configure CPPFLAGS="-I$(brew --prefix openssl)/include" LDFLAGS="-L$(brew --prefix openssl)/lib" --prefix=$HOME/Temp/python-3.7.5 --enable-shared --enable-optimizations
```

* Build and install with:

```
$ make && make altinstall
```


Installing Mu and making it all work
------------------------------------

* Change working directory into the target installation directory (`$HOME/Temp/python-3.7.5`, above).
* Run `00_relink_cpython.py` to make the CPython installation relocatable.
* Run `01_install_mu.sh` to install `Mu` from source.
* Run `02_make_mu_relocatable.py` to make the `mu-editor` command relocatable.
* Run `03_trim_down.sh` to trim down the whole distribution (somewhat aggressive!).


Result
------

* The `$HOME/Temp/python-3.7.5` directory holds a fully relocatable Mu installation.
* Seems to work fine when transferred to a freshly installed macOS Mojave system (with no `brew`, now Python, no nothing!).

Notes
-----

Many paths are are hard-coded to my working environment.

