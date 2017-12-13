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

##### LinearRegressionを使って見る

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

##### Logistic Regression

このモデルを解決するため、LogisticRegressionを使えます。LogisticRegressionは以下のモデルを使います

$$
pass =　f( \theta_{1}   \times hours + \theta_{2} )
$$

$$
h(x) = \frac{1} {(1 + e^{-z})},\ \ z = \theta_{1}x + \theta_{2}
$$

{% img right images/04/ex4.png 800 %}

$f$ の特徴を相談しましょうか？

- 値の範囲は　$[0, 1]$に制限されます。
- 水軸=0.5の点は区別点として、左の点、遠い遠いほど、予測値は０にアップロチします。逆に右の点が１にアップロチします。


確率にすると

$$
P(y=0|\ x;\theta) = 1 - h_{\theta}(x) \\
P(y=1|\ x;\theta) = h_{\theta}(x)
$$

| $h(x)$        | $y=0$         | $y=1$        |
| ------------- |---------------|--------------|
| 0.5           | 0.5           | 0.5          |
| 0.75          | 0.25          | 0.75         |
| 0.1           | 0.1           | 0.9          |



##### Log Likelihood (対数尤度)

$$
P(y|\ x;\theta) = h_{\theta}(x)^{y}(1-h_{\theta}(x))^{1-y}
$$


この変数はLikelihood変数と呼ばれます。通訳すると **「条件 $x$ の下で $y$ 値を正しく予測する確率」** 。この事例に関して、**「勉強した時間$x$の条件の下に　正しいに合格する事を予測する可能性」** ということです。
基本的には変数の右側を最大化したいです。最尤法(maximum likelihood estimation: MLE)は　Likelihoodを最大するため　$\theta$　を探します。　


デーだセットのサイズはnですから、全部のLikelihood変数を一緒にかけると、以下の変数をもらえます。
$$
L(\theta) = \prod_{i=1}^{n}p(y_{i}|x_{i};\theta)　\\
L(\theta) = \prod_{i=1}^{n}h_{\theta}(x_{i})^{y_{i}}(1-h_{\theta}(x_{i}))^{1-y_{i}}
$$

この変数を見ると、likelihoodの値範囲は0から１までですから、全部かけると小さい過ぎになります。$log$変数を使います

$$
\ell(\theta) = log\ L(\theta) \\
\ell(\theta) = \sum_{i=1}^{n}y_{i}\log(h_{\theta}(x_{i})) + (1-y_{i})\log(1-h_{\theta}(x_{i}))
$$

ですから、「maximum log likelihood」というモデルを呼ばれます。
対数尤度の曲線を以下に示します。

{% img right images/04/ex6.png 800 %}
