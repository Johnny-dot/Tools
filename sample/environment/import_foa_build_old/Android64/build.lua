_dofile('version.lua')

local pack1 = {}
for _,v in ipairs(_dofile('nodod.lua') or {}) do
    pack1[v] = true
end
local pack2 = {}
for _,v in ipairs(_dofile('pack2.lua') or {}) do
    pack2[v] = true
end

local lang = _dofile('cfg_language.lua')

local function split(s, delimiter)
    if ''==s then return {} end
    local t, i, j, k = {}, 1, 1, 1
    while i <= #s+1 do
        j, k = s:find(delimiter, i)
        j, k = j or #s+1, k or #s+1
        t[#t+1] = s:sub(i, j-1)
        i = k + 1
    end
    return t
end

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
    local n = _sys:getFileName(f, true, false)
    if f:find('-alpha.') or pack1[n] then
        dod = "needed"
    elseif pack2[n] then
        dod = "pack2"
    end
    fmt = infoformat(f, path)
    for k, v in next, ignores do
        if f:find(v) then
            fmt = nil
        end
    end
    return fmt, dod, pack
end

local is64 = _sys:getGlobal("is64") == "true"
local createArchive = function()
    local archive = _Archive.new()
    archive.appTitle = name
    archive.appName = name
    archive.appVersion = version
    archive.launchFile = code
    archive.mainPlugin = mainPlugin
    archive.baseManifest = focName
    archive:addPlugin(mainPlugin)
    archive.fileFolder = path..'\\'
    return archive
end
local archive = createArchive()
local isAndroid = platform == "android"

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
		local gname = ''
        if dod and dod == 'needed' then
			gname = 'needed'
        elseif dod and dod == "pack2" then
            gname = "pack2"
        else
            local isnottrans = true
            for i,v in ipairs(lang) do
                local sss = split(f, '\\')
                if v.short~='en' and (sss[#sss]:lead(v.short..'_') or sss[#sss]:lead('text-'..v.short)) then
                    isnottrans = false
					gname = v.short..'pack'
                end
            end
            if isnottrans then
				gname = 'pack3'
            end
        end

        -- add lua64

		if fmt == _Archive.TypeScript and isAndroid then
			local logicname = f:sub( 1, -5 ) .. '.lua64'
			archive:addFile( f, gname, _Archive.TypeScript2, logicname )
		end

        archive:addFile( f, gname, fmt, f )
    end
end
_sys:enumFile(path, true, onEnumFile)

local foaNameFont = out .. '/' .. name .. '_' .. version
archive:save(foaNameFont .. '.foa', foaNameFont .. '.txt', '6a7bf9ad539301d1795155eca6425e7f')
_abort()
