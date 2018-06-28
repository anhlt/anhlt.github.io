Title: Linear Regression Explained
Slug: linear-regression-explained
Date: 2017-10-05 17:57:36
Modified: 2017-10-05 17:57:36
Tags: explained, japanese
Category: machinelearning 
Author: h4cker
Lang: jp
Summary:
Status: draft


## Problem 🏟 

あるファッションな会社で、かわいい女の子が多いです。入社する時、健康診断とか、IQ試験とかをしないといけないです。

{% img right images/post_2/girl.jpg %}

モデルの体育のデータベースがあります。

| Height        | Weight        | IQ    |Age | Breast size |　
| ------------- |---------------|-------|----|-------------|
| 170 cm        | 60  kg        | 150   | 18 |100          |
| 150 cm        | 54  kg        | 90    | 20 |70           |
| 160 cm        | 71  kg        | 70    | 25 |88           |
| 166 cm        | 86  kg        | 80    | 22 |78           |
| ...           | ...           | ...   | ...|...          |
| 180 cm        | 67  kg        | 80    | 90 |96           |

新モデルを入社する時、胸の測定さずに、おっぽいサイズを予測できますかという問題が発生します。

## The Illustration

想定すると、グルップの女の子のデータを集まります。体重、身長、IQ, 年齢,おっぽいサイズのデータを取得できました。体重、身長、IQ, 年齢のデータが簡単に収得できましたが、おっぽいのサイズは難しいです。

もしおっぽいのサイズを予測できると、いいかな？？？

どのファクターを使って、おっぽいサイズを予測できるか？　scatterplotsはとても役に立つ。

{% img right images/post_2/height.png 300 400 %}


{% img right images/post_2/weight.png 300 400 %}

このグラフを見ると、一貫した傾向を観察できます。赤いのラインを見ると体重の値からおっぽいのサイズを予測できます。
どうやって赤いラインを描けますか？

## Technical Explanation

Linear Regressionのゴールはい一番いいな傾向のラインを派生する為です。このラインは、予測誤差をできるだけ減らすように配置されています。以下のシミュレーションでは、位置がずれている傾向線が大きな予測誤差をもたらす方法を示していますが、線がデータポイントに近づくほど予測精度は向上します。

{% img right images/post_2/line.gif 300 400 %}

だから、２つの変数の傾向のラインが配置できれば、おっぽいのサイズを予測できます。

反対にいかのグラフは予測できません。

{% img right images/post_2/age.png 300 400 age %}

{% img right images/post_2/iq.png 300 400 iq %}

## Comparing predictors

強力な予測因子であるかどうかを推測するために、データ点が傾向ラインにどれだけ近づいているかを調べることができます。これは、correlation coefficientによって測定される。

傾向ラインに沿ってデータポイントが密集している場合、それはファクターが強いというサインであり、大きなcorrelation coefficientで表されます。


Correlation coefficients　の範囲は−１から１までです。体重が増加すると、おっぽいサイズも向上します。Correlation coefficients は　＞0.

しかし、IQとおっぽいのサイズ比較する時、Correlation coefficientsの値は0を期待できます。

{% img right images/post_2/simulation.gif 300 400 simulation %}

## Limitation