from sample.src_references.common.vos.ParaVO import ParaVO
FOA_BUILD_VO = {
    # 打包配置
    "opt" : "FOA_BUILD",
    "branches" : "tagA",
    "platform" : "android",
    "res_target" : "res",
    "lang" : "en",
    "tag" : "hwzs64",
    "sysversion" : "7.4.8",
    "bigversion" : "v1",
    "use_sdk" : True,
    "is64" : False,
    "use_localserverlist" : False,
    "isdebug" : False,
    "sandbox" : False,
    "istoiran" : False,
    "foaName" : "",
    "focName" : "",
    "channel" : "and_64_xiaomi",
    "isAppleStoreReview": False,
    "istestapp": False,
    "snapshopPath":"",
    # 转资源
    'sourceItems':None,
    'inputUrl':"",
    'outputUrl':"",
    'outputUrlExtra':"",
}

# 所有分支的SVN库链接
ALL_BRANCHES_REPO = {
    "devA":"http://devsvn.uuzuonline.net/redgold_oversea_182/Game/devA",
    "devB":"http://devsvn.uuzuonline.net/redgold_oversea_182/Game/devB",
    "tagA":"http://devsvn.uuzuonline.net/redgold_oversea_182/Game/tagA",
    "trunk":"http://devsvn.uuzuonline.net/redgold_oversea_182/Game/trunk"
}

ALL_PLATFORM = {
    "android":"android",
    "ios":"ios",
    "mclient":"mclient",
}

class FoaDetectVO(ParaVO):
    def __init__(self, pType, pPara) -> None:
        super().__init__()


