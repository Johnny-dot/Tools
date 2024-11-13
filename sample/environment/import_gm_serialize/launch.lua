function _G.serialize (o, s)
    if not s then
        s = ''
    end

    if type(o) == "number" then
        s = s..o;
    elseif type(o) == "string" then
        s = s..'"'..o..'"';
    elseif type(o) == "boolean" then
        s = s..(o and "true" or "false");
    elseif type(o) == "table" then
        s = s.."{";
        local dot = ""
        for k, v in next, o do
            s = s..dot

            if type(k) == 'number' then
                s = s.."["..k.."]=";
                s = serialize(v, s);
            elseif type(k) == 'string' then
                s = s.."['"..k.."']=";
                s = serialize(v, s);
            elseif type(k) == "boolean" then
                s = s.."[" .. (k and "true" or "false") .. "]=";
                s = serialize(v, s);
            end

            if "" == dot then
                dot = ","
            end
        end
        s = s.."}";
    elseif type(o) == "function" then
        --  print( "ignor" );
    elseif type(o) == "userdata" then
        --  print( "ignor" );
    else
        -- print( "ignor" );
        -- error("cannot serialize a " .. type(o))
    end
    return s
end

_G.unserializeT = nil
function _G.unserialize(s, o)
    if not o then
        o = {}
    end

    local can = pcall(loadstring('_G.unserializeT = ' .. s))
    if not can then _G.unserializeT = {} end

    -- loadstring('_G.unserializeT = ' .. s)()

    return _G.unserializeT
end

function _G.dump(o, indent)
    if not indent then indent = "" end
    if type(o) == "table" then
        local s = "{\n"
        for k, v in pairs(o) do
            local key
            if type(k) == "number" then
                key = "[" .. k .. "]"
            else
                key = '["' .. tostring(k) .. '"]'
            end
            s = s .. indent .. "  " .. key .. " = " .. dump(v, indent .. "  ") .. ",\n"
        end
        return s .. indent .. "}"
    else
        return tostring(o)
    end
end

function _G.doSerialize(tb, fn)
    local s = _G.serialize(tb)

    local fn_out = string.format("output/serialize_%s.txt", fn)
    -- 将 s 保存到一个 txt 文件中
    local file = io.open(fn_out, "w") -- 以写模式打开文件
    file:write(s) -- 写入字符串 s
    file:close() -- 关闭文件

    -- 从文件中读取序列化的字符串
    local file = io.open(fn_out, "r") -- 以读模式打开文件
    local content = file:read("*a") -- 读取文件的全部内容
    file:close() -- 关闭文件

    -- 反序列化字符串为表
    local new_tb = _G.unserialize(content)

    print(string.format("%s-序列化成功", fn))
end

local function listFilesInDirectory(directory)
    for fn, str in pairs(io.dir(directory)) do  -- 遍历目录中的文件
        local tb = dofile(string.format("%s/%s", directory, fn))
        _G.doSerialize(tb, fn)
    end
end

listFilesInDirectory("input")
os.exit( )
