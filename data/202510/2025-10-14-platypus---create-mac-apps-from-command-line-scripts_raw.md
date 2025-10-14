Title: Platypus - Create Mac apps from command line scripts  |

URL Source: https://sveinbjorn.org/platypus

Published Time: Thu, 25 Sep 2025 11:28:16 GMT

Markdown Content:
![Image 1: Platypus icon](https://sveinbjorn.org/images/platypus.png)

**Platypus** is a developer tool that creates native Mac applications from command line scripts such as shell scripts or Python, Perl, Ruby, Tcl, JavaScript and PHP programs. This is done by wrapping the script in a macOS [application bundle](http://en.wikipedia.org/wiki/Application_bundle) along with an app binary that runs the script.

Platypus makes it easy to share scripts and command line programs with people who are unfamiliar with the shell interface. Native, user-friendly applications can be created with a few clicks. It is very easy to create installers, droplets, administrative applications, login items, status menu items, launchers and automations using Platypus.

Features
--------

*   Supports shell scripts, Python, Perl, Ruby, PHP, Swift, Expect, Tcl, AWK, JavaScript, Dart, AppleScript or any other user-specified interpreter
*   Apps can display graphical feedback of script execution as progress bar, text window with script output, droplet, WebKit HTML rendering or status item menu
*   Apps support receiving dragged and dropped files or text snippets, which are then passed to the script as arguments
*   Apps can execute scripts with root privileges via the macOS Security Framework
*   Apps can register as handlers for URI schemes and send user notifications
*   Apps can be configured to run in the background (LSUIElement)
*   Set own application icon or select from presets
*   Set app's associated file types, identifier, version, author, etc.
*   Graphical interface for bundling support files with the script
*   Command line tool for automation and build process integration
*   "Profiles" can be used to save app configurations
*   Built-in script editor, or linking with external editor of choice
*   Extensive [documentation](https://sveinbjorn.org/platypus_documentation) and many built-in examples to help you get started
*   Fast, responsive native app written in Objective-C/Cocoa

License
-------

Platypus is free, open source software distributed under the terms of the [three-clause BSD license](https://sveinbjorn.org/bsd_license) and has been continually maintained and developed for a very long time (since 2003). The source code is available on [GitHub](https://github.com/sveinbjornt/Platypus).

**If Platypus makes your life easier, please [make a donation to support continued development.](https://sveinbjorn.org/donations)**

Download
--------

The latest version is **Platypus 5.4.1**, released on October 22nd, 2022. Platypus and Platypus-generated applications require **macOS 10.11** or later, and are **Universal 64-bit Intel/ARM** binaries. The main Platypus application and command line tool are Apple Developer ID signed.

Platypus can also be installed via [Homebrew](https://brew.sh/) (may not be latest version):

$ brew install --cask platypus

Legacy support
--------------

If you want to target macOS 10.8-10.10, use [version 5.3](https://sveinbjorn.org/files/software/platypus/platypus5.3.zip). If you want to target 10.6 and/or 32-bit Intel systems, [version 4.9](https://sveinbjorn.org/files/software/platypus/platypus4.9.zip) continues to work just fine.

Links
-----

*   [Documentation](https://sveinbjorn.org/platypus_documentation)
*   [GitHub Repository](https://github.com/sveinbjornt/Platypus)
*   [man page](https://sveinbjorn.org/files/manpages/platypus.man.html)
*   [Appcast XML](https://sveinbjorn.org/files/appcasts/PlatypusAppcast.xml)
*   [Old Versions](https://sveinbjorn.org/files/software/platypus/)

Screenshots
-----------

![Image 2: Platypus Window](https://sveinbjorn.org/images/basic_interface.png)

Platypus lets you select one of several different user interfaces for your script.

#### Progress Bar

![Image 3: Progress Bar interface](https://sveinbjorn.org/images/interface_progressbar.png)

#### Text Window

![Image 4: Text Window interface](https://sveinbjorn.org/images/interface_textwindow.png)

#### Web View

![Image 5: Web View interface](https://sveinbjorn.org/images/interface_webview.png)

#### Status Menu

![Image 6: Status Menu interface](https://sveinbjorn.org/images/interface_statusmenu.png)

#### Droplet

![Image 7: Droplet interface](https://sveinbjorn.org/images/interface_droplet.png)
