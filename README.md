# key-value-database
In this project we will be creating a simple version of a distributed, fault-tolerant, Key-Value (KV) database (or store), with a few tweaks. 

## Prerequisites
• Make sure you have python3 (3.11.1 or greater) installed. 

• All libraries used are part of the python standard library.

The zip file contains all the source code, the input-output data files, this README file and a pdf report with more details about the implementation. 

## Instructions 
### Data Generation ###

Run the following command to generate random data:

```bash
  $ python3 genData.py -k keyFile.txt -n 100 -d 3 -l 4 -m 5
```
where, <br/>
-k: file (keyFile.txt) containing a list of key names and their data types that can be used for the data creation <br/>
-n: number of lines (i.e. separate data) that we would like to generate <br/>
-d: maximum level of nesting <br/>
-m: maximum number of keys inside each value <br/>
-l: maximum length of a string value whenever we need to generate a string <br/>

### Key-Value (KV) Database ###

We will use the generated data to implement the Key-Value store.

**KV Server** <br/> 
First of all, we need to launch the servers using the following commands:
```bash
  $ python3 kvServer.py -a 127.0.0.1 -p 8000 
  $ python3 kvServer.py -a 127.0.0.1 -p 8001 
  $ python3 kvServer.py -a 127.0.0.1 -p 8002 
```
where,<br/>
-a: ip_address <br/>
-p: port <br/>

The above commands can run from different terminals in order to set up multiple servers simultaneously. 

**KV Client** <br/> 
After servers are launched, we can populate the database with the generated data. <br/>

To launch the client, use the following command:
```bash
  $ python3 kvClient.py -s serverFile.txt -i dataToIndex.txt -k 3
```
where,<br/>
-s: file (serverFile.txt) containing a list of server IPs and ports that will be listening for queries <br/>
-i: file (dataToIndex.txt) containing data that was output from the previous part of the project <br/>
-k: replication factor, i.e. how many different servers will have the same replicated data <br/>

When the indexing is finished, we can move ahead with performing queries. <br/> 
KV Broker accepts queries from the user, as shown in the examples below: <br/>

```bash
  $ GET key2
  $ DELETE key3
  $ QUERY key4.age
  $ COMPUTE 2-x WHERE x = QUERY key2.age
  $ COMPUTE 2^x WHERE x = QUERY key2.age
  $ COMPUTE 2*x+3 WHERE x = QUERY key2.age
  $ COMPUTE 2/(x+3*(y+z)) WHERE x = QUERY key2.age AND y = QUERY key2.age AND z = QUERY key2.age
  $ COMPUTE log(2*(x+3)) WHERE x = QUERY key2.age
  $ COMPUTE cos(x)-tan(2*y+3) WHERE x = key2.age AND y = QUERY key2.age
  $ EXIT
```
The supported query commands are : GET, DELETE, QUERY, COMPUTE (addition, subtraction, division, multiplication, power, trigonometric/logarithmic functions for up to 3 variables which are queries). </br> </br>
The "EXIT" command is used to exit the kvClient.
