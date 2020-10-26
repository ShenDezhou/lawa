# -*- coding: utf-8 -*-
from distutils.core import setup
LONGDOC = """
lawa
=====

“法阿”中文分词：做最好的 Python 法律中文分词组件

"lawa" (Law-a) Chinese text segmentation: built to
be the best Python Chinese word segmentation module.

完整文档见 ``README.md``

GitHub: https://github.com/ShenDezhou/lawa

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

在线演示： ShenDezhou

安装说明
========

代码对 Python 2/3 均兼容

-  全自动安装： ``easy_install lawa`` 或者 ``pip install lawa`` / ``pip3 install lawa``
-  半自动安装：先下载 https://pypi.python.org/pypi/lawa/ ，解压后运行
   python setup.py install
-  手动安装：将 lawa 目录放置于当前目录或者 site-packages 目录
-  通过 ``import lawa`` 来引用

词典介绍
=========

* law_doc.dic和law_term.dic是使用了法规、期刊以及案例标题统计的文档频和词频字典。
* case_doc.dic和case_term.dic是案例全文统计的文档频和词频字典。
* lawa_doc.dic和lawa_term.dic是融合和法规、案例和期刊全部特征统计的文档频和词频字典，默认使用`lawa_doc.dic`作为词典加载。

中文全角字符
============

* 对于全角字符同样看作ASCII字符（英文字符）进行处理：
    * 例：“---６０００元” 分成  -, -, -, ６０００, 元

新增网络词典
=============

* 从中文维基和百度百科收集了一些互联网词语对法律语料进行了扩充，默认新词典改为`wiki_baike_law_doc.dic`。词典共7627641个词，其中法律词231316个，其余为网络词。
"""


setup(name='lawa',
      version='1.2.5',
      description='Chinese Words Segmentation Utilities',
      long_description=LONGDOC,
      author='Shen Dezhou',
      author_email='tsinghua9boy@sina.com',
      url='https://github.com/ShenDezhou/lawa',
      license="MIT",
      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='NLP,tokenizing,Chinese word segementation',
      packages=['lawa'],
      package_dir={'lawa':'lawa'},
      package_data={'lawa':['*.*','finalseg/*']}
)
