-- ETC压缩。

-- 压缩工具 etcpack.exe。

-- ETC部分机型需要图片尺寸为2的幂。

--  对于不符合规格的图片，可以

--  1.local size = _mf:getImageSize("xxx.xxx")。       -- 获取原尺寸

--  2._mf:resizeImagePowerOfTwo("xxx.xxx", "xxx.xxx") -- 拉伸至符合规格的最小尺寸

--  3.compressImageToETC(...)

--  4._mf:addImageHeader("xxx.xxx", size.width, size.height)-- 写入原始尺寸

-- 以a.jpg为例，目标目录textures，压缩命令为etcpack a.jpg textures -c etc1，会生成压缩过的文件a.pkm。

-- 若源图片带alpha通道，加上-as选项，etcpack a.jpg textures -c etc1 -as，会额外生成压缩的alpha通道文件a_alpha.pkm。

-- 对于分为rgb和alpha两个文件的图片加载，引擎自动识别的规则为：

-- 加载[name].[ext]图片同时会去加载[name]-alpha.[ext]的图片作为alpha通道。

-- 例： a.jpg -> a-alpha.jpg。后缀名需相同。

-- 详细指令用etcpack --help来获取.

```
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
```

