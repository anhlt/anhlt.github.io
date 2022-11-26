## Flow of data in MySQL

I will try to explain how MySQL write data to Disk, recovery , 

This is first part of 3 parts article "Flow of data in MySQL"


### Buffer management 

- RAM and Disk, Pages

Many database are built using 2 types of memory to physically store data.


- RAM: Random access memory or main memory. RAM allows us to access and modify data randomly and fast, the downside of ram is this is volatile, the data in ram will be erased when the computer restart and the size of RAM is relatively smaller than Disk. 
- Disk: persistent storate. Disk allows us to store huge amount of data, and non-volatile. Sequence read/write speed in Disk is faster than random access.


_But how data are stored logically_? TLDR:  Table are stored in Files of Pages of Record.

Most of database split file in to same-sized pages, that ranges from 4KB to 16KB. Each page will be identify by **PageID**. 
In one page there are many records, and each record will has the **location** in the page. 
In order to access a particular record on Disk, we need to know the pair of **(PageID, location)**. 



- Buffer Management strategy
- Steal / No Force

### Log

- WAL
- Undo log MVCC
- 
