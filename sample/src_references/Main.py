import argparse
import importlib
import sample.src_references.common.utils.InputUtil as InputUtil
import sample.src_references.common.vos.FoaBuildVO as KB_VO
from sample.src_references.common.manager.LogMgr import LogMgr

FOA_BUILD_VO = KB_VO.FOA_BUILD_VO
TYPE_ANALYZE_PARAMS = KB_VO.TYPE_ANALYZE_PARAMS

def dynamic_import(module_path, class_name):
    """动态导入模块并获取类."""
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

def main(paraVo):
    opt = paraVo.getVal('opt')
    if opt == 'FOA_BUILD':
        FoaBuildClass = dynamic_import('sample.src_references.plugin_foa_build.FoaBuild', 'FoaBuild')
        foabuild = FoaBuildClass(paraVo)
        return foabuild.main()
    elif opt == 'RES_CONVERT':
        ResConvertClass = dynamic_import('sample.src_references.plugin_res_convert.ResConvert', 'ResConvert')
        resconvert = ResConvertClass(paraVo)
        return resconvert.main()
    elif opt == 'BRANCH_COVER':
        BranchCoverClass = dynamic_import('sample.src_references.plugin_branch_cover.BranchCover', 'BranchCover')
        branchcover = BranchCoverClass(paraVo)
        return branchcover.main()
    elif opt == 'FILES_SNAPSHOT':
        pass
    elif opt == 'DETECT_DUPLICATE_FILES':
        DetectDuplicateClass = dynamic_import('sample.src_references.plugin_duplicate_detect.DetectDuplicate', 'DetectDuplicate')
        detectduplicate = DetectDuplicateClass(paraVo)
        return detectduplicate.main()
    elif opt == 'FOA_DETECT':
        FoaDetectClass = dynamic_import('sample.src_references.plugin_foa_detect.FoaDetect', 'FoaDetect')
        foadetect = FoaDetectClass(paraVo)
        return foadetect.main()
    elif opt == 'DEBUG_ANALYSIS':
        DebugAnalysisClass = dynamic_import('sample.src_references.plugin_debug_analysis.DebugAnalysis', 'DebugAnalysis')
        debuganalysis = DebugAnalysisClass(paraVo)
        return debuganalysis.main()
    elif opt == 'GM_SERIALIZE':
        GMSerializeClass = dynamic_import('sample.src_references.plugin_gm_serialize.GMSerialize', 'GMSerialize')
        gmserialize = GMSerializeClass(paraVo)
        return gmserialize.main()
    else:
        print('没有找到此工具:%s' % opt)

def inputOneLine():
    for key in FOA_BUILD_VO:
        parser.add_argument(key)
    args = parser.parse_args()
    paraVo = KB_VO.KB_VO(TYPE_ANALYZE_PARAMS.PARSER, args)

    return paraVo

def inputByLine():
    print("直接回车则自动填入缺省值\n")
    args = {}
    for key, val in FOA_BUILD_VO.items():
        msg = "缺失值为:" + val + '\n'
        inputPara = InputUtil.inputWithMsg(msg)
        args[key] = val if inputPara == '' else inputPara
    paraVo = KB_VO.KB_VO(TYPE_ANALYZE_PARAMS.get('DICT'), args)

    return paraVo

def inputByDict(buildDict):
    args = {}
    for key, val in FOA_BUILD_VO.items():
        inputPara = buildDict.get(key)
        args[key] = val if inputPara == None else inputPara
    paraVo = KB_VO.KB_VO(TYPE_ANALYZE_PARAMS.get('DICT'), args)

    return paraVo

if __name__ == '__main__':
    LogMgr()
    parser = argparse.ArgumentParser()
    checkKey = next(FOA_BUILD_VO)
    parser.add_argument(checkKey)
    args = parser.parse_args()

    paraVo = None
    # 1.命令行连续参数输入
    if args[checkKey]:
        paraVo = inputOneLine()
    else:
    # 2.手动按行输入
        paraVo = inputByLine()

    main(paraVo)


