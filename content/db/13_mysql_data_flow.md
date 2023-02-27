---
Title: Flow of data in MySQL
Slug: mysql-data-flow
Date: 2023-02-27 12:17:14
Modified: 2023-02-27 12:17:14
Tags:  Transaction_Level, Database
Category: TIL
Author: h4cker
Lang: vi
Status: 
Summary: Introduce to Isolation Level
Series: Transaction in Database
---

# Flow of data in MySQL

I will try to explain how MySQL write data to Disk, recovery, WAL log, 
MVCC.  Multiple Version CC



# RAM and Disk, Pages

_How is data stored physically?_ TLDR: DBMS stored data in RAM and Disk

Many database are built using 2 types of memory to physically store data.

- RAM: Random access memory or main memory. RAM allows us to access and modify data randomly and fast, the downside of ram is this is volatile, the data in ram will be erased when the computer restart, and the size of RAM is relatively smaller than Disk. 
- Disk: persistent storage. Disk allows us to store huge amount of data, and non-volatile. Sequence read/write speed in Disk is faster than random access on Disk.


_How is data stored logically?_ TLDR:  Table are stored in Files of Pages of Record.

Most databases split files into same-sized pages, that range from 4KB to 16KB. Each page will be identified by _PageID_. In one page, there are many records, and each record will have the _location_ in the page. To access a particular record on Disk, we need to know the _pointer_ as a pair of _(PageID, location)_.

![Page_buffer_disk.png]({{site.baseurl}}/content/db/Page_buffer_disk.png)


# Buffer management 

Because we cannot modify data directly on disk, we need to load data from Disk to RAM, modify, then write back to disk to persist data. The perpose of buffer management is providing the illusion that we are operating in memory. Buffer manage map the pages in memory to pages in disk.

The size of RAM is much smaller than Disk, so we need the strategy for loading pages into RAM, and flushing pages in to Disk. There are 2 properties that we need to think about in buffer management.

**_Steal_** Suppose an transaction _Trx1_ want to read data from page _P1_, but the memory is already full as other transactions load other pages to memory, So _Trx1_ needs to clear some memory, by flush other pages from memory to disk, remove that pages from memory, then load the needed pages from disk to memory. 

**_Force_** means when the trx1 commit, all the affected pages in memory need to be flushed to disk. 



Let's think about  **No Steal Policy** , We don't allow the pages with uncommited changes to be replaced. This is useful for archieving atomicity without UNDO logging. But also need to keep many pages in memory

![Steal.png]({{site.baseurl}}/content/db/Steal.png)



If we make sure every update are forced onto disk before commit, we are provided durability, but it also cause poor performance by lot of random IO to commit

**Our prefer strategy is  Steal / No-Force**

_No Force_ : We don't need to flush modified pages to disk before commit. We will use 2 other data structs to store the changes. _Redo log buffer_ in ram and _Redo Log_ in Disk. Before we update any record in pages on buffer pool, we appending a new log entry of _Redo log buffer_ , and before we commit we will persist the log entries in _Redo log buffer_ to _Redo log_. Instead of randomy flush the pages to disk, we now write the Redo log sequentially to disk.


_Steal_ : By allowing to replace dirty pages, there is some risk. If the transaction is abort, how can we restore to previous value? What if the system crash before the transaction finished? We need undo log

# REDO log (WAL log)

Basic idea, for every operation on buffer pages, we will record that operation to WAL log.
Log record, there is 4 kind of log record in Redo log

- _[START T]_ transaction T has begun
- _[COMMIT T]_ transaction T has commited
- _[ABORT T]_ transaction T 
- _[T, X, V]_ transaction T has updated the element X with new value v

```
BEGIN

SELECT value FROM table where ID  = A

UPDATE table SET value = 16 where ID = A

SELECT value FROM table where ID  = B


UPDATE table SET value = 16 where ID = B

COMMIT



```
  

```
STEP    |1          |2          |3      |4          |5          |6      |7             | 8          | 9      | 10     |
ACTION  |           |READ(A,t)  |T=T*2  |WRITE(A,t) |READ(B, t) |T=T*2  | WRITE (B, t) | COMMIT T   | FLUSH A| FLUSH B|
MEM__A  |           |8          |       |16         |16         |16     |16            | 16         | 16     | 16     |
MEM__B  |           |           |       |           |8          |8      |16            | 16         | 16     | 16     |
DISK_A  |8          |8          |       |8          |8          |8      |8             | 8          | 16     | 16     |
DISK_B  |8          |8          |       |8          |8          |8      |8             | 8          | 8      | 16     |
REDO_L  |[START T]  |           |       |[T, A, 16] |           |       |[T, A, 16]    | [COMMIT T] |        |        |
  
```


Two important points of WAL log.

1. The operations should be write to WAL log buffer before write to pages

	In the 4th step, we need to write the redo log **[T, A, 16]** before update the value of A in memory
    
    In the 7th step, we need to write the redo log **[T, B, 16]** before update the value of B in memory

2. Must **force** all log record for a transaction before commit
    
    In the 8th step, we need to flush all the previous log entries and the **[COMMIT T]** to WAL log in Disk before return success response.


If the system crashed after we wrote the [COMMIT T] to disk. In the WAL log on disk we have

```
[START T], [T, A, 16] ,[T, A, 16] , [COMMIT T]
```
So we can redo the the log.

If the system crashed before we wrote the [COMMIT T] to disk. We should ignore the transaction T. 

```
[START T], [T, A, 16] ,[T, A, 16]
```


# The flow of data

A log sequence number (LSN) represents the offset, in bytes, of a log record from the beginning of a database log file

FlushedLSN represent the last LSN that have been flushed to Disk

PageLSN represent the LSN of last log entry, which updated this page


![data_flow_dbms.png]({{site.baseurl}}/content/db/data_flow.png)

As we see in the step 4. If the pageLSN in buffer-pool is larger than flushedLSN, we not allow to force the page to disk, because we will lose information in LSN in case of system crash. 
If the pageLSN smaller than flushedLSN, we are allow to replace the pages with other pages.



# Recovery.

![Recovery.png]({{site.baseurl}}/content/db/Recovery.png)



# UNDO Log

As you can see that when we update the the value of any record, we update directly to the pages on buffer pool. How can we revert the value when abort the transaction? To do that, we need to save the old value in some place called UNDO log. By using undo log, we can also provide MVCC for transaction.


## Mysql data layout

![B_tree.png From O'Reilly.High.Performance.MySQL.3rd.Edition]({{site.baseurl}}/content/db/B_tree.png)

In InnoDB the clustered index is actually the table. The leaf node in the clustered index contains 

- the PK value
- the transaction ID
- the rollback pointer for transactional and MVCC
- the rest of the columns.


## UNDO Log Entry.

There are 2 types of entry in UNDO Log.

**Insert entry**, for new record, we don't have previous value, but we still need to insert the Inserting entry to UNDO log before update the record value in buffer pool. Insert entry contains


**Update entry**, before we update any record in buffer page, we need to add new update entry with current value of the record to the UNDO log , and then update the value on buffer pool.

- the PK value
- the transaction ID
- the rollback pointer, which points to previous version of the record
- the rest of the columns.

We could think the UNDO log for every record is a **linked-list** with head is latest value, and the tail is the **Insert Entry**




## Undo Log Entry

- Every transaction will have one undo log entry. The Undo log header contains the transaction ID that start this UNDO log, The update 



![UNDO.png]({{site.baseurl}}/content/db/UNDO.png)







# Overall architecture of MySQL

![innodb.png]({{site.baseurl}}/content/db/innodb.png)


https://excalidraw.com/#json=gk8L0m-mg9viqWyc_0MTl,F44tZbzcuRKQaTzrP4avJg

