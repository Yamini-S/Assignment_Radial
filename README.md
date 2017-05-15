# Assignment_Radial


Language: Python3.5

The assignment takes data.csv as source file. 
Two Output files are generated as patienClaims.csv(Question1) and claimUtilization.csv(Question2) in the same folder where script is located.

Below command is used to create binary for python script using pyinstaller to avoid installing python and other libraries.
```
pyinstaller --specpath build --onefile -n Assignment_RadialAnalytics Assignment_RadialAnalytics.py
```

To run binary file,
1. Clone the repo
2. Place the source file(data.csv) in the same folder where binary file is cloned
3. From command line navigate to your cloned directory, and run the below command

```
./Assignment_RadialAnalytics
```

Note: The binary uploaded in the repo runs for linux system.
