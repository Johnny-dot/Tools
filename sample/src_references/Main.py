import argparse

import sample.src_references.common.g.G as G

import sample.src_references.common.utils.InputUtil as InputUtil

import sample.src_references.common.vos.FoaBuildVO as KB_VO

from sample.src_references.common.manager.KBMgr import KBMgr
from sample.src_references.common.manager.LogMgr import LogMgr
from sample.src_references.plugin_branch_cover.BranchCover import BranchCover
from sample.src_references.plugin_foa_build.FoaBuild import FoaBuild
from sample.src_references.plugin_foa_detect.FoaDetect import FoaDetect
from sample.src_references.plugin_res_convert.ResConvert import ResConvert
from sample.src_references.plugin_duplicate_detect.DetectDuplicate import DetectDuplicate

FOA_BUILD_VO = KB_VO.FOA_BUILD_VO
TYPE_ANALYZE_PARAMS = KB_VO.TYPE_ANALYZE_PARAMS

def main(paraVo):
    opt = paraVo.getVal('opt')
    initManagers(paraVo)
    if opt == 'FOA_BUILD':
        foabuild = FoaBuild(paraVo)
        return foabuild.main()
    elif opt == 'RES_CONVERT':
        resconvert = ResConvert(paraVo)
        return resconvert.main()
    elif opt == 'BRANCH_COVER':
        branchcover = BranchCover(paraVo)
        return branchcover.main()
    elif opt == 'FILES_SNAPSHOT':
        pass
    elif opt == 'DETECT_DUPLICATE_FILES':
        detectduplicate = DetectDuplicate(paraVo)
        return detectduplicate.main()
    elif opt == 'FOA_DETECT':
        foadetect = FoaDetect(paraVo)
        return foadetect.main()
    else:
        print('不支持的操作类型%s' % opt)

def initManagers(paraVo):
    KBMgr()

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


