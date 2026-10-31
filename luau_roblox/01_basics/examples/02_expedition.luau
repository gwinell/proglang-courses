local playerName = "Аня"
local startCoins = 5
local rounds = 3
local baseReward = 4
local isVip = false
local target = 15

local function calculateReward(base, vip)
    if vip then
        return base * 2
    end
    return base
end

local coins = startCoins
print("Игрок: " .. playerName)

for round = 1, rounds do
    local reward = calculateReward(baseReward, isVip)
    coins = coins + reward
    print("Раунд " .. tostring(round) .. ": " .. tostring(coins))
end

print("Итог: " .. tostring(coins))

if coins >= target then
    print("Цель достигнута")
else
    print("Нужно продолжить")
end
