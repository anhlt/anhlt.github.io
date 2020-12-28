Title: Nodejs, Redis eventloop hoạt động như thế nào, Libuv, epoll
Slug: 
Date: 2018-01-14 12:17:14
Modified: 2018-01-14 12:17:14
Tags:  eventloop, epoll, socket, javascript, libuv
Category: Programing
Author: h4cker
Lang: vi
Summary: Epoll


Một ngày cuối năm đẹp trời, tôi bị đứa bạn thân ai nấy lo lâu năm hỏi một câu, mày biết tại sao cái thằng Nodejs, Redis là Single-Thread nhưng mà sao nó vẫn chạy nhanh như thế không. Thú thật là mình không biết, vào đọc mấy cái medium thì cũng k hiểu gì. Thôi thì tự code một cái event-loop , cũng là để hiểu event-loop nó hoạt động như thế nào.


### Một số khái niệm

Nào cùng nhau tra cứu một số khái niệm, để hiểu được bài viết này, cảnh báo là nhiều chữ và nhiều code nên các bạn cứ thảnh thơi ra làm ấm trà, điếu thuốc rồi vào đọc cho nó thư thả.

#### File Descriptors / File Descriptor Table

Trong linux có một câu nói khá nổi tiếng `Everything is a file`, File ở đây có thể là.
    
+ File *(Đương nhiên rồi)*
+ Terminal I/O (stdin/stdout/stderr)
+ pipe
+ sockets
+ device

Khi một tiến trình được khởi chạy thì mặc định sẽ được truy cập đến 3 tài nguyên

+ stdin
+ stdout
+ stderr

Các tài nguyên này được lưu trong bảng gọi là **File Descriptor Table** (`FDTable`) với chỉ số (index) là File Descriptor(`FD`)

|FD    	|Pointer   	            |
|---	|---	                |
|   0   |   stdin pointer   	|
|   1   |   stdout pointer	    |
|   2   |   stderr pointer	    |

Nếu tiến trình này mở một file mới, thì file mới sẽ được add vào `FDTable`, Tương tự khi tiến trình này mở 1 connection, một pipe, tất cả các tài nguyên này, đều là file, và được lưu ở `FDTable`

|FD    	|Pointer   	            |
|---	|---	                |
|   0   |   stdin pointer   	|
|   1   |   stdout pointer	    |
|   2   |   stderr pointer	    |
|   3   |   file pointer	    |

#### Libuv / Eventloop

Nhắc đến **Event Loop** trong javascript thì chắc chẳng ai còn lạ gì nữa, nếu thấy lạ thì mời bạn xem video rất nổi tiếng sau đây:

{% youtube 8aGhZQkoFbQ %}


Libuv là gì, 

    libuv is a multi-platform support library with a focus on asynchronous I/O. 
    It was primarily developed for use by Node.js, but it's also used by Luvit, Julia, pyuv, and others.










### Nguyên lý 

#### R-CNN

#### Fast RCNN 

#### Faster RCNN

Tổng kết lại ta có bảng so sánh đơn giản về 3 thuật toán trên như sau Hello

