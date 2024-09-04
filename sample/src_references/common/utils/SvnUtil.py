import sample.src_references.common.utils.TerminalUtil as TerminalUtil

# @item 1.Path 2.URL 3.Relative URL 4.Repository Root 5.Repository UUID 
# 6.Revision 7.Node Kind 8.Last Changed Author 9.Last Changed Rev # 10.Last Changed Date
def getSvnInfo(item, repositoryUrl):
    returnList = TerminalUtil.run(["svn", "info", "--show-item", "%s" % item, repositoryUrl])
    return returnList[0]
