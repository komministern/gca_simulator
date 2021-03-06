
ExportScript.Tools = {}
--ExportScript.Version.Tools = "1.1.1"


function ExportScript.Tools.split(inputstr, sep)
    if sep == nil then
        sep = "%s"
    end
    local t={} ; i=1
    for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
        t[i] = str
        i = i + 1
    end
    return t
end

function ExportScript.Tools.tablelength(T)
    local count = 0
    for _ in pairs(T) do count = count + 1 end
    return count
end
