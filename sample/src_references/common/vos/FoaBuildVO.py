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
        "snapshotPath":"",
        "outPath1":"",
        "outPath2":"",
        # 转资源
        'sourceItems':None,
        'inputUrl':"",
        'outputUrl':"",
        'outputUrlExtra':"",
        # 文件去重
        'match_text':"",
        # 合并分支
        'source_repository_url':"",
        'destination_repository_url':"",
        'commit_message':"",
    }
# iter(
# )

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

ALL_PLATFORM_LANG = {
    "android":"安卓",
    "ios":"IOS",
    "mclient":"微端",
}

TYPE_ANALYZE_PARAMS = {
    "DICT" : "DICT",
    "PARSER" : "PARSER",
}

class KB_VO(ParaVO):
    def __init__(self, pType, pPara) -> None:
        super().__init__()
        self._uniqueKey = None
        if pType == TYPE_ANALYZE_PARAMS.get('DICT'):
            for k,v in pPara.items():
                self.setVal(k, v)
        elif pType == TYPE_ANALYZE_PARAMS.get('PARSER'):
            for k,v in pPara.items():
                self.setVal(k, v)
        else:
            # G.getG('LogMgr').error(runType, '不支持的操作类型%s'%runType)
            print('无效的vo类型')


