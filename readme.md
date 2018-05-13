# A simple parallel libffm converter

## Introduction

Please refer the origin codes to [here](https://github.com/guestwalk/kaggle-2014-criteo/tree/master/converters). 

Extract the core component to convert .csv file into .ffm file, prepared for `libffm` or `xlearn`.

## Usage

### convert 

Please look up to `run.py` and modify the source and destination path.

```python
    python run.py
```

## Time consumption evaluation

`./test.csv` contains 20 instances of 4 different categorical fields.
Tried to convert it into .ffm file in both parallel and serial way, and their time consumtion are as follow.

![pic](https://github.com/SongDark/libffm_converter/blob/master/time_test/res.png?raw=true)
