# lawa
“法阿”中文分词：做最好的 Python 法律中文分词组件

特点
====
-  支持三种分词模式：
   -  精确模式，试图将句子最精确地切开，适合文本分析；
   -  全模式，把句子中所有的可以成词的词语都扫描出来,
      速度非常快，但是不能解决歧义；
   -  搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。
-  支持繁体分词
-  支持自定义词典
-  MIT 授权协议
在线演示： 
安装说明
========
代码对 Python 2/3 均兼容
-  全自动安装： ``easy_install lawa`` 或者 ``pip install lawa`` / ``pip3 install lawa``
-  半自动安装：先下载 https://pypi.python.org/pypi/lawa/ ，解压后运行
   python setup.py install
-  手动安装：将 lawa 目录放置于当前目录或者 site-packages 目录
-  通过 ``import lawa`` 来引用

算法
========
* 基于前缀词典实现高效的词图扫描，生成句子中汉字所有可能成词情况所构成的有向无环图 (DAG)
* 采用了动态规划查找最大概率路径, 找出基于词频的最大切分组合
* 对于未登录词，采用了基于汉字成词能力的 HMM 模型，使用了 Viterbi 算法

主要功能
=======
1. 分词
--------
* `lawa.cut` 方法接受四个输入参数: 需要分词的字符串；cut_all 参数用来控制是否采用全模式；HMM 参数用来控制是否使用 HMM 模型；use_paddle 参数用来控制是否使用paddle模式下的分词模式，paddle模式采用延迟加载方式，通过enable_paddle接口安装paddlepaddle-tiny，并且import相关代码；
* `lawa.cut_for_search` 方法接受两个参数：需要分词的字符串；是否使用 HMM 模型。该方法适合用于搜索引擎构建倒排索引的分词，粒度比较细
* 待分词的字符串可以是 unicode 或 UTF-8 字符串、GBK 字符串。注意：不建议直接输入 GBK 字符串，可能无法预料地错误解码成 UTF-8
* `lawa.cut` 以及 `lawa.cut_for_search` 返回的结构都是一个可迭代的 generator，可以使用 for 循环来获得分词后得到的每一个词语(unicode)，或者用
* `lawa.lcut` 以及 `lawa.lcut_for_search` 直接返回 list
* `lawa.Tokenizer(dictionary=DEFAULT_DICT)` 新建自定义分词器，可用于同时使用不同词典。`lawa.dt` 为默认分词器，所有全局分词相关函数都是该分词器的映射。

代码示例

```python
# encoding=utf-8
seg_list = lawa.cut("本法所称转移土地、房屋权属，是指下列行为", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式


seg_list = lawa.cut("土地使用权转让，包括出售、赠与、互换；", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_list = lawa.cut("中华人民共和国民法典", cut_all=False, HMM=True)
print("HMM Mode(default on): " + "/ ".join(seg_list))  # 精确模式+新词发现模型(默认开启)

seg_list = lawa.cut("全国人民代表大会常务委员会关于授予在抗击新冠肺炎疫情斗争中作出杰出贡献的人士国家勋章和国家荣誉称号的决定", cut_all=False, HMM=True)
print("HMM Mode(default on): " + "/ ".join(seg_list))  # 精确模式+新词发现模型(默认开启)

seg_list = lawa.cut("前款第二项土地使用权转让，不包括土地承包经营权和土地经营权的转移。")  # 默认是精确模式
print(", ".join(seg_list))

seg_list = lawa.cut_for_search("在中华人民共和国境内缴纳增值税、消费税的单位和个人，为城市维护建设税的纳税人，应当依照本法规定缴纳城市维护建设税。")  # 搜索引擎模式
print(", ".join(seg_list))
```

输出:

    【全模式】:  本法/ 所称/ 转移/ 土地/ 、/ 房屋/ 权属/ ，/ 是/ 指/ 下列/ 行为

    【精确模式】: 土地/ 使用权/ 转让/ ，/ 包括/ 出售/ 、/ 赠与/ 、/ 互换/ ；

    【新词识别】：中华人民共和国/ 民法典    (此处，“民法典”并没有在词典中，但是也被Viterbi算法识别出来了)
    
                全国人民代表大会/ 常务委员会/ 关于/ 授予/ 在/ 抗击/ 新冠/ 肺炎/ 疫情/ 斗争/ 中/ 作出/ 杰出贡献/ 的/ 人士/ 国家/ 勋章/ 和/ 国家/ 荣誉称号/ 的/ 决定    (此处，“新冠”并没有在词典中，但是也被Viterbi算法识别出来了)

    【搜索引擎模式】： 在, 中华, 华人, 人民, 共和, 共和国, 中华人民共和国, 境内, 缴纳, 增值, 增值税, 、, 消费, 消费税, 的, 单位, 和, 个人, ，, 为, 城市, 维护, 建设, 税, 的, 纳税, 纳税人, ，, 应当, 依照, 本, 法, 规定, 缴纳, 城市, 维护, 建设, 税, 。

2. 添加自定义词典
----------------

### 载入词典

* 开发者可以指定自己自定义的词典，以便包含 lawa 词库里没有的词。虽然 lawa 有新词识别能力，但是自行添加新词可以保证更高的正确率
* 用法： lawa.load_userdict(file_name) # file_name 为文件类对象或自定义词典的路径
* 词典格式和 `law_doc.dic` 一样，一个词占一行；每一行分三部分：词语、词频（可省略）、词性（可省略），用空格隔开，顺序不可颠倒。`file_name` 若为路径或二进制方式打开的文件，则文件必须为 UTF-8 编码。
* 词频省略时使用自动计算的能保证分出该词的词频。

**例如：**

```
创新办 3 i
云计算 5
凱特琳 nz
台中
```

* 更改分词器（默认为 `lawa.dt`）的 `tmp_dir` 和 `cache_file` 属性，可分别指定缓存文件所在的文件夹及其文件名，用于受限的文件系统。

* 范例：

    * 自定义词典：https://github.com/shendezhou/lawa/blob/master/lawa/law_term.dic

    * 用法示例：https://github.com/shendezhou/lawa/blob/master/lawa.py


        * 之前： 李小福 / 是 / 创新 / 办 / 主任 / 也 / 是 / 云 / 计算 / 方面 / 的 / 专家 

        * 加载自定义词库后：　李小福 / 是 / 创新办 / 主任 / 也 / 是 / 云计算 / 方面 / 的 / 专家 

### 调整词典

* 使用 `add_word(word, freq=None, tag=None)` 和 `del_word(word)` 可在程序中动态修改词典。
* 使用 `suggest_freq(segment, tune=True)` 可调节单个词语的词频，使其能（或不能）被分出来。

* 注意：自动计算的词频在使用 HMM 新词发现功能时可能无效。

代码示例：

```pycon
>>> print('/'.join(lawa.cut('如果放到post中将出错。', HMM=False)))
如果/放到/post/中将/出错/。
>>> lawa.suggest_freq(('中', '将'), True)
494
>>> print('/'.join(lawa.cut('如果放到post中将出错。', HMM=False)))
如果/放到/post/中/将/出错/。
>>> print('/'.join(lawa.cut('「台中」正确应该不会被切开', HMM=False)))
「/台/中/」/正确/应该/不会/被/切开
>>> lawa.suggest_freq('台中', True)
69
>>> print('/'.join(lawa.cut('「台中」正确应该不会被切开', HMM=False)))
「/台中/」/正确/应该/不会/被/切开
```
