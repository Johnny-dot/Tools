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
function table.count(t)
	local n = 0
	for k, v in next, t do
		n = n + 1
	end
	return n
end
------------------------
------ 功能实现
------------------------
local i = _sys:getGlobal('i')
local f = _File.new()
f:open('temp-fancy-etc' .. i .. '.txt')
local lines = f:read():split('\n')
print('Fancy2Etc --------------------- start', i, table.count(lines))
for _,cmd in next, lines do if #cmd > 0 then
	print(cmd)
	_sys:command(cmd, true, false)
end end

if i == '8' then
	print('continue or close when another window closed')
else
	print('Fancy2Etc --------------------- done')
end
if i ~= '8' then
	_abort()
end