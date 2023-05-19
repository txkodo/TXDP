scoreboard players set aGCG9RZ2L _ 1
scoreboard players set n1cpc3wLV _ 1
execute if score aGCG9RZ2L _ matches 10 run say true
execute unless score aGCG9RZ2L _ matches 10.. run say true
execute if score aGCG9RZ2L _ matches ..10 run say true
execute unless score aGCG9RZ2L _ matches ..10 run say true
execute if score aGCG9RZ2L _ matches 10.. run say true
execute if score aGCG9RZ2L _ = n1cpc3wLV _ run say true
execute if score aGCG9RZ2L _ < n1cpc3wLV _ run say true
execute if score aGCG9RZ2L _ <= n1cpc3wLV _ run say true
execute if score aGCG9RZ2L _ > n1cpc3wLV _ run say true
execute if score aGCG9RZ2L _ >= n1cpc3wLV _ run say true
execute if score aGCG9RZ2L _ matches 1..100 run say true
say true
scoreboard players reset aGCG9RZ2L _
scoreboard players reset n1cpc3wLV _