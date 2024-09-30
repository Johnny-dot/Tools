-- foa 版本
-- _dofile("cache.lua")
-- _G.cache.isUseCache = false
local respath = _sys:getGlobal('respath')
local version = _sys:getGlobal('version')
local out = _sys:getGlobal('out')

local flist = _dofile("nodod.lua")
local flist_t = {}
for i, v in pairs(flist) do
    flist_t[v] = true
end
function copyFolder(from, to)
    if _sys:copyFolder(from, to) then
        print("copy " .. from .. " to " .. to)
    end
end
function deleFolder(f)
    _sys:command("del.bat " .. f, true, false)
end
deleFolder("XA/code")
deleFolder("XA/res")
copyFolder(respath .. "/code", "XA/code")
copyFolder(respath .. "/res", "XA/res")
_sys:copyFile("version.lua", "XA/code/version.lua")
-- _G.cache.useCache(respath,"./XA")
-- _sys:command("echo.bat " .. "_app.use_sdk = true XA/code/version.lua", true, false)
local function split(s, delimiter)
    if "" == s then
        return {}
    end
    local t, i, j, k = {}, 1, 1, 1
    while i <= #s + 1 do
        j, k = s:find(delimiter, i)
        j, k = j or #s + 1, k or #s + 1
        t[#t + 1] = s:sub(i, j - 1)
        i = k + 1
    end
    return t
end

-- 合并bound到skl
function onEnumSklFile(filename)
    filename = "XA/" .. filename
    if filename:find(".skl$") then
        local bound = filename:sub(1, -5) .. "-bound.skn"
        _mf:buildSkeletonBoundSphere(filename, bound)
        _sys:delFile(bound)
    end
end
_sys:enumFile("XA", true, onEnumSklFile)

_sys.catchResError = false

---------------------------------------------------

local info = {
    name = "rg",
    path = "XA",
    code = "code/main.lua"
}

local paths = {
    -- 新资源
    "res",
    "res/audio",
    "res/char",
    "res/env",
    "res/env/skybox",
    "res/env/terrain",
    "res/env/textures",
    "res/env/water",
    "res/env/map",
    "res/mkr",
    "res/char/chm",
    "res/char/chf",
    "res/wep",
    "res/icon",
    "res/icon/face",
    "res/mon",
    "res/npc",
    "res/pet",
    "res/pfx",
    "res/textures",
    "res/swf",
    "code",
    -- 老资源
    "audio",
    "char",
    "env",
    "env/terrain",
    "env/roles",
    "env/object",
    "env/nature",
    "env/mainbuilding",
    "env/house",
    "env/skybox",
    "env/wall",
    "env/water",
    "env/pzl",
    "mkr",
    "char/chm",
    "char/chf",
    "wep",
    "icon",
    "icon/face",
    "mon",
    "npc",
    "pet",
    "pfx",
    "textures",
    "swf",
    "code"
}

local function addPath()
    for i, v in ipairs(paths) do
        _sys:addPath(v)
    end
end

local function removePath()
    for i, v in ipairs(paths) do
        _sys:delPath(v)
    end
end

local function lowertable(t)
    for k, v in pairs(t) do
        t[k] = v:lower()
    end
end

local dods = {
    "msh$",
    "skn$",
    "man$",
    "san$",
    "tga$",
    "bmp$",
    "jpg$",
    "dds$",
    "png$",
    "mp3$",
    "wav$",
    "sen$",
    "lay",
    "ttf$"
}
local needed = {"lua$", ".lst$", "cog$", "%.cur$", "%.ico$", "%.flt$", "%.swf$"}
local firsts = {".gai$"}
local ignores = {"%.exe$", "%.fob$", "%.db$", "info$", "cfg$", "txt$", ".svn", "zip$", ".fla$", "$.tmp"}

lowertable(dods)
lowertable(needed)
lowertable(firsts)
lowertable(ignores)

local function isTexture(n)
    n = n:lower()
    if n:find(".bmp$") or n:find(".jpg$") or n:find(".tga$") or n:find(".png$") then
        return true
    else
        return false
    end
end

local types = {}
types["tga"] = _Archive.TypeImage
types["bmp"] = _Archive.TypeImage
types["jpg"] = _Archive.TypeImage
types["dds"] = _Archive.TypeImage
types["png"] = _Archive.TypeImage
types["gif"] = _Archive.TypeImage
types["skn"] = _Archive.TypeMesh
types["msh"] = _Archive.TypeMesh
types["san"] = _Archive.TypeAnima
types["man"] = _Archive.TypeAnima
types["sen"] = _Archive.TypeScene
types["lua"] = _Archive.TypeScript

local function infoformat(f, needformat)
    local res = 0
    local ext = split(f, "%.")
    if types[ext[#ext]] then
        res = types[ext[#ext]]
    end
    --if f:find'textures' and not needformat then res = _Archive.TypeImageNoMip return res end
    if f:find "icon" then
        res = _Archive.TypeImageNoMip
    end
    if
    res == _Archive.TypeImage and not needformat and
    (f:find "pet" or f:find "mon" or f:find "vassals" or f:find "ui3d")
    then
        res = _Archive.TypeImageNoMip
    end
    return res
end

local function packinfo(f)
    local fn = _sys:getFileName(f, true, false)
    local dod, fmt, pack
    if fn:find("-alpha.") or flist_t[fn] then
        dod = "needed"
    else
        dod = "pack2"
    end
    local needFormat = true
    for i, v in ipairs(ignores) do
        if f:find(v) then
            needFormat = false
        end
    end
    fmt = infoformat(f, needFormat)

    return fmt, dod, pack
end

local archive = _Archive.new()
archive.appTitle = info.name
archive.appName = info.name
archive.appVersion = version
archive.launchFile = info.code
archive.mainPlugin = "fancy3d.fob"
archive:addPlugin "fancy3d.fob"
-- archive:addPlugin(' > @king.fob')
archive.fileFolder = info.path .. "\\"

------------------------------------------------------------DDS start
local function isDDS(filename)
    if not _sys:fileExist(filename) then
        return
    end

    local file = _File.new()
    file:open(filename)
    local s = file:read()
    file:close()

    local ddsflag = s:sub(1, 4)
    return ddsflag == "DDS "
end

-- Pack img.xxx and img-alpha.xxx.
local imgDDS = function(respath, name)
    if not isTexture(name) then
        return
    end
    if name:find("-alpha") then
        return
    end

    local namenoext = name:sub(1, -5)
    local ext = name:sub(-4, -1)
    local alphaname = namenoext .. "-alpha" .. ext

    local resfile = respath .. name
    local alpfile = respath .. alphaname

    if not _sys:fileExist(alpfile) then
        return
    end

    local img = _Image.new(resfile)
    img:saveToFile(resfile)
    _sys:delFile(alpfile)

    print(string.format(' ========== Pack file "%s" "%s" --> "%s"', resfile, alpfile, resfile))
end

-- Convert textures.
command = 'PVRTexTool.exe -silent -dds -fdxt %d -i "%s" -o "%s"'
local textureDDS = function(respath, name)
    if not isTexture(name) then
        return
    end
    --alpha贴图不直接转dds,alpha贴图先执行imgDDS合成后再转dds
    if name:find("-alpha") then
        return
    end
    --[[if isDDS(name) then
print(string.format('==========%s is already DDS.', name))
return
end]]
    local namenoext = name:sub(1, -5)
    local resfile = respath .. name
    local ddsname = respath .. namenoext .. ".dds"

    local format = _mf:isAlphaImage(resfile) and 3 or 1
    local cmd = string.format(command, format, resfile, ddsname)
    print(cmd)
    _sys:command(cmd, true, false)

    if not isDDS(ddsname) then
        print(string.format('++++++++++DDS convert failed, resname: "%s".', resfile))
    else
        _sys:moveFile(ddsname, resfile)
    end
end

-- Convert textures. 3D贴图加-m
command = 'PVRTexTool.exe -silent -dds -fdxt%d -m -i "%s" -o "%s"'
local textureDDS3D = function(respath, name)
    if not isTexture(name) then
        return
    end
    --alpha贴图不直接转dds,alpha贴图先执行imgDDS合成后再转dds
    if name:find("-alpha") then
        return
    end
    --[[if isDDS(name) then
print(string.format('==========%s is already DDS.', name))
return
end]]
    local namenoext = name:sub(1, -5)
    local resfile = respath .. name
    local ddsname = respath .. namenoext .. ".dds"

    local format = _mf:isAlphaImage(resfile) and 3 or 1
    local cmd = string.format(command, format, resfile, ddsname)
    print(cmd)
    _sys:command(cmd, true, false)

    if not isDDS(ddsname) then
        print(string.format('++++++++++DDS convert failed, resname: "%s".', resfile))
    else
        _sys:moveFile(ddsname, resfile)
    end
end
------------------------------------------------------------DDS end

function optimizeRes(filename)
    -- local cacheFiles = _G.cache.cacheFiles
    -- if cacheFiles and cacheFiles[filename] then
    --     return
    -- end
    local f = filename:lower()
    if isTexture(filename) then
        if filename:find("icon") then
            --icon不转dds
        elseif string.find(f, ".dds") then
            imgDDS(info.path .. "\\", f)
            textureDDS(info.path .. "\\", f)
        else
            imgDDS(info.path .. "\\", f)
            textureDDS3D(info.path .. "\\", f)
        end
    elseif string.find(f, ".bmp") then
        -- bmp转jpg,转DDS了不需要这一步
        --_mf:changeImageFormat( info.path..'\\'..f, info.path..'\\'..f, _mf.ImageJpg, 100 )
    elseif string.find(f, ".san") then
        -- 优化动画资源
        _mf:optimizeSkeletonAnimation(f)
        -- 将tag文件的信息合并到动画文件中
        _mf:checkAnimation(f)
    elseif string.find(f, ".skn") or string.find(f, ".msh") then
        -- 优化模型资源
        _mf:optimizeMesh(f)
    end
end

function onEnumFile(filename)
    local f = filename:lower()
    local fmt, dod, pack = packinfo(f)
    if fmt == nil then
        return
    end
    optimizeRes(filename)
    --转DDS了不需要这一步
    if string.find(f, ".swf") then
        local fn = _sys:getFileName(f, true, false)
        fn = string.lower(fn)
        archive:addFile(f, nil, fmt)
    end

    if not pack then
        archive:addFile(f, tostring(dod), fmt)
    else
        archive:addPack(f, pack, f)
    end
end

_sys:enumFile(info.path, true, onEnumFile)
--添加分组。打包之后先添加的组在前，后添加的在后. needed可以写也可以不写，引擎会处理。其他的分组需要写.
--[[for i, list in ipairs( neededlistScene ) do
archive:addPreGroup('pregroup'..i)
end]]
-- _G.cache.createCache(respath,"./XA")
archive.compressMode = _Archive.Compress7z
local name = "rghw"
local foaNameFont = out .. '/' .. name .. '_' .. version
archive:save(foaNameFont .. '.text', foaNameFont .. '.txt', "6a7bf9ad539301d1795155eca6425e7f")
-- deleFolder("XA/code")
-- deleFolder("XA/res")
_abort()