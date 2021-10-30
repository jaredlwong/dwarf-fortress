# dwarf-fortress
Dwarf Fortress Scripts and Configs

**df:**
Get all type defs in global `df` that are an enum or bitfield
```lua
for k, v in dfpairs(df) do
  if v._kind == 'bitfield-type' or v._kind == 'enum-type' then
    print(k, v._kind)
  end
end
```

Choose appropriate iterator based on `_kind`
```lua
function dfpairs(t)
  if t._kind == 'bitfield-type' or t._kind == 'enum-type' then
    return ipairs(t)
  elseif t._kind == 'struct-type' then
    return orderedpairs(t)
  end
  return orderedpairs(t)
end
```

```printall(obj)

If the argument is a lua table or DF object reference, prints all fields.

printall_recurse(obj)

If the argument is a lua table or DF object reference, prints all fields recursively.```

**Plants:**
* All plant definitions
  * `df.global.world.raws.plants.all`
  * `gui/gm-editor df.global.world.raws.plants.all`
* 

All plantable plants:
  ```lua
  for k, v in pairs(df.global.world.raws.plants.all) do
    print(v.id, v.flags.SEED, v.flags.TREE)
  end
```

**Jobs:**

active jobs
```lua
local utils = require 'utils'

local function getUnitName(unit)
  local language_name = dfhack.units.getVisibleName(unit)
  if language_name.has_name then
    return dfhack.df2console(dfhack.TranslateName( language_name ))
  end
  -- animals
  return dfhack.units.getProfessionName(unit)
end

for _link, job in utils.listpairs(df.global.world.jobs.list) do
  local building = dfhack.job.getHolder(job)
  local unit = dfhack.job.getWorker(job)
  print(dfhack.job.getName(job),
        job.flags.do_now,
        building and utils.getBuildingName(building),
        unit and getUnitName(unit))
end
```

job types
```lua
for k, v in ipairs(df.job_type) do
  print(k, v)
end
```


**Utils:**
* <https://github.com/DFHack/dfhack/blob/develop/library/lua/utils.lua>

**Dreamfort:**
* <https://github.com/DFHack/dfhack/blob/master/data/examples/init/onMapLoad_dreamfort.init>

**Plugins:**
* <https://docs.dfhack.org/en/stable/docs/Plugins.html>

**All Scripts:**
* <https://docs.dfhack.org/en/stable/docs/Scripts.html>

**Basic Scripts:**
* <https://docs.dfhack.org/en/stable/docs/_auto/base.html>

**GUI Scripts:**
* <https://docs.dfhack.org/en/stable/docs/_auto/gui.html>
* `gui/gm-editor`

**Devel Scripts:**
* <https://docs.dfhack.org/en/stable/docs/_auto/devel.html>
* <https://docs.dfhack.org/en/stable/docs/_auto/devel.html#devel-send-key>

**Scripts for Modders:**
* <https://docs.dfhack.org/en/stable/docs/_auto/modtools.html>

**Bugfix Scripts:**
* <https://docs.dfhack.org/en/stable/docs/_auto/fix.html>

**Lua:**
* https://docs.dfhack.org/en/stable/docs/Lua%20API.html


```lua
-- If we want to sort the table by the field name, in reverse alphabetical order, we just write this:
-- orderedpairs(table, function (a,b) return (a.name > b.name) end)
-- for k, v in orderedpairs(table, orderfunc) do print(k, v) end
local function orderedpairs(t, f)
  local keys = {}
  for k in pairs(t) do
    keys[#keys + 1] = k
  end
  table.sort(keys, f)
  local i = 0
  return function ()
    i = i + 1
    if i > #keys then
      return nil
    end
    return keys[i], t[keys[i]]
  end
end
```
