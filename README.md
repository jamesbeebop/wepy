#wepy

wepy displays the weather in a terminal, and is inspired by https://github.com/schachmat/wego

I'm freshly started down the [10 year path](http://www.norvig.com/21-days.html) to being a
better programmer.  I'm in IT, but my job is more SysAdmin-y and I don't do a lot of coding
professionally.  
The idea for this program, as well as the excellent ASCII art, and other sundry goodies, all
come from the wego project mentioned above.  This seemed like a great way to learn a little more 
Python, and also what it's like to publish to the world on Github.  Turns out, the latter is 
a bit scary.  :)

##Features

* show forecast for 1 to 5 days
* nice ASCII art icons
* displayed info (metric or imperial units):
  * temperature
  * windspeed and direction
  * viewing distance
  * precipitation amount and probability
* ssl, so the NSA has a harder time learning where you live or plan to go
* config file for default location which can be overridden by command line

![Screenshots](http://jamesbeebop.github.io/wepy/wepy.gif)

##Dependencies

* Tested under Python 2.7 and 3.4
* [Python requests](https://pypi.python.org/pypi/requests/2.5.3) - Python
  HTTP for humans
* utf-8 terminal with 256 colors
* A worldweatheronline.com API key (see Setup below)

##Setup

1. If you don't have the necessary API key, you can [register
   here](https://developer.worldweatheronline.com/auth/register) with your github.com account. 
   Your github.com account needs a public email address, but
   you can choose a bogus one.
2. Copy your API key into the `conf.py` file, change the city to your preference, and 
   choose if you want to use metric or imperial units. Save the file in the same folder
   with `we.py`
3. Run `python we.py ` to display the weather based on your conf entries, or 
   override with command line arguments (run `python we.py --help` to see
   options)

##Todo

* Does continuous improvement count as a to do?  :)

##License

The MIT License (MIT)

Copyright (c) 2015 <jamesbeebop@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

##Original License from the wego project

Copyright (c) 2015,  <teichm@in.tum.de>

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.