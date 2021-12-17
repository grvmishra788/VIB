# VIB - Visualizing and Interpreting Bias 

### Requirements
Python 3.6+, pip

The web interface is supported only for Chrome and Firefox.

The following libraries are also required to run the code:
```
flask
sklearn
scipy
numpy
tqdm
gensim
```

To install these libraries using pip, use the following command in the terminal:
```
pip3 install flask scikit-learn scipy numpy pandas tqdm gensim
```

To install these packages only for current user (or if you do not write access to the python installation on the machine):
```
pip3 install flask scikit-learn scipy numpy pandas tqdm gensim --user
```

Alternately, you can also use conda to install the packages:
```
conda install flask scikit-learn scipy numpy pandas tqdm gensim
```

### Dataset
You need to download the dataset from [https://drive.google.com/drive/folders/1ni_1yWWC4n6c6dTvauOPhV8aPbHRMLlK](https://drive.google.com/drive/folders/1ni_1yWWC4n6c6dTvauOPhV8aPbHRMLlK) and replace the contents of the dummy `data` folder present here from the contents of `data` folder present in the above google drive link.

### Installation
Clone this repository to your local machine, make sure the requirements are installed on your machine. Then update the contents of the `data` folder 
Then navigate to the cloned repository and in the base directory, type the following
command in the terminal.
```shell script
git clone https://github.com/grvmishra788/VIB.git
# Update contents o `data` folder
cd VIB
python3 -m flask run
```

Once the command above is running, open your web browser (Chrome and Firefox supported) and navigate to: 
http://127.0.0.1:5000/ (or equivalently to: http://localhost:5000)


### Common installation issues and fixes

#### Error: Could  not locate a Flask application on command `python -m flask run`
If you get the following error, it might indicate that you are not in the correct directory. Open a terminal in the 
base directory of the cloned repository.
```
Error: Could not locate a Flask application. You did not provide the
"FLASK_APP" environment variable, and a "wsgi.py" or "app.py" module
was not found in the current directory
```

#### Python version
The tool is written with Python 3.6+ support, and may/may not work with earlier versions of Python3.x. 
Python 2.x. is not supported.

#### Missing libraries
Make sure you install the requirements before running the application. 

#### Application runs but UI is mangled in the browser
We have tested the tool on Firefox and Chrome. There are known issues of point labels not showing correctly in Safari.

#### I get the following error: "Something went wrong! Could not find the key 'xxxx'
This error means that one of the words (denoted by 'xxxx' above) in your provided word set was not found the 
vocabulary of the word vector embedding. Check the spelling, or use another common word instead. 
