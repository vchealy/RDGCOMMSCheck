#### RDG Comms From Device  

>The use of this code is to determine which devices have communicated with the server. With a list of devices in a separate file they are used with a webscraper, as there is no API for the server.   

The server holds a log for the different types of communication that the device could make to the server.
These are known as message types and a specific one is targeted in this code as the best metric.

The message type can either come from the server or the device so the device serial number is added as the message originator.
With a from / to date, using the from date to determine if the device has not spoken for a number of days/weeks/months.

If there are no messages from the device this is logged and a file is created to give a report of devices that have not communicated.

**requirements.txt**  
The dependencies for running this tool  

**variables.py**  
Select the TOCs from this file  

**auth.py**  
This has changed a little removing item in previous versions of the code

**setup.py**  
Holds the domain construction information  
Environment choice function  
    Note: this also reads in the files. If the file names change then the code will need to be altered here  
Message Class Choice function  
Date/Time management function  
  
**art.py**  
The log  and code to give a clean console look  
  
I am still not completely happy with the initial console screen, but it ticks over looking better  
  
VCHealy  