# key-value-database
In this project we will be creating a simple version of a distributed, fault-tolerant, Key-Value (KV) database (or store), with a few tweaks. 

## Prerequisites
• Make sure you have python3 (3.11.1 or greater) installed. 

• All libraries used are part of the python standard library.

The zip file contains all the source code, the input-output data files, this README.md file and a pdf report with more details about the implementation. 

# Instructions 
## Data Generation 

Run the following command to generate random data:

```bash
  $ python3 genData.py -k keyFile.txt -n 1000 -d 3 -l 4 -m 5
```
where, <br/>
-k: file (keyFile.txt) containing a list of key names and their data types that we can use for the data creation <br/>
-n: number of lines (i.e. separate data) that we would like to generate <br/>
-d: maximum level of nesting <br/>
-m: maximum number of keys inside each value <br/>
-l: maximum length of a string value whenever we need to generate a string <br/>
