import lawa as lawa

#用词频来表示语言模型,默认为文档频(law_doc.dic).
#增加了维基中文和百科词典，增加词表后对网络语言适配更好。
#lawa.load_userdict('lawa/wiki_baike_all.dic')


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

seg_list = lawa.cut("举例来说，国内近年来围绕游戏版权的直播和短视频平台侵权案件不断发生，游戏版权人在经过艰难诉讼后获得的，仅仅是对起诉前平台存在侵权内容的移除。平台因为不负有后续的屏蔽义务，对于起诉后再次上传的侵权游戏短视频，仍然会放纵其存在和滋生，借以吸引用户、流量来牟利。")
print(", ".join(seg_list))

#FF01-FF5F
seg_list = lawa.cut_for_search("---６０００元")  # 默认是精确模式
print(", ".join(seg_list))