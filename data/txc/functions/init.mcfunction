data remove storage txc _
data modify storage txc _.lED2S0bdH set value 100
data modify storage txc _.WYu5gmasv set from storage txc _.lED2S0bdH
execute if data storage txc _.WYu5gmasv run data modify storage txc _.uNbIdaS8T set value 100
execute unless data storage txc _.WYu5gmasv run function txc/rd6xhw3ym6r098hd
data modify storage txc _.lED2S0bdH set value 102