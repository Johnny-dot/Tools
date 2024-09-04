_G.cache = {}
local function getFileMd5(fpath)
    local md5 = _sys:readConfig(fpath):md5()
    return md5
end

local function createCache(source, target)
    local cacheDir = "./cache"
    print("-------start createCache----------")
    _sys:delPath(cacheDir)
    _sys:enumFile(source, true, function(filename)
        local sourceResPath = source .. '/' .. filename
        local targetResPath = target .. '/' .. filename
        if _sys:fileExist(targetResPath) then
            local md5Name = getFileMd5(sourceResPath)
            if _G.cache.cacheLog then
                print("cache", targetResPath, md5Name)
            end
            _sys:copyFile(targetResPath, cacheDir .. '/' .. md5Name)
        end
    end)
    print("················end createCache···············")
end

local function useSingleCache( ... )
    -- body
end

local function useCache(source,path)
    --如果path文件夹下文件md5存在索引 就使用cache替换
    if not _G.cache.isUseCache then return end
    local cacheDir = "./cache"
    local cacheFiles = {}
    print("-------start useCache----------")
    _sys:enumFile(path, true, function(filename)
        local resPath = path .. '/' .. filename
        local md5Name = getFileMd5(resPath)
        local md5File = cacheDir .. "/" .. md5Name
        if _sys:fileExist(md5File) then
            if _G.cache.cacheLog then
                print("usecache:" .. filename, md5Name)
            end
            cacheFiles[filename] = true
            _sys:copyFile(md5File, resPath)
        end
    end)
    print("················end useCache··················")
    _G.cache.cacheFiles = cacheFiles
    return cacheFiles
end

_G.cache = {
    getFileMd5 = getFileMd5,
    createCache = createCache,
    useCache = useCache,
}
