---
Title: Flow of data in MySQL
Slug: null
Date: {}
Modified: {}
Tags: 'Transaction_Level, Database'
Category: TIL
Author: h4cker
Lang: vi
Status: null
Summary: Data flow in Mysql
Series: Transaction in Database
published: true
---
## Flow of data in MySQL

I will try to explain how MySQL write data to Disk, recovery , 

This is first part of 3 parts article "Flow of data in MySQL"

### ACID properties

**Atomicity:** All actions in transaction happens or none happen at all
**Consistency** 

**Isolation**

**Durability**


### RAM and Disk, Pages

_How is data stored physically?_ TLDR: DBMS stored data in RAM and Disk

Many database are built using 2 types of memory to physically store data.

- RAM: Random access memory or main memory. RAM allows us to access and modify data randomly and fast, the downside of ram is this is volatile, the data in ram will be erased when the computer restart, and the size of RAM is relatively smaller than Disk. 
- Disk: persistent storate. Disk allows us to store huge amount of data, and non-volatile. Sequence read/write speed in Disk is faster than random access.


_How is data stored logically?_ TLDR:  Table are stored in Files of Pages of Record.

Most databases split files into same-sized pages, that range from 4KB to 16KB. Each page will be identified by _PageID_. In one page there are many records, and each record will have the _location_ in the page. To access a particular record on Disk, we need to know the _pointer_ as a pair of _(PageID, location)_.


### Buffer management 

Because we cannot modify data directly on disk, we need to load data from Disk to Ram, modify, then write back to disk to persist data. The perpose of buffer management is providing the illusion that we are operating in memory. Buffer manage map the pages in memory to pages in disk.

The size of RAM is much smaller than Disk, so we need the strategy for loading pages into RAM, and flushing pages in to Disk. 

_Steal_ Suppose an transaction _Trx1_ want to read data from page _P1_, but the memory is already full as other transaction load other pages to memory, So _Trx1_ needs to clear some memory, by flush other pages from memory to disk, remove that pages from memory, then load the needed pages from disk to memory. 

_Force_ means when the trx1 commit, all the affected pages in memory need to be flushed to disk. 

Let's think about No Steal Policy, We don't allow the pages with uncommited changes to be replaced. This is useful for archieving atomicity without UNDO logging. But also need to keep many pages in memory

If we make sure every update id forced onto disk before commit, we are provided durability, but it also cause poor performance by lot of random IO to commit

Our prefer strategy is  Steal / No-Force

_No Force_ : We don't need to flush modified pages to disk before commit. In stead we will using 2 other data struct to store the changes. _Redo log buffer_ in ram and _Redo Log_ in Disk. Before we update any record in pages on buffer pool, we appending a new log entry of _Redo log buffer_ , and before we commit we will persist the log entries in _Redo log buffer_ to _Redo log_. Instead of randomy flush the pages to disk, we now write the Redo log sequentially to disk.

_Steal_ : By allowing to replace dirty pages, there is some risk. If the transaction is abort, how can we restore to previous value? What if the system crash before the transaction finished? We need undo log

### REDO log (WAL log)

Basic idea, for every operation on buffer pages, we will record that operation to WAL log.
Log record, there is 4 kind of log record in Redo log

- _[START T]_ transaction T has begun
- _[COMMIT T]_ transaction T has commited
- _[ABORT T]_ transaction T 
- _[T, X, V]_ transaction T has updated the element X with new value v
  
How do we recover ?

```
STEP    |1          |2          |3      |4          |5          |6      |7             | 8          | 9      | 10     |
ACTION  |           |READ(A,t)  |T=T*2  |WRITE(A,t) |READ(B, t) |T=T*2  | WRITE (B, t) | COMMIT T   | FLUSH A| FLUSH B|
MEM__A  |           |8          |       |16         |16         |16     |16            | 16         | 16     | 16     |
MEM__B  |           |           |       |           |8          |8      |16            | 16         | 16     | 16     |
DISK_A  |8          |8          |       |16         |16         |16     |16            | 16         | 16     | 16     |
DISK_B  |8          |8          |       |8          |8          |8      |16            | 16         | 16     | 16     |
REDO_L  |[START T]  |           |       |[T, A, 16] |           |       |[T, A, 16]    | [COMMIT T] |        |        |
  
```




Two important points of WAL log.

1. The data changes operation should be write to WAL log before write to Disk
2. Must **force** all log record for a transaction before commit



![InnoDB]({{site.baseurl}}/content/db/innodb.png)


  



### Log


- Undo log MVCC
-
