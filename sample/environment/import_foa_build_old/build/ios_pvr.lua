------------------------
------ lua string.split
------------------------
function string.split(s, delimiter)
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
------------------------
------ 配置
------------------------
local path = 'client_pvr/' -- 资源路径

local opens = { -- 优化开关 true开|false关
	san=false, -- 动画
	sknandmsh=true, -- 骨骼和模型
	pvr=true, -- 转pvr
}
local filereplace = true -- 转换后文件是否替换源文件
local replaceformat = '%s-new' -- 不替换源文件，新文件的命名规则

------------------------
------ 功能实现
------------------------
_sys:command('fancy-res-helper.py pvr-start', true, false)

---- optimize animation
local function optimizeSan()
	if not opens.san then return end
	local function onEnum(f)
		if f:find('san$') then
			_mf:optimizeSkeletonAnimation(path .. f) -- 优化动画资源
		end
	end
	_sys:enumFile(path, true, onEnum)
end
optimizeSan()

---- optimize skeleton and mesh
local function optimizeSknAndMsh()
	if not opens.sknandmsh then return end
	local function onEnum(f)
		if f:find('skn$') or f:find('msh$') then
			_mf:optimizeMesh(path .. f) -- 优化模型资源
		end
	end
	_sys:enumFile(path, true, onEnum)
end
optimizeSknAndMsh()

---- convert pvr
-- to pvr
local exclude = 'gundongziti.tga$'
local function toPvr()
	if not opens.pvr then return end
	local pvrf = _File.new() pvrf:create('temp-pvr.txt')
	local bsf = _File.new() bsf:create('temp-backsize-pvr.txt')
	local pvrs, resizes = '', ''
	local bpp = 4 -- bpp[int]:每个像素占用的空间(2/4)
	local genmip = true -- genmip[bool]:是否生成mipmap
	local function onEnum(f)
		if (f:find("tga$") or f:find("bmp$") or f:find("jpg$")) and not f:find(exclude) then
			local fin = _String.replace(path .. f, '\\', '/')
			local fname = _sys:getFileName(fin, false, true)
			local fout = filereplace and ('%s.%s'):format(fin, _sys:getExtention(f)) or (replaceformat):format(fname..'.pvr')
			local size = _mf:getImageSize(fin)
			resizes = ('%s%d|%d|%s|%s\n'):format(resizes, size.width, size.height, fout, fin)
			-- if #resizes > 102400 then
				-- bsf:write(resizes) resizes = ''
			-- end
			_mf:resizeImagePowerOfTwo(fin, fin, true) -- 拉伸至符合规格的最小尺寸
			-- _mf:resizeImage(fin, fin, 0.5, 0.5) -- 缩小图片至1/2
			pvrs = ('%sPVRTexTool.exe -silent -foglpvrtc%d -pvrtciterations8 -yflip0 %s -i \"%s\" -o \"%s\"\n'):format(pvrs, bpp, genmip and "-m" or "", fin, fout)
			-- if #pvrs > 102400 then
				-- pvrf:write(pvrs) pvrs = ''
			-- end
		end
	end
	_sys:enumFile(path, true, onEnum)
	pvrf:write(pvrs)
	pvrf:close()
	bsf:write(resizes)
	bsf:close()
	_sys:command('fancy-res-helper.py pvr-run', true, false)
end
toPvr()

-- backsize
local function backsize()
	local f = _File.new()
	f:open 'temp-backsize-pvr.txt'
	local lines = f:read():split('\n')
	for _,line in next, lines do if #line > 0 then
		local s = line:split'|'
		local width, height = tonumber(s[1]), tonumber(s[2])
		local fins, fout = s[3]:split('%.'), s[4]
		local fin = ''
		for i=1, #fins do if i < #fins then
			fin = ('%s%s%s'):format(fin, i == 1 and '' or '.', fins[i])
		end end
		if filereplace then
			_sys:moveFile(fout .. '.pvr', fout)
			_sys:delFile(fout .. '.pvr')
		else
			_sys:moveFile(fin .. '.pvr', fout)
		end
        _mf:addImageHeader(fout, width, height)-- 写入原始尺寸
	end end
end
backsize()

_sys:command('fancy-res-helper.py pvr-done', true, false)
print('============================= DONE =============================')
_abort()