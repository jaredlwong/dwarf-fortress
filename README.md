# dwarf-fortress
Dwarf Fortress Scripts and Configs

`df.global.world.raws.plants.all`: All plants

All plantable plants:
  ```lua
  for k, v in pairs(df.global.world.raws.plants.all) do
    print(v.id, v.flags.SEED, v.flags.TREE)
  end
```

