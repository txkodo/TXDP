scoreboard players set sHRFz39L7 _ 1
scoreboard players set q05zdaeQX _ 1
execute if score sHRFz39L7 _ matches 10 run say true
execute unless score sHRFz39L7 _ matches 10.. run say true
execute if score sHRFz39L7 _ matches ..10 run say true
execute unless score sHRFz39L7 _ matches ..10 run say true
execute if score sHRFz39L7 _ matches 10.. run say true
execute if score sHRFz39L7 _ = q05zdaeQX _ run say true
execute if score sHRFz39L7 _ < q05zdaeQX _ run say true
execute if score sHRFz39L7 _ <= q05zdaeQX _ run say true
execute if score sHRFz39L7 _ > q05zdaeQX _ run say true
execute if score sHRFz39L7 _ >= q05zdaeQX _ run say true
execute if score sHRFz39L7 _ matches 1..100 run function _/3foopglbivuhdcl9
execute store result score sHRFz39L7 _ if score sHRFz39L7 _ matches 1..100
say true
scoreboard players reset sHRFz39L7 _
scoreboard players reset q05zdaeQX _