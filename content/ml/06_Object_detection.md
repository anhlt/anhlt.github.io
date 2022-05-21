Title: Bài toán Object Detection cổ điển
Slug: classic-object-detection
Date: 2018-01-16 19:18:33
Modified: 2018-01-16 19:18:33
Tags: vietnamese, explained, object_detection
Category: Deep Learning
Author: h4cker
Lang: vi
Summary: Giới thiệu bài toán Object Detection cổ điển, từ đó nắm bắt được ý tưởng của các thuật toán Deep Learing phức tạp hơn

Nhiều năm về trước, bài toán object detection thường sử dụng những thuật toán đơn giản, tốc độ tính toán nhanh, nhưng bù lại độ chính xác không tốt như sử dụng deep learning. Mặc dù vậy, để hiểu rõ hơn về ý tưởng của các thuật toán phức tạp hơn, hôm nay mình muốn giới thiệu ý tưởng của 1 thuật toán cổ điển, sử dụng HOG. Mục đích của bài viết này chỉ là giới thiệu về ý tưởng của thuật toán , nên mình sẽ không code bài toán này. 

### Trích xuất thuộc tính
Trích xuất thuộc tính(feature extraction) là một quá trình nhằm biến dữ liệu phức tạp đầu vào thành một cách biểu diễn dữ liệu đơn giản hơn, phù hợp hơn cho các thuật toán học máy. Dữ liệu sau khi xử lý đã được lược bỏ phần dữ liệu dư thừa, giữ lại những dữ liệu có ích cho bài toán cần xử lý.

Trong bài toán object detection, đầu vào của dữ liệu là hình ảnh , vì thế để đơn giản hơn cho việc tính toán chúng ra sử dụng một số thuật toán để trích xuất như HOG, SIFT. Trong nội dung bài viết này, tôi không đi sâu về các thuật toán trích xuất dữ liệu này.

### Histogram of Oriented Gradients 

Histogram of Oriented Gradients(HOG) là một thuật toán để trích xuất thuộc tính hình ảnh. Vậy cụ thể HOG có đầu ra như thế nào. 

- HOG chia hình ảnh đầu vào thành một lưới các ô vuông
- Mỗi ô vuông trích xuất thành một vector hướng của gradient trong cell đó

{% img right /images/06/hog_01.png 200 %}

Trích dẫn một ví dụ về đầu ra của HOG từ trang [scikit-image.org](http://scikit-image.org/docs/dev/auto_examples/features_detection/plot_hog.html)

{% img right /images/06/hog_02.png 800 hehehe %}

Từ ví dụ trên ta có thể thấy, trích xuất thuộc tính bằng HOG bảo toàn thông tin về đường viền của đối tượng trong ảnh, làm mất đi các thông tin về màu sắc, giảm độ sắc nét của dữ liệu. 

Thông thường, đầu vào của một hình ảnh có kích thước $W x H x 3$ , đầu ra của HOG là vector 1-D $N x 1$

Đã có một bài viết tiếng Việt đề cập khá cụ thể về cách tính HOG feature từ [Viblo](https://viblo.asia/p/tim-hieu-ve-hoghistogram-of-oriented-gradients-m68Z0wL6KkG). Các bạn có thể tham khảo thêm

### Sliding Window

Sau khi đã có HOG feature descriptor, ta sẽ sử dụng vào bài toán object detector. Phần này tôi sẽ lược dịch từ trang [pyimagesearch.com](https://www.pyimagesearch.com/2014/11/10/histogram-oriented-gradients-object-detection/)

1. Lấy ra số lượng P các hỉnh ảnh chưa đối tượng và trích xuât HOG feature descriptor từ các hình ảnh này
2. Lấy ra N các hình ảnh không chưa bất kì một đối tượng nào và trích xuất HOG feature descriptor từ các hình ảnh này. Trong thực tế thì $N >> P$  
3. Huấn luyện mạng SVM trên các HOG feature descriptor trên tập dữ liệu từ bước một và bước 2
4. Đối với mỗi hình ảnh trong tập không chứa đối tượng, sử dụng phương pháp sliding window, tại mỗi vị trí cửa sổ tính toán giá trị HOG và sử dụng mô hình SVM đã huấn luyện ở trên để dự đoán kết quả. Nếu mô hình đưa ra kết quả sai, lưu lại giá trị HOG tương ứng tại vị trí cửa sổ đó cùng xác suất được dự đoán

    {% img right /images/06/sliding_window_example.gif 200 %}

5. Lấy các kết quả false-positive tìm thấy ở bước 4 , sắp xếp theo giá trị của xác suất và huấn luyện lại mô hình SVM
6. Kết thúc

### Lời kết

Giải quyết bài toán object detection bằng các phương pháp cổ điển có ưu điểm là cần năng lực tính toán thấp, mô hình đơn giản, tốc độ xử lý nhanh. Nhưng trong quá trình xử lý làm mất đi nhiều thông tin giá trị của hình ảnh như màu sắc, độ sắc nét. Dẫn tới độ chính xác không cao.
