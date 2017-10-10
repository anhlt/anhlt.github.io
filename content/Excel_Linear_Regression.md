Title: ExcelでLinear Regressionを調査します 
Slug: excelでlinear-regressionを調査します
Date: 2017-10-11 00:35:46
Modified: 2017-10-11 00:35:46
Tags: 
Category: 
Author: 
Lang: 
Summary:

#### Dataset

私たちは統計コンサルタントとしてクライアントは、特定の製品の販売を改善する方法に関してアドバイスを提供します。
報告データセットは２００の市場でその製品の販売と３つのメディアにおける製品の報告予算で構成されています。


| TV            | Radio         | Newpaper    |Sales|
| ------------- |---------------|-------------|-----|
| 230.1         | 37.8          | 69.2        |22.1 |
| 44.5          | 39.3          | 45.1        |10.4 |
| ...           | ...           | ...         | ... |
| 180           | 10.8          | 58.4        |12.9 |


#### Scatter plotでデータを分析します。

![aa](images/excel_linear_regression/TV.png)

TV

![aa](images/excel_linear_regression/radio.png)

radio

![aa](images/excel_linear_regression/newspaper.png)

newspaper





#### Function

$$
sales \approx \beta_0 + \beta_1 \times TV + \beta_2 \times radio + \beta_3 \times newspaper + \epsilon
$$


Linear Regressionのゴールはい一番いいな傾向のラインを派生する為です。この場合は$\beta_0$, $\beta_1$,$\beta_2$,$\beta_3$　四つのパラメータを探します。

パラメータを使って、Salesを予測できます。

$$
\hat{Y} = \beta_0 + \beta_1 \times TV + \beta_2 \times radio + \beta_3 \times newspaper
$$ 










