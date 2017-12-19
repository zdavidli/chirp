# 2017-group-18

Group Members:

* Yu-chi Chang (kikichang)
* Gary Qian (garyqian)
* Ryan Newell (rnewell4)
* David Li (zdavidli)
* Richard Chen (richarizardd)


# Building the project:

Note: Since the project is primarily in python and Flask, it does not need to be built!

**Note:** Minimum recommended server requirements: GTX 1060 or above with >8gb RAM

We recommend Python 3.6 and Anaconda due to Tensorflow requirements. To use the GPU features, you must also install the CUDA libraries that Tensorflow requries.

To install requirements

```
pip install -r requirements.txt
```

Install ffmpeg:

Windows 64 bit:

Open an administrator Command Prompt:

```
setx /M PATH "C:\path\to\git\repo\lib\ffmpegwin64\bin;%PATH%"
```

Be sure to replace the path with the correct path to the lib/ffmpegwin64 directory.

Ubuntu:

```
sudo add-apt-repository ppa:mc3man/trusty-media  
sudo apt-get update  
sudo apt-get install ffmpeg  
sudo apt-get install frei0r-plugins  
```

MacOS

Here are a couple of links to instructions:

http://www.renevolution.com/ffmpeg/2013/03/16/how-to-install-ffmpeg-on-mac-os-x.html
http://www.idiotinside.com/2016/05/01/ffmpeg-mac-os-x/
http://macappstore.org/ffmpeg/

Restart your shell/command prompt/ssh after your install ffmpeg

To run:

```
cd src
python app.py
```

You will now be able to access the app at localhost:5000

You may also run on a different port with:

```
cd src
python app.py -p <port>
```

Note: On unix devices, use sudo to run on ports below 1024.

# Testing

To run all tests...

On Unix systems, run

```shell
$ ./test.sh
```

On Windows systems, run

```shell
test.bat
```
