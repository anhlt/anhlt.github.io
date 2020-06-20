Title: Bài toán Object Detection cổ điển
Slug: End-t-End-transformer-classic-object-detection
Date: 2020-06-16 19:18:33
Modified: 2020-06-16 19:18:33
Tags: vietnamese, explained, object_detection, transfomer
Category: Deep Learning
Author: h4cker
Lang: vi
Summary: Giới thiệu bài toán Object Detection cổ điển, từ đó nắm bắt được ý tưởng của các thuật toán Deep Learing phức tạp hơn

Từ trước đến nay bài toán object detection thường dựa vào các thuật toán thiết kế thủ công như Non-maximum Suppession, hay anchor generation để thiết kế mạng network. Bài báo này đưa ra một phương pháp mới mới gọi là "DEtection TRansformer" sử dụng kiến trúc transfomer để giải quyết bài toán object detection.

### Kiến trúc mạng 

{% img  images/08/network.png 600  'DETR' %}


1. __Feed-forward ảnh qua DNN thu được convolutional features.__
    
    Trong bài báo gốc, tác giả đã nhắc đến nhiều các mạng Convolution Network có sẵn như VGG-16, ZFNet, để dễ dàng cho việc giải thích, chúng ta sẽ lấy ví dụ ở đây là mạng VGG-16. 

    Mạng VGG-16 chứa 13   convolutions layer kích thước $3 \times 3$ cùng với 5  max pooling layer kích thước $2 \times 2$. Khi đầu vào là một ảnh có kích thước $3 \times W \times H$ , đầu ra sẽ nhận được $3 \times W^{'} \times H^{'}$ với $W^{'} = \frac{W}{16}$ $H^{'} = \frac{H}{16}$

    {% img  images/rpn/step-1.png 600  'Fast RCNN' %}

2.     




### Loss Function

$$
\mathcal{L}_{\text {Hungarian }}(y, \hat{y})=\sum_{i=1}^{N}\left[-\log \hat{p}_{\hat{\sigma}(i)}\left(c_{i}\right)+\mathbb{1}_{\left\{c_{i} \neq \varnothing\right\}} \mathcal{L}_{\mathrm{box}}\left(b_{i}, \hat{b}_{\hat{\sigma}}(i)\right)\right]
$$


