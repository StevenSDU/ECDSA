# ECDSA
任务十：ECDSA算法由签名反推公钥（Deduce public key from signature）

1、原理展示：有关“由签名反推公钥”的原理如下图所示：

![image](https://user-images.githubusercontent.com/108848022/181870611-5a538508-fab3-4df5-996a-9b6e3f737a15.png)

2、代码解释：

（1）给定参数：

![image](https://user-images.githubusercontent.com/108848022/181870640-30899897-4c20-488c-ba43-3bd2ef34aa00.png)

（2）有关求逆和约分的函数：

![image](https://user-images.githubusercontent.com/108848022/181870656-20f98e44-6158-482d-b8f0-bd90a98c9af1.png)

（3）有关计算P+Q函数、nP函数在代码中进行了详细解释，在此不再赘述。

（4）将kG的横纵坐标逆推：

![image](https://user-images.githubusercontent.com/108848022/181870693-e79f7a28-6527-47fa-a15e-92980d27eede.png)

（5）由于可以得到两种可能的纵坐标，因此我们最终会得到两种可能的公钥结果，在此分别进行计算（按照第一步所示的原理和公式）

![image](https://user-images.githubusercontent.com/108848022/181870714-6f173525-bb33-4eeb-9631-15e3d29637b6.png)

3、结果截图：可以看出，最后我们得到了符合题意的公钥，即由签名逆推公钥成功。

![image](https://user-images.githubusercontent.com/108848022/181870721-1c68fde8-dba1-4634-84f1-c68104d2f628.png)


