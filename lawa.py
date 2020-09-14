import lawa as lawa

#用词频来表示语言模型,默认为文档频(law_doc.dic).
lawa.load_userdict('lawa/law_term.dic')


seg_list = lawa.cut("本法所称转移土地、房屋权属，是指下列行为", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式


seg_list = lawa.cut("土地使用权转让，包括出售、赠与、互换；", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_list = lawa.cut("中华人民共和国民法典", cut_all=False, HMM=True)
print("HMM Mode(default on): " + "/ ".join(seg_list))  # 精确模式

seg_list = lawa.cut("全国人民代表大会常务委员会关于授予在抗击新冠肺炎疫情斗争中作出杰出贡献的人士国家勋章和国家荣誉称号的决定 ", cut_all=False, HMM=True)
print("HMM Mode(default on): " + "/ ".join(seg_list))  # 精确模式


seg_list = lawa.cut("前款第二项土地使用权转让，不包括土地承包经营权和土地经营权的转移。")  # 默认是精确模式
print(", ".join(seg_list))

seg_list = lawa.cut_for_search("在中华人民共和国境内缴纳增值税、消费税的单位和个人，为城市维护建设税的纳税人，应当依照本法规定缴纳城市维护建设税。")  # 搜索引擎模式
print(", ".join(seg_list))
