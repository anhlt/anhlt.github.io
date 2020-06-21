Title: Giải thích bài báo DEtection TRansformer
Slug: End-t-End-transformer-classic-object-detection
Date: 2020-06-16 19:18:33
Modified: 2020-06-16 19:18:33
Tags: vietnamese, explained, object_detection, transfomer
Category: Deep Learning
Author: h4cker
Lang: vi
Summary: Giới thiệu bài toán Object Detection cổ điển, từ đó nắm bắt được ý tưởng của các thuật toán Deep Learing phức tạp hơn

Từ trước đến nay bài toán object detection thường dựa vào các thuật toán thiết kế thủ công như Non-maximum Suppession, hay anchor generation để thiết kế mạng network. Bài báo này đưa ra một phương pháp mới mới gọi là "DEtection TRansformer" sử dụng kiến trúc transfomer để giải quyết bài toán object detection.

### Kiến trúc mạng DETR

{% img  images/08/network.png 1000  'DETR' %}

Kiến trúc mạng DETR gồm 3 thành phần chính

1. __Backbone network__
    
    Tương tự như Faster RCNN, DETR sử dụng một mạng CNN để thu được `convolutional features` của ảnh đầu vào. 

    Với mỗi ảnh đầu vào có kích thước

    $$x_{\mathrm{img}} \in \mathbb{R}^{3 \times H_{0} \times W_{0}}$$

    thu được `convolutional features` có kích thước 

    $$f \in \mathbb{R}^{C \times H \times W} $$
    
    trong đó $C=2048$ , $H, W=\frac{H_{0}}{32}, \frac{W_{0}}{32}$


    {% img  images/rpn/step-1.png 400  'Fast RCNN' %}

2. __Transformer encoder__    
    
    Ở đây, tác giả sử dụng $1x1$ convolution để giảm chiều `convolutional features` từ $C$ xuống $z_{0} \in \mathbb{R}^{d \times H \times W}$. 
    Bởi vì `encoder` có đầu vào dạng `sequence`, tại đây, `features` được `flatten` thành $z_{0} \in \mathbb{R}^{d \times HW}$ 

    {% img  images/08/step1.png 400  'Fast RCNN' %}


    {% img  images/08/transformer.png 400  'Encoder-Decoder' %}



### Loss Function

$$
\mathcal{L}_{\text {Hungarian }}(y, \hat{y})=\sum_{i=1}^{N}\left[-\log \hat{p}_{\hat{\sigma}(i)}\left(c_{i}\right)+\mathbb{1}_{\left\{c_{i} \neq \varnothing\right\}} \mathcal{L}_{\mathrm{box}}\left(b_{i}, \hat{b}_{\hat{\sigma}}(i)\right)\right]
$$


