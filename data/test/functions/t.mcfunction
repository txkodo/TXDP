data modify storage : _.UxPSy8W2b set value "nagaistring"
data modify storage : _.AqqZ21LVs set from storage : _.UxPSy8W2b
function _/9rxm1wgm92s6coyz
scoreboard players remove nFVbQdS7J _ 1
scoreboard players set 9G6V2M5a7 _ 100
scoreboard players operation 6SMh9zgxt _ = 9G6V2M5a7 _
data modify storage : _.l87jCulzn set value 100
execute store result score X16kAvmJO _ run data get storage : _.l87jCulzn
execute store result storage : _.FWLQleJPa int 0.5 run data get storage : _.98gtbXjCb 2
data remove storage : _.98gtbXjCb
data remove storage : _.l87jCulzn
data remove storage : _.UxPSy8W2b
data remove storage : _.FWLQleJPa
scoreboard players reset 9G6V2M5a7 _
scoreboard players reset 6SMh9zgxt _
scoreboard players reset X16kAvmJO _