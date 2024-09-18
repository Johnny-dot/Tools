_dofile('convertconfig.lua')
local path = _G.ConvertConfig.FolderIn

-- 获取不合规的资源
-- 渲染类型为ColorKey
-- 纹理层数不为空.layer:纹理层数,取值范围为[0, 3],默认值为0
-- local function IsIncompatibleFiles(f)
--     local ext = _sys:getExtention(f)
--     local relativeResPath = path .. f
--     -- 跳过.skn、.msh类型的文件
--     if ext == 'skn' or ext == 'msh' then
--         local msh = _Mesh.new(relativeResPath)
--         local submeshs = msh:getSubMeshs()
--         local meshes = #submeshs > 0 and submeshs or {submeshs}

--         for i, submesh in pairs(meshes) do
--             if submesh.isColorKey then
--                 for ii = 0, 3 do
--                     local img = submesh:getTexture(ii)
--                     if img then
--                         if _sys:getFileName(img.resname, true, false) == _sys:getFileName(f, true, false) then
--                             -- Test 测试是否存在参数不同结果相同
--                             if img.resname ~= f then
--                                 print("test1 output")
--                             end
--                             return true
--                         end
--                     end
--                 end
--             end
--         end
--     end

--     return false
-- end

etcingnore = {}
imgScale = 1

local function getEtcingnore(path)
    _sys:enumFile(path, true, function(f)
        local fullfilename =  path .. f
        local ext = _sys:getExtention(f)
    
        if ext ~= 'skn' and ext ~= 'msh' then return end
        local msh = _Mesh.new(fullfilename)
        local submeshs = msh:getSubMeshs()
        if #submeshs > 0 then
            for i, submesh in next, msh:getSubMeshs() do
                if submesh.isColorKey then
                    for ii = 0, 3 do
                        local img = submesh:getTexture(ii)
                        if img then
                            local etcingnoreFile = _sys:getFileName(img.resname, true, false)
                            etcingnore[etcingnoreFile] = true
                        end
                    end
                end
            end
        else
            if msh.isColorKey then
                for ii = 0, 3 do
                    local img = msh:getTexture(ii)
                    if img then
                        local etcingnoreFile = _sys:getFileName(img.resname, true, false)
                        etcingnore[etcingnoreFile] = true
                    end
                end
            end
        end
    end)

end


fileNum = 0
jumpNum = 0

local function Main()

    getEtcingnore(path)

    for filename, _ in pairs(etcingnore) do
        print("getEtcingnore is in filename:", filename)
    end

    
    -- @path #string 枚举的目录
    -- @recursive #bool 是否枚举子文件夹
    -- @enumFunc #function[@doneFunc #function]
    -- 枚举目录下的文件。每次枚举都调用回调函数enumFunc,参数为枚举到的文件名。枚举全部完成后会调用doneFunc
    _sys:enumFile(path, true, function(f)

            fileNum = fileNum + 1
        --if not IsIncompatibleFiles(f) then
            local extname = _sys:getExtention(f)
            local relativeResPath = path .. f
            local fileName = _sys:getFileName(relativeResPath, true, false)


            if etcingnore[fileName] then 
                print('etcingnore---->>>>--', fileName, jumpNum)
                jumpNum = jumpNum + 1
                return 
            end

            if extname:find('san$') then
                --print('optimization san--->', fileNum, relativeResPath, jumpNum)
                -- _mf:optimizeSkeletonAnimation(relativeResPath) -- 优化动画资源
            elseif extname:find('skn$') or f:find('msh$') then
                print('optimization skn--->', fileNum, relativeResPath, jumpNum)
                _mf:optimizeMesh(relativeResPath) -- 优化模型资源
            end

            if extname:find("tga$") or extname:find("bmp$") then
                local size = _mf:getImageSize(relativeResPath)             -- 获取原尺寸
                if size.width < 8 and size.height < 8 then
                    print('Image size too little ----------->', fileName, size.width, size.height)
                    return
                end
                print('img--info->', fileNum, relativeResPath, jumpNum)

                local wholepath = _sys:getFileName(relativeResPath, false, true)
                local name = _sys:getFileName(relativeResPath, false, false)
                _mf:resizeImage(relativeResPath, relativeResPath, imgScale, imgScale); -- 缩小图片尺寸为1/4
                local size = _mf:getImageSize(relativeResPath)             -- 获取原尺寸
                _mf:resizeImagePowerOfTwo(relativeResPath, relativeResPath, true) -- 拉伸至符合规格的最小尺寸
        
                if _mf:isAlphaImage(relativeResPath) then
                    command = string.format("etcpack %s . -c etc1 -as", relativeResPath)
                else
                    command = string.format("etcpack %s . -c etc1", relativeResPath)
                end
        
                _sys:command(command, true, false)
                
                _sys:moveFile(name .. ".pkm", relativeResPath)
                _mf:addImageHeader(relativeResPath, size.width, size.height)-- 写入原始尺寸
        
                local fromAlpha = name .. "_alpha.pkm"
                local toAlpha = wholepath .. "-alpha." .. extname
                if _sys:fileExist(fromAlpha) then
                    _sys:moveFile(fromAlpha, toAlpha)
                    _mf:addImageHeader(toAlpha, size.width, size.height)-- 写入原始尺寸
                end
            end
        --end
    end)
end

Main()
print('============================= FINISHED =============================')
_abort()