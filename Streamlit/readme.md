## Windows Users:

1. Go to File -> Settings -> Tools -> Terminal.

2.Replace the value in Shell path with

```
powershell.exe -ExecutionPolicy ByPass -NoExit -Command "& conda activate <yourcondaenvname>
```
***
## Run code
1. Install the dependencies from requirements.txt
2. Run streamlit 
   * streamlit run <Filename.py>
   * python -m streamlit <Filename.py>

## Dependencies

These are the packages needed to run all the demos. These specific versions are known to work, but this does not mean 
older or newer versions will cause any issues.

- streamlit 1.28.0
- pandas 2.1.1
- numpy 1.26.1
- matplotlib 3.8.0
- plotly 5.17.0
- altair 5.1.2
- vega_datasets 0.9.0
- scipy 1.11.3
