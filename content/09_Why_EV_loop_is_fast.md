---
Title: Nodejs eventloop hoạt động như thế nào, Libuv, epoll
Slug: 
Date: 2020-12-28 12:17:14
Modified: 2020-12-28 12:17:14
Tags:  eventloop, epoll, socket, javascript, libuv
Category: Programing
Author: h4cker
Lang: vi
Summary: Libuv , epoll hoạt động như thế nào
---

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


Libuv là gì, nó là thư viện để xử lý các vấn đề liên quan đến bất đồng bộ, như 

```
    libuv is a multi-platform support library with a focus on asynchronous I/O. 
    It was primarily developed for use by Node.js, but it's also used by Luvit, Julia, pyuv, and others.
```

{% img images/09/nodejs_system.png 1000 'DETR' %}


### Blocking Socket Server

{% include_code 09/blocking_socket.py lang:python %}

Nói đến lập trình socketsocket thì ví dụ trên là một chương trình socket điển hình. 
- Khởi tạo một socket server, lắng nghe ở port `654321`. 
- Tạo một vòng lặp vô tận, chờ một kết nối đến
    - nhận dữ liệu từ client cho đến khi có kí tự `EOL` trong nội dung.
    - Đóng kết nối và gửi lại client nội dung `Hello world`
    - Tiếp tục một vòng lặp mới

Nhưng vấn đề ở chương trình này là gì, đó là nó bị `blocking` ở câu lệnh sau 

```python
        conn, address = server.accept()
```

Tại dòng lệnh này thì trình dịch python sẽ dừng chương trình lại, không xử lý gì cả, chờ đợt cho đến khi có một connection mới. Thuật ngữ thường được gọi là `blocking IO`. Dẫn đến chương trình này chỉ làm việc được với tối đa 1 client trong 1 thời điểm, những client sau đó phải chờ cho đến khi client trước đó hoàn thành phiên làm việc mới được xử lý.

Các bạn có thể xem demo chường trình này dưới đây, tôi cùng một lúc khởi tạo 2 client với id là `1` và `2` đến socket server. Mỗi client hoạt động theo logic như sau:
- Khởi tạo kết nối đến server
- Sau một khoảng thời gian nhất định, gửi 1 xâu có giá trị `hello from {client_id}` đến server
- Sau 10 lần gửi thông điệp client sẽ gửi `EOL` đến server


Các bạn có thể thấy, server xử lý tuần tự 1 client trong 1 thời điểm, sau khi hoàn thành xử lý với `client 1`, thì server mới tiếp tục làm việc với `client 2` 



[![asciicast](https://asciinema.org/a/OMX7Buub9ksUi9k7eLiUSK6g8.svg)](https://asciinema.org/a/OMX7Buub9ksUi9k7eLiUSK6g8)


{% include_code 09/client.py lang:python :hidefilename: client.py  %}



Để giải quyết bài toán này thì mọi người thường nghĩ đến một giải pháp là `multithread`, đây cũng là giải pháp thường được các thầy giáo hướng dẫn ở trong trường đại học. Mỗi khi có một kết nối đến server thì chương trình sẽ khởi tạo 1 thread mới, xử lý data được gửi đến từ client và trả lại dữ liệu cho client.

Nhược điểm của phương pháp này nó là, mỗi thread sẽ có `call stack` riêng, và việc chuyển đổi giữa các `call stack` cũng ảnh hưởng tới hiệu năng của chương trình. Một cách khác để giải quyết vấn đề này đó chính là `non-blocking IO`, nói một cách khác, chúng ta sẽ không bắt chương trình chờ cho đến khi có data nữa.


### Non-Blocking Socket Server

{% include_code 09/non_blocking_socket.py lang:python %}


[![asciicast](https://asciinema.org/a/DQcgHeBbIcy7AXU1lP5VKeMqr.svg)](https://asciinema.org/a/DQcgHeBbIcy7AXU1lP5VKeMqr)


