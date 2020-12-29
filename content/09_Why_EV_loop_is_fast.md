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


## Một số khái niệm

Nào cùng nhau tra cứu một số khái niệm, để hiểu được bài viết này, cảnh báo là nhiều chữ và nhiều code nên các bạn cứ thảnh thơi ra làm ấm trà, điếu thuốc rồi vào đọc cho nó thư thả.

### File Descriptors / File Descriptor Table

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
|   1   |   stdin pointer   	|
|   2   |   stdout pointer	    |
|   3   |   stderr pointer	    |

Nếu tiến trình này mở một file mới, thì file mới sẽ được add vào `FDTable`, Tương tự khi tiến trình này mở 1 connection, một pipe, tất cả các tài nguyên này, đều là file, và được lưu ở `FDTable`

|FD    	|Pointer   	            |
|---	|---	                |
|   1   |   stdin pointer   	|
|   2   |   stdout pointer	    |
|   3   |   stderr pointer	    |
|   4   |   file pointer	    |

### Timer / Callback

Cùng nói qua một chút về `timer` và `callback` trong `javascipt`. Chúng ta cùng xem xét đoạn code sau

    :::javascipt

    setTimeout(function cb() {
        console.log("callback")
    }, 5000)


thì nodejs sẽ khởi tạo 1 `timer`, sau khi `timer`đó kết thúc, thì sẽ đẩy `callback` vào `task queue`


{% video  images/09/timer3.mp4 800 300 %}

### Libuv / Eventloop

Nhắc đến **Event Loop** trong javascript thì chắc chẳng ai còn lạ gì nữa, nếu thấy lạ thì mời bạn xem video rất nổi tiếng sau đây:

{% youtube 8aGhZQkoFbQ %}


Libuv là gì, nó là thư viện để xử lý các vấn đề liên quan đến bất đồng bộ, như 

```
    libuv is a multi-platform support library with a focus on asynchronous I/O. 
    It was primarily developed for use by Node.js, but it's also used by Luvit, Julia, pyuv, and others.
```

{% img images/09/nodejs_system.png 500 'Node JS System' %}


## Blocking Socket Server

{% include_code 09/blocking_socket.py lang:python %}

Nói đến lập trình socketsocket thì ví dụ trên là một chương trình socket điển hình. 
- Khởi tạo một socket server, lắng nghe ở port `654321`. 
- Tạo một vòng lặp vô tận, chờ một kết nối đến
    - nhận dữ liệu từ client cho đến khi có kí tự `EOL` trong nội dung.
    - Đóng kết nối và gửi lại client nội dung `Hello world`
    - Tiếp tục một vòng lặp mới

Nhưng vấn đề ở chương trình này là gì, đó là nó bị `blocking` ở câu lệnh sau 

    :::python
        conn, address = server.accept()


Tại dòng lệnh này thì trình dịch python sẽ dừng chương trình lại, không xử lý gì cả, chờ đợt cho đến khi có một connection mới. Thuật ngữ thường được gọi là `blocking IO`. Khi có dữ liệu mới từ client, chương trình tiếp tục xử lý và sau đó quay lại chu kì lặp và tiếp tục chờ đợi. Dẫn đến chương trình này chỉ làm việc được với tối đa 1 client trong 1 thời điểm, những client sau đó phải chờ cho đến khi client trước đó hoàn thành phiên làm việc mới được xử lý.

Các bạn có thể xem demo chường trình này dưới đây, tôi cùng một lúc khởi tạo 2 client với id là `1` và `2` đến socket server. Mỗi client hoạt động theo logic như sau:
- Khởi tạo kết nối đến server
- Sau một khoảng thời gian nhất định, gửi 1 xâu có giá trị `hello from {client_id}` đến server
- Sau 10 lần gửi thông điệp client sẽ gửi `EOL` đến server


Các bạn có thể thấy, server xử lý tuần tự 1 client trong 1 thời điểm, sau khi hoàn thành xử lý với `client 1`, thì server mới tiếp tục làm việc với `client 2` 



[![asciicast](https://asciinema.org/a/OMX7Buub9ksUi9k7eLiUSK6g8.svg)](https://asciinema.org/a/OMX7Buub9ksUi9k7eLiUSK6g8)


{% include_code 09/client.py lang:python :hidefilename: client.py  %}



Để giải quyết bài toán này thì mọi người thường nghĩ đến một giải pháp là `multithread`, đây cũng là giải pháp thường được các thầy giáo hướng dẫn ở trong trường đại học. Mỗi khi có một kết nối đến server thì chương trình sẽ khởi tạo 1 thread mới, xử lý data được gửi đến từ client và trả lại dữ liệu cho client.

Nhược điểm của phương pháp này nó là, mỗi thread sẽ có `call stack` riêng, và việc chuyển đổi giữa các `call stack` cũng ảnh hưởng tới hiệu năng của chương trình. Một cách khác để giải quyết vấn đề này đó chính là `non-blocking IO`, nói một cách khác, chúng ta sẽ không bắt chương trình chờ cho đến khi có data nữa.


## Non-Blocking Socket Server

{% img images/09/epoll.png 500 'Epoll' %}

Để giải quyết bài toán trên mà không sử dụng đến `multithread`, chúng ta cần sử dụng một `system call` là `epoll`. `epoll` là 1 câu lệnh của hệ điều hành linux (`system call`), đưa cho `epoll` một hoặc nhiều `file descriptors`, `epoll` sẽ trả về cho chương trình những file nào có thể đọc được.



Quay lại về bài toán lập trình socket. Để sử dụng `epoll` thì chúng ta sẽ thay đổi logic như sau:

- Khởi tạo một `socket`, và `epoll`
- Đăng kí `socket file descriptor` cùng sự kiện `EPOLLIN` vào trong `epoll`
- Tại một vòng lặp vô tận:
    + kiểm tra xem epoll có event mới nào không
    + nếu có sự kiện mới thì xử lý sự kiện đó, và tiếp tục lặp
    + nếu không thì tiếp tục quay lại vòng lặp


{% img images/09/epoll_flow.png 500 'Epoll Flow' %}



{% include_code 09/non_blocking_socket.py lines:67-94 lang:python %}

Đối với mỗi loại event thì server sẽ xử lý bằng những hàm tương ứng, chúng ta cùng xem kỹ hơn cách server xử lý từng loại sự kiện.

### Có kết nối mới từ client

Khi kiểm tra `file descriptor` của sự kiện mới là `socket server file descriptor` chúng ta hiểu được rằng là đã có một kết nối đến server.

+ Bởi vì kết nối cũng là 1 file, nên chúng ta sẽ đăng kí `fd` của kết nối này vào trong `epoll`
+ Mỗi khi có dữ liệu mới đến từ kết nối này, `epoll` sẽ tạo event mới cho chúng ta

{% include_code 09/non_blocking_socket.py lines:26-38 lang:python :hideall: %}


### Có dữ liệu từ kết nối:

+ Đọc dữ liệu từ kết nối
+ Nếu kết nối bị ngắt, xóa `fd` tương ứng khỏi `epoll`
+ Nếu có `EOL` trong dữ liệu thì set event cho `fd` trở thành `EPOLLOUT`, tương ứng với việc thông báo cho chương trình là đã đọc hết dữ liệu từ client này, hãy hồi đáp về cho client

{% include_code 09/non_blocking_socket.py lines:40-58 lang:python :hideall: %}

### Có tín hiệu hồi đáp cho client.

+ Gửi dữ liệu cho client
+ Đổi loại event cho kết nối thành `EPOLLIN`, để server tiếp lắng nghe dữ liệu mới trên kết nối này


{% include_code 09/non_blocking_socket.py lines:59-64 lang:python :hideall: %}


[![asciicast](https://asciinema.org/a/DQcgHeBbIcy7AXU1lP5VKeMqr.svg)](https://asciinema.org/a/DQcgHeBbIcy7AXU1lP5VKeMqr)


## LibUV







Nói một cách đơn giản, Libuv chỉ là 1 vòng lặp.


Đầu tiên chương trình sẽ kiểm tra vòng lặp này có đang hoạt động hay không? Chương trình có đang có kết nối, có đang có timer chưa chạy hay không, có đang mở socket nào hay không.

Tiếp theo chương trình sẽ kiểm tra xem có timer nào đang hết hạn hay không.

Thực thi các callback đang được pending trong queue.

Bước tiếp theo:

Chuẩn bị handler
Block và chờ IO từ epoll

Timeout được tính toán sao cho chương trình không phải chờ poll quá lâu. 

The core is just a loop

check timer 
call pendding callback

idle handle
prepare handle
poll for IO
check handle

Call callback
