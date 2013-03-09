What is Brunobot?
=================
Brunobot is an Internet Relay Chat (IRC) bot. Dynamic. Awesome. Modular. Nice.
DAMN!

Installation
============
Install [pyric](http://github.com/veiset/pyric) IRC library
```bash
git clone http://github.com/veiset/pyric.git
cd pyric
git submodule init
git submodule update
python setup.py install
```

Clone and run Brunobot
```bash
git clone http://github.com/veiset/Brunobot.git
cd Brunobot/new
python3 main.py
```

Running tests
=============
(requires pyric and py.test)
```bash
py.test -v .
```
