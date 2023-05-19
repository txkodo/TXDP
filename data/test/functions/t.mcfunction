data modify storage : _.hcxZvcxKY set value "hello"
data modify storage : _.MAy3QoUKy set value ["hello"]
data modify storage : _.08iT6tDNX set from storage : _.hcxZvcxKY
execute if data storage : _{08iT6tDNX:"hello"} run say true
data modify storage : _.DHmoelW2Y set from storage : _.MAy3QoUKy[0]
execute if data storage : _{DHmoelW2Y:"hello"} run say true
data modify storage : _.58EUmVEYC set from storage : _.hcxZvcxKY
execute store success storage : _.wGzyJNiKO byte 1 run data modify storage : _.58EUmVEYC set from storage : _.hcxZvcxKY
execute if data storage : _{wGzyJNiKO:0b} run say true
data remove storage : _.wGzyJNiKO
data remove storage : _.hcxZvcxKY
data remove storage : _.58EUmVEYC
data remove storage : _.08iT6tDNX
data remove storage : _.DHmoelW2Y
data remove storage : _.MAy3QoUKy