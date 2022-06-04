---
Title: [Short] Isolation in Database 
Slug: 
Date: 2022-05-20 12:17:14
Modified: 2022-05-20 12:17:14
Tags:  Transaction_Level, Database
Category: TIL
Author: h4cker
Lang: vi
Status: 
Summary: Introduce to Isolation Level
Series: Transaction in Database
---
Tính tách biệt (Isolation) của transaction là tính chất mà mỗi transaction hoạt động hoàn toàn độc lập với nhau, không bị ảnh huởng bởi nhung transaction khác.
Để cải thiện tốc độ xử lý, khi xử lý nhiều transaction, hệ quản trị cơ sở dữ liệu cần phải lập lịch để thực thi câu lệnh giữa các transaction một cách xen kẽ với nhau.


[TOC]
# Một số khái niệm
## Serial Schedule (Lịch thực thi tuần tự)

Một lịch thực thi tuần tự là lịch thực thi mà các câu lệnh không chạy xen kẽ với nhau.

Ví dụ:
Chúng ta có 2 transaction như sau, cơ sở dữ liệu cần phải lập lịch để thực thi những câu lệnh trong mỗi transaction

```
T1
BEGIN
A = A - 100
B = B + 100
COMMIT
```

```
T2
BEGIN
A = A * 0.01
B = B * 0.01
COMMIT
```
Một lịch thực thi tuần tự sẽ sắp xếp cho T1 hoàn thành trước, sau đó thực thi T2, hoặc ngược lại.

Ví dụ

```
T1          T2
BEGIN
A = A - 100
B = B + 100
COMMIT
            BEGIN
            A = A * 0.01
            B = B * 0.01
            COMMIT
```

## 




