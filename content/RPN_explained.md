Title: RPN explained
Slug: rpn-explained
Date: 2017-10-08 03:27:29
Modified: 2017-10-09 03:27:29
Tags: RPN, faster_rcnn, vietnamese, explained
Category: Deep Learning
Author: h4cker
Lang: vi
Summary: 

#### RPN

Đối với Fast RCNN , do chia sẻ tính toán giữa các region trong ảnh, tốc độ thực thực thi của thuật toán đã được giảm từ 120s mỗi ảnh xuống 2s. Phần tính toán gây ra nghẽn chính là phần đưa ra các region proposal đầu vào, chỉ có thể thực thi tuần tự trên CPU. 



RPN giải quyết các vấn đề trên bằng cách huấn luyện mạng neural network để đảm nhận thay vai trò của các thuật toán như selective search vốn rất chậm chạp

#### Cấu trúc mạng neural network 

RPN cấu tạo gồm 3 thành phần chính


	:::
	RPN (
	(features): Sequential (
	    (0): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
	    (1): ReLU (inplace)
	    (2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
	    (3): ReLU (inplace)
	    (4): MaxPool2d (size=(2, 2), stride=(2, 2), dilation=(1, 1))
	    (5): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
	    (6): ReLU (inplace)
	    (7): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
	    (8): ReLU (inplace)
	    (9): MaxPool2d (size=(2, 2), stride=(2, 2), dilation=(1, 1))
	    (10): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
	    (11): ReLU (inplace)
	    (12): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
	    (13): ReLU (inplace)
	    (14): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
	    (15): ReLU (inplace)
	    (16): MaxPool2d (size=(2, 2), stride=(2, 2), dilation=(1, 1))
	    (17): Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
	    (18): ReLU (inplace)
	    (19): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
	    (20): ReLU (inplace)
	    (21): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
	    (22): ReLU (inplace)
	    (23): MaxPool2d (size=(2, 2), stride=(2, 2), dilation=(1, 1))
	    (24): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
	    (25): ReLU (inplace)
	    (26): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
	    (27): ReLU (inplace)
	    (28): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
	    (29): ReLU (inplace)
	    (30): MaxPool2d (size=(2, 2), stride=(2, 2), dilation=(1, 1))
	)
	(conv1): Conv2d (
		(conv): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
		(relu): ReLU (inplace)
	)
	(score_conv): Conv2d (
		(conv): Conv2d(512, 18, kernel_size=(1, 1), stride=(1, 1))
	)
	(bbox_conv): Conv2d (
		(conv): Conv2d(512, 36, kernel_size=(1, 1), stride=(1, 1)))
	)


#### Cách tạo Anchor  



	:::python
	from faster_rcnn.utils.cython_bbox import bbox_overlaps

	overlaps = bbox_overlaps(
		np.ascontiguousarray(box_data[:,1:], dtype=np.float),
		np.ascontiguousarray(origin_gt_box, dtype=np.float))



Với scale của anchors là 

	:::python
	anchor_scales = [4, 8, 16]

Ta thu được kết quả sau 

{% img  images/rpn/index.png 600  'Best overlap anchors' %}

Với các giá trị overlap lần lượt là:
​   

	:::python
	array([ 0.50942772,  0.69580078,  0.81643243])


Ảnh test thử anchor và groud boxes



Với scale của anchors là 

	:::python
	anchor_scales = [8, 16, 32]

Ta thu được kết quả sau 

{% img  images/rpn/index2.png 600  'Best overlap anchors' %}

Với các giá trị overlap lần lượt là:

	:::python   
	array([ 0.33923037,  0.69580078,  0.81643243])


##### Nhận xét 

Khi thay đổi độ co giãn của anchors thì giá trị overlap bị thay đổi nhiều. Tùy vào dataset để thay đổi scale phù hợp        


#### Loss function

Khi training RPN, chúng ta gán các label cho các anchor theo logic, anchor sẽ được gắn nhãn positive nếu thỏa mãn

- Đó là anchors có giá trị overlap lớn nhất với một ground truth box.
- Đó là một anchors có giá trị overlap lớn hơn 0.7 với bất kì ground-truth box nào.

Các non-positive anchors có giá trị overlap bé hơn 0.3 thì được gán là negative anchor.Với cách gán các anchor nêu trên. Loss function sẽ được định nghĩa theo công thức sau 

$$
L(\{ p_i \}, \{ t_i \}) = \frac{1}{N_{cls}} \sum_{i} L_{cls} (p_i, p_i^{*}) + \lambda \frac{1}{N_{reg}} \sum_{i} p_i^{*} L_{reg}(t_i, t_i^{*})
$$

Với $i$ là index của anchor trong mini-batch và $p_i$ là xác suất dự đoán của anchor $i$ là một đối tượng. Giá trị nhãn ground-truth $p_i^{*}$ là một nếu anchor là positive, và là không khi anchor là negative.

- $t_i$  là một vector 4 chiều biểu diễn giá trị tọa độ của bounding box đã được dự đoán. 
- $t_i^{*}$ là vector 4 chiều biểu diễn giá trị tọa độ của ground-truth box tương ứng với positive anchor.

- $L_{cls}$ là log loss của 2 class (object và non-object) 
- $L_{reg}$ dùng SmoothL1Loss




##### Công thức tính Smooth L1

$$
loss(x, y) = \sum \begin{cases} 
		0.5 * (x_i - y_i)^2, if |x_i - y_i| < 1 \\  
		|x_i - y_i| - 0.5,   otherwise   
		\end{cases} \quad
$$

{% include_code rpn/anchor_target_layer.py lang:python lines:208-227 :hidefilename: anchor_target_layer.py %}

`bbox_inside_weights` tương ứng với giá trị nhãn $p_{i}^{*}$ có giá trị bằng một khi anchor tương ứng là positive anchors

`bbox_outside_weights`  là hệ số để cân bằng giữa positive anchor và negative anchors  và đã nhân với giá trị  $\frac{1}{N_{reg}}$ . Trong cấu hình đưa ra thì `TRAIN.RPN_POSITIVE_WEIGHT = -1`. Lúc này giá trị hệ số là bằng nhau.





Định ngĩa của loss function

	:::
	layer {
	  name: "rpn_loss_bbox"
	  type: "SmoothL1Loss"
	  bottom: "rpn_bbox_pred"
	  bottom: "rpn_bbox_targets"
	  bottom: 'rpn_bbox_inside_weights'
	  bottom: 'rpn_bbox_outside_weights'
	  top: "rpn_loss_bbox"
	  loss_weight: 1
	  smooth_l1_loss_param { sigma: 3.0 }
	}

File C thực thi

{% include_code rpn/smooth_L1_loss_layer.cpp lang:cpp lines:51-82 :hidefilename: smooth_L1_loss_layer.cpp %}


#### Trích Dẫn

1. ["How-does-RPN-work-on-the-Faster-R-CNN"](https://www.quora.com/How-does-RPN-work-on-the-Faster-R-CNN?no_redirect=1 "How-does-RPN-work-on-the-Faster-R-CNN")
