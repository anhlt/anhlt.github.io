Title: Logistic Regression
Slug: logistic-regression
Date: 2017-12-06 10:24:35
Modified: 2017-12-06 10:24:35
Tags: machinelearning
Category: machinelearning
Author: h4cker
Lang: jp
Summary: logistic regressionについて説明します

### 事例

Wikipediaから勉強時間と試験を合格するの関係の事例を使います。

モデルの体育のデータベースがあります。

| Study Hours   | Pass          | Study Hours  |Pass          |
| ------------- |---------------|--------------|--------------|
| 0.5           | 0             | 2.75         | 1            |
| 0.75          | 0             | 3            | 0            |
| 1             | 0             | 3.75         | 1            |
| 1.25          | 0             | 4.45         | 1            |
| ...           | ...           | ...          |...           |
| 2.5           | 0             | 5.5          | 1            |


グラップでプロットすると詳しく見えます

{% img right images/04/ex1.png 800 %}

### Logistic Regression Model

LogisticRegressionモデールを共する前に、LinearRegressionのモデルを要約しましょうか
前回のセルースのじれで、相関関係を探します
$$
\hat{Y} = \beta_0 + \beta_1 \times TV + \beta_2 \times radio + \beta_3 \times newspaper
$$

LinearRegressionは連続値を予測ために使います。$\beta_0$ $\beta_1$ $\beta_2$ $\beta_3$ を探します。


今回はLinear Regression を使って、試験を合格かを予測しましょう。

モデルを設定して、$\beta_0$ $\beta_1$　を探します。
$$
pass = \beta_0 + \beta_1 \times hours
$$

以下の結果を見えます。
{% img right images/04/ex2.png 800 %}

このグラプを見ると、以下の結論できます。

- LinearRegressionを使って、連続値を予測しますので、合格できるかを予測出来ません。
- passの値の範囲は制限されないです。
- 閾値をつかて、passを0.5より大きいは合格です。passは0.5より小さい合格しない

また、データに２０時間で勉強しました学生を追加して、もちろんその学生は合格はずです。このモデルは以下の状態になります。

{% img right images/04/ex3.png 800 %}

このモデールをつかって、多いの合格した人が合格しないと予測されました。これは良くないモデールです。

このモデルを解決するため、LogisticRegressionを使えます。LogisticRegressionは以下のモデルを使います

$$
pass =　f( \beta_0 + \beta_1 \times hours )
$$

$f$ の特徴を相談しましょうか？

{% img right images/04/ex4.png 800 %}


- 値の範囲は　$[0, 1]$に制限されます。
- 水軸=0.5の点は区別点として、左の点、遠い遠いほど、予測値は０にアップロチします。逆に右の点が１にアップロチします。

{% img right images/04/ex5.png 800 %}
