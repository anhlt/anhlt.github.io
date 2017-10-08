Title: RPN explained
Slug: rpn-explained
Date: 2017-10-08 03:27:29
Modified: 2017-10-08 03:27:29
Tags: RPN, faster_rcnn
Category: Deep Learning
Author: 
Lang: vi
Summary: 

#### RPN 




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


#### Nhận xét 

Khi thay đổi độ co giãn của anchors thì giá trị overlap bị thay đổi nhiều. Tùy vào dataset để thay đổi scale phù hợp        


#### Cách Tính loss function

{% include_code rpn/anchor_target_layer.py lang:python lines:208-213 :hidefilename: anchor_target_layer.py %}

	:::python
	# gt_boxes[argmax_overlaps, :]
	array([[ 140.  ,  253.75,  185.  ,  430.  ,   24.  ],
       [ 140.  ,  253.75,  185.  ,  430.  ,   24.  ],
       [ 140.  ,  253.75,  185.  ,  430.  ,   24.  ],
       ..., 
       [ 140.  ,  253.75,  185.  ,  430.  ,   24.  ],
       [ 140.  ,  253.75,  185.  ,  430.  ,   24.  ],
       [ 140.  ,  253.75,  185.  ,  430.  ,   24.  ]])