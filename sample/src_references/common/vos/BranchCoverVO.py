from sample.src_references.common.vos.ParaVO import ParaVO
from sample.src_references.common.vos.ParaVO import TYPE_ANALYZE_PARAMS

# 所有分支的SVN库链接
MAIN_BRANCHES_REPO = {
    "develop":"http://devsvn.uuzuonline.net/redgold_182/chengxu/branches/gongce0.1-dev-shoufa/XAserver",
}

OB_BRANCHES_REPO = {
    # "release":"http://devsvn.uuzuonline.net/redgold_182/chengxu/branches/gongce0.1/XAserver",
    "release":"http://devsvn.uuzuonline.net/redgold_oversea_182/Game/test1",
    "release":"http://devsvn.uuzuonline.net/redgold_oversea_182/Game/test",
}

BRANCH_COVER_VO = {

}

class BRANCH_COVER_VO(ParaVO):
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




