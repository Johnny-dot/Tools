_dofile('version.lua')

local function optimizeRes(f)
    f = path .. '/res/'..f
    if f:find('%.san$') then
        -- _mf:optimizeSkeletonAnimation(f) -- 优化动画资源, 对特殊动画进行过滤，不优化
    elseif f:find('%.skn$') or f:find('%.msh$') then
        _mf:optimizeMesh(f) -- 优化模型资源
    elseif f:find('%.bmp$') then
        _mf:resizeImage(f, f, 1, 1); -- 缩小图片尺寸为1/4
        _mf:changeImageFormat(f, f, _ModelFactory.ImageJpg, 100); -- 将图片转成JPG格式
    elseif f:find('%.tga$') then
        _mf:resizeImage(f, f, 0.5, 0.5); -- 缩小图片尺寸为1/4
        _mf:changeImageFormat(f, f, _ModelFactory.ImagePng , 100); -- 将图片转成TGA格式
    end
end

_sys:enumFile(path .. '/res/', true, optimizeRes)

local function infoformat(f, path)
    if platform == 'android' then
        if string.find(f, 'lua$') then
            return _Archive.TypeScript
        end
    end
    -- if _sys:getExtention(f) == 'lua' then
    --     if string.find(f, 'cfg_') then
    --         local aaaa = _dofile(path .. '/' .. f)
    --         if type(aaaa) == 'table' then
    --             -- print('TypeScript----', f)
    --             _sys:delFile(path .. '/' .. f)
    --             return _Archive.TypeScript
    --         else
    --             print('TypeConfig>>>>', f)
    --             return _Archive.TypeConfig
    --         end
    --     else
    --         -- print('TypeScript----', f)
    --         _sys:delFile(path .. '/' .. f)
    --         return _Archive.TypeScript
    --     end
    -- end
    if string.find(f, 'mp3$') or string.find(f, 'mp4$') then
        return _Archive.TypeStream
    end
    return 0
end

local dods = {'msh$', 'skn$', 'man$', 'san$', 'tga$', 'bmp$', 'jpg$', 'dds$', 'png$', 'mp3$', 'wav$', 'pfx$', 'walk$', 'sen$', 'skl$','mov$'}
local ndods = {'lua$', '.lst$', 'cog$', '%.cur$', '%.ico$', '%.flt$', '%.swf$'}
local ignores = {'%.exe$', '%.fob$', '%.db$', 'cfg$', 'inf$', 'thumbs.db$', '%.log$', '.fla$', 'info$'}
local function packinfo(f, path)
    local dod, fmt, pack
    for k, v in next, dods do
        if f:find(v) then
            dod = ''
            break
        end
    end
    if f:find('%.gai$') then
        pack = 'gai'
    end
    if f:find('%.pfx$') then
        pack = 'pfx'
    end
    if f:find('%.gif$') then
        pack = 'gif'
    end
    if f:find('%.tag$') then
        pack = 'tag'
    end
    if f:find('%.skl$') then
        pack = 'skl'
    end
    -- if f:find('%.lua$') then
    --     if f:find('cfg') then
    --         pack = 'luacfg'
    --     else
    --         pack = 'lua'
    --     end
    -- end
    for k, v in next, ndods do
        if f:find(v) then
            dod = 'needed'
            break
        end
    end
    fmt = infoformat(f, path)
    for k, v in next, ignores do
        if f:find(v) then
            fmt = nil
        end
    end
    return fmt, dod, pack
end

local archive = _Archive.new()
archive.appTitle = name
archive.appName = name
archive.appVersion = version
archive.launchFile = code
archive.mainPlugin = mainPlugin
archive.baseManifest = focName
archive:addPlugin(mainPlugin)

archive.fileFolder = path..'\\'
function onEnumFile(filename)
    local f = filename
    if platform == 'ios' then
        if string.find(f, 'android') and string.find(f, 'shr') then
            print('jump---android--->', f)
            return
        end
    elseif platform == 'android' then
        if string.find(f, 'ios') and string.find(f, 'shr') then
            print('jump---ios--->', f)
            return
        end
    end
    local fmt, dod, pack = packinfo(f, path..'\\')
    if not fmt then return end
    if pack then
        archive:addPack(f, pack, f)
    else
        archive:addFile(f, 'needed', fmt, f)
    end
end
_sys:enumFile(path, true, onEnumFile)

local foaNameFont = out .. '/' .. foaName .. '_' .. version
archive:save(foaNameFont .. '.foa', foaNameFont .. '.txt', '6a7bf9ad539301d1795155eca6425e7f')

_abort()