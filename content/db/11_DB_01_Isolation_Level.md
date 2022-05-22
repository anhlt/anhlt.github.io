---
Title: [Short] Abnomaly in DB 
Slug: 
Date: 2022-05-21 12:17:14
Modified: 2022-05-21 12:17:14
Tags:  Transaction_Level, Database
Category: Interview
Author: h4cker
Lang: vi
Status: 
Summary: Giải thích về Isolation Level
Series: Database
---

Khi sủ dụng một hệ quản trị cơ sở dữ liệu, thì một điều cần đáng phải quan tâm đó chính là xử lý song song các transaction. Khi bạn chỉ có một 

[TOC]

# Abnomalies

## Dirty Read 

This is situation when a transaction could read uncommited changes from other transactions.

```
┌──────────────────────┬──────────────────────┐
│                      │                      │
│         T1           │         T2           │
├──────────────────────┼──────────────────────┤
│       BEGIN          │                      │
│                      │                      │
├──────────────────────┼──────────────────────┤
│                      │       BEGIN          │
│                      │                      │
├──────────────────────┼──────────────────────┤
│                      │                      │
│                      │       W(A)           │ A = 20
├──────────────────────┼──────────────────────┤
│                      │                      │
│       R(A)           │                      │ A = 20
├──────────────────────┼──────────────────────┤
│                      │                      │
│                      │       ABORT          │
├──────────────────────┼──────────────────────┤
│                      │                      │
│       COMMIT         │                      │
└──────────────────────┴──────────────────────┘
```



## Unrepeatable Reads Anomaly
## Phantom Reads Anomaly

# Isolation Level

## Read Uncommitted
## Read Committed

## Cursor Stability
## Repeatable Reads

## Snapshot Isolation
## Serializable

