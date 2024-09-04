local swfurl = 'loading.swf' 
local fodname = 'rg' 
_sys.showVersion = false 
_sys.showStat = false 
_sys.showMemory = false 
_sys.fpsLimit = 30
local mainurl = 'code/main.lua' 

local uiWidth = 1130
local uiHeight = 630
local windowScaleWP = _rd.w / uiWidth
local windowScaleHP = _rd.h / uiHeight
if windowScaleWP > windowScaleHP then
    windowScaleP = windowScaleHP
else
    windowScaleP = windowScaleWP
end
local t = _Timer.new()
local swf = _SWFManager.new(swfurl)
local addWP = nil
local addHP = nil
-- if isFullScreen then
--     addWP = (_rd.w / swf._width) - 1
--     addHP = (_rd.h / swf._height) - 1
-- else
addWP = windowScaleP - 1
addHP = addWP
-- end
local tempA = swf._width
local addW2 = tempA * addWP
swf._width = tempA + addW2
tempA = swf._height
local addH2 = tempA * addHP
swf._height = tempA + addH2

--align
local addW = swf.stageWidth * addWP
local addH = swf.stageHeight * addHP
local align = swf.stageAlign
if string.find(align, "R") then
    swf._x = swf._x - addW
elseif string.find(align, "L") then
    -- swf._x = swf._x
else
    swf._x = swf._x - (addW / 2)
end

if string.find(align, "T") then
    -- swf._y = swf._y
elseif string.find(align, "B") then
    swf._y = swf._y - addH
else
    swf._y = swf._y - (addH / 2)
end

local hasCount = nil
local totalCount = 0
local curr = 0
local lastCurrCount = 0
local lastprog = 0
local function onProgress(prog, finishCount, count, finishSize, size, speed)
	if not hasCount then 
        hasCount = finishCount 
        totalCount = count-hasCount
    end
    curr = finishCount-hasCount
    if curr <= lastCurrCount then
        return
    end
    lastCurrCount = curr
    lastprog = prog
    if curr == totalCount then
        swf.curText.htmlText = '正在进入游戏...'
        swf.cur:gotoAndStop(100)
        return
    end
    swf.curText.htmlText = string.format('%.1f%%', prog * 100) .. ' (' .. curr .. '/' .. totalCount .. ')'
    swf.cur:gotoAndStop(math.floor(prog * 100))
    print(prog, math.floor(prog * 100))
end

local function onComplete(done, ver)
    t:stop('checknet')
    isUpdate = false
    if done then
        print(done,ver)
        _reset(mainurl, fodname)
    else
        if ver == 0 then
            swf.dialogMc._visible = true
            swf.dialogMc.msg.text = '检查更新失败，是否重试？'
            swf.dialogMc.hitTestDisable = false
        else
            swf.dialogMc._visible = true
            swf.dialogMc.msg.text = '更新资源超时，是否重试？'
            swf.dialogMc.hitTestDisable = false
        end
        print('not need update')
    end
end

local function onUpdate(needupdate, version)
    print(needupdate,version)
    if needupdate then
        swf.version.text = _sys:getGlobal('bigversion') .. string.sub(_sys.version, 5, 10) .. version
        _sys:doUpdate(onComplete, onProgress)
    else
        onComplete(needupdate, version)
    end
end

local isUpdate = false
local function onSure()
    swf.dialogMc._visible = false
    if _sys.networkState == _System.NetNone then 
        swf.dialogMc._visible = true
        swf.dialogMc.msg.text = '当前网络不可用，是否重试？'
        swf.dialogMc.hitTestDisable = false
    else
        if isUpdate then return end
        swf.dialogMc._visible = false
        swf.dialogMc.hitTestDisable = true
        _sys:httpGet('http://120.132.69.194/foa.php?dev=android&c=dev', function(foaurl)
            print('check update '.. foaurl)
            _sys:checkUpdate(foaurl, onUpdate, fodname)
            isUpdate = true
        end)
        t:start('checknet', 5000, onSure)
    end
end

local function onCancel()
    _abort()
end

swf.dialogMc._visible = false
swf.dialogMc.hitTestDisable = true
swf.dialogMc.cancelBtn.click = onCancel
swf.dialogMc.btnClose.click = onCancel
swf.dialogMc.sureBtn.click = onSure

onSure()
