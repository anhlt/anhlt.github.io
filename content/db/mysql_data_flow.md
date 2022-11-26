## Flow of data in MySQL

I will try to explain how MySQL write data to Disk, recovery , 

This is first part of 3 parts article "Flow of data in MySQL"


### RAM and Disk, Pages

_How is data stored physically?_ TLDR: DBMS stored data in RAM and Disk

Many database are built using 2 types of memory to physically store data.

- RAM: Random access memory or main memory. RAM allows us to access and modify data randomly and fast, the downside of ram is this is volatile, the data in ram will be erased when the computer restart, and the size of RAM is relatively smaller than Disk. 
- Disk: persistent storate. Disk allows us to store huge amount of data, and non-volatile. Sequence read/write speed in Disk is faster than random access.


_How is data stored logically?_ TLDR:  Table are stored in Files of Pages of Record.

Most databases split files into same-sized pages, that range from 4KB to 16KB. Each page will be identified by _PageID_. In one page there are many records, and each record will have the _location_ in the page. To access a particular record on Disk, we need to know the _pointer_ as a pair of _(PageID, location)_.


### Buffer management strategy



- Steal / No Force


### Log

- WAL
- Undo log MVCC
- 
