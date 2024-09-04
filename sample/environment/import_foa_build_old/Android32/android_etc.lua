version = 100
tools = {
    {
        name = 'rg',
        path = 'client_etc',
        code = 'code/main.lua',
    }
}
imgScale = 1

-- ETC压缩。
-- 压缩工具 etcpack.exe。
-- ETC部分机型需要图片尺寸为2的幂。

--  对于不符合规格的图片，可以
--  1.local size = _mf:getImageSize("xxx.xxx")。             -- 获取原尺寸
--  2._mf:resizeImagePowerOfTwo("xxx.xxx", "xxx.xxx") -- 拉伸至符合规格的最小尺寸
--  3.compressImageToETC(...)
--  4._mf:addImageHeader("xxx.xxx", size.width, size.height)-- 写入原始尺寸

-- 以a.jpg为例，目标目录textures，压缩命令为etcpack a.jpg textures -c etc1，会生成压缩过的文件a.pkm。
-- 若源图片带alpha通道，加上-as选项，etcpack a.jpg textures -c etc1 -as，会额外生成压缩的alpha通道文件a_alpha.pkm。

-- 对于分为rgb和alpha两个文件的图片加载，引擎自动识别的规则为：
-- 加载[name].[ext]图片同时会去加载[name]-alpha.[ext]的图片作为alpha通道。
-- 例： a.jpg -> a-alpha.jpg。后缀名需相同。

-- 详细指令用etcpack --help来获取.



etcingnore = {}

_sys:enumFile(tools[1].path..'/res', true, function(f)
    local fullfilename = tools[1].path .. '/res/' .. f
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
                        etcingnore[_sys:getFileName(img.resname, true, false)] = true
                    end
                end
            end
        end
    else
        if msh.isColorKey then
            for ii = 0, 3 do
                local img = msh:getTexture(ii)
                if img then
                    etcingnore[_sys:getFileName(img.resname, true, false)] = true
                end
            end
        end
    end
end)

for k,v in pairs(etcingnore) do
    print(k,v)
end

_sys:getFileName(i, false, true)

fileNum = 0
jumpNum = 0
_sys:enumFile(tools[1].path..'/res', true, function(f)
    fileNum = fileNum + 1
    extname = _sys:getExtention(f)
    fullfilename = tools[1].path .. '/res/' .. f

    local currName = _sys:getFileName(f, true, false)
    if etcingnore[currName] then 
        print('etcingnore---->>>>--', currName, jumpNum)
        jumpNum = jumpNum + 1
        return 
    end

    if extname:find('san$') then
        print('san--->', fileNum, fullfilename, jumpNum)
        -- _mf:optimizeSkeletonAnimation(fullfilename) -- 优化动画资源
    elseif extname:find('skn$') or f:find('msh$') then
        print('skn--->', fileNum, fullfilename, jumpNum)
        _mf:optimizeMesh(fullfilename) -- 优化模型资源
    end

    if extname:find("tga$") or extname:find("bmp$") then
        local size = _mf:getImageSize(fullfilename)             -- 获取原尺寸
        if size.width < 8 and size.height < 8 then
            print('Image size too little ----------->', currName, size.width, size.height)
            return
        end
        -- print('img--->', fileNum, fullfilename, jumpNum)
        local filename = _sys:getFileName(fullfilename, false, true)
        local name = _sys:getFileName(fullfilename, false, false)
        _mf:resizeImage(fullfilename, fullfilename, imgScale, imgScale); -- 缩小图片尺寸为1/4
        local size = _mf:getImageSize(fullfilename)             -- 获取原尺寸
        _mf:resizeImagePowerOfTwo(fullfilename, fullfilename, true) -- 拉伸至符合规格的最小尺寸

        if _mf:isAlphaImage(fullfilename) then
            command = string.format("etcpack %s . -c etc1 -as", fullfilename)
        else
            command = string.format("etcpack %s . -c etc1", fullfilename)
        end

        _sys:command(command, true, false)
        
        _sys:moveFile(name .. ".pkm", fullfilename)
        _mf:addImageHeader(fullfilename, size.width, size.height)-- 写入原始尺寸

        local fromAlpha = name .. "_alpha.pkm"
        local toAlpha = filename .. "-alpha." .. extname
        if _sys:fileExist(fromAlpha) then
            _sys:moveFile(fromAlpha, toAlpha)
            _mf:addImageHeader(toAlpha, size.width, size.height)-- 写入原始尺寸
        end
    end
end)

-- ETCPACK v4.0.1 for ETC and ETC2
-- Compresses and decompresses images using Ericsson Texture Compression (ETC)
--            version 1.0 and 2.0.

-- Usage:
--     etcpack <input_filename> <output_directory> [Options]
-- Options:
--       -s {fast|slow}                     Compression speed. Slow = exhaustive
--                                          search for optimal quality
--                                          (default: fast).
--       -e {perceptual|nonperceptual}      Error metric: Perceptual (nicest) or
--                                          nonperceptual (highest PSNR)
--                                          (default: perceptual).
--       -c {etc1|etc2}                     Codec: etc1 (most compatible) or
--                                          etc2 (highest quality)
--                                          (default: etc2).
--       -f {R|R_signed|RG|RG_signed|       Compressed format: one, two, three
--           RGB|RGBA1|RGBA8 or RGBA}       or four channels, and 1 or 8 bits
--                                          for alpha (1 equals punchthrough)
--                                          (default: RGB).
--       -mipmaps                           Generate mipmaps.
--       -ext {PPM|PGM|JPG|JPEG|PNG|GIF|    Uncompressed formats
--             BMP|TIF|TIFF|PSD|TGA|RAW|    (default PPM).
--             PCT|SGI|XPM}
--       -ktx                               Output ktx files, not pkm files.
--       -v                                 Verbose mode. Prints additional
--                                          information during execution.
--       -progress                          Prints compression progress.
--       -version                           Prints version number.

-- Options to be used only in conjunction with etc codec (-c etc):
--       -aa                                Use alpha channel and create a
--                                          texture atlas.
--       -as                                Use alpha channel and create a
--                                          separate image.
--       -ar                                Use alpha channel and create a
--                                          raw image.

-- Examples:
--   etcpack img.ppm myImages               Compresses img.ppm to myImages\img.pkm
--                                          in ETC2 RGB format.
--   etcpack img.ppm myImages -ktx          Compresses img.ppm to myImages\img.ktx
--                                          in ETC2 RGB format.
--   etcpack img.pkm myImages               Decompresses img.pkm to
--                                          myImages\img.ppm.
--   etcpack img.ppm myImages -s slow       Compress img.ppm to myImages\img.pkm
--                                          using the slow mode.
--   etcpack img.tga MyImages -f RGBA       Compresses img.tga to MyImages\img.pkm
--                                          using etc2 + alpha.
--   etcpack img.ppm MyImages  -f RG        Compresses red and green channels of
--                                          img.ppm to MyImages\img.pkm.
--   etcpack img.pkm MyImages -ext JPG      Decompresses img.pkm to
--                                          MyImages\img.jpg.
--   etcpack orig.ppm images\copy.ppm -p    Calculate PSNR between orig.ppm and
--                                          images\copy.ppm.
--                                          Instead of output directory a full
--                                          file path is given as a second
--                                          parameter.

