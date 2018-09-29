
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

function ExportScript.Tools.toDegMinSec(inputstr)
    temp = ExportScript.Tools.split(inputstr, '.')
    deg = temp[1]
    dec = temp[2]
    min = math.floor(tonumber('0.'..dec) * 60)
    sec = (tonumber('0.'..dec) - min/60) * 3600
    return deg.."'"..tostring(min).."'"..string.format("%." .. (4) .. "f", sec)
end

