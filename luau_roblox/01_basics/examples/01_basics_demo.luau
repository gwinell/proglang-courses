-- Урок 2. Примеры основ Luau.
-- Скопируй файл в один Script в ServerScriptService и открой Output.
-- do ... end здесь только отделяет независимые примеры друг от друга.
-- В тексте урока каждый пример можно запускать отдельно без этой оболочки.

-- Пример: hello
do
    print("Привет, исследователь!")
end

-- Пример: variables
do
    local coins = 10
    print(coins)

    coins = coins + 5
    print(coins)
end

-- Пример: types
do
    local playerName = "Аня"
    local coins = 10
    local hasKey = false
    local selectedItem = nil

    print(type(playerName))
    print(type(coins))
    print(type(hasKey))
    print(type(selectedItem))
    print(type("10"))
end

-- Пример: arithmetic
do
    local price = 8
    local quantity = 3
    local payment = 30
    local total = price * quantity
    local change = payment - total

    print(total)
    print(change)
    print(8 % 3)
    print(2 ^ 3)
    print((2 + 3) * 4)
end

-- Пример: strings
do
    local playerName = "Аня"
    local coins = 15

    print("Игрок: " .. playerName)
    print("Монеты: " .. tostring(coins))
end

-- Пример: comparisons
do
    local coins = 10

    print(coins == 10)
    print(coins > 10)
    print(coins >= 10)
    print(coins ~= 10)
end

-- Пример: logic
do
    local level = 5
    local hasKey = true
    local isBanned = false

    print(level >= 5 and hasKey)
    print(level >= 10 or hasKey)
    print(not isBanned)
end

-- Пример: branch
do
    local coins = 10
    local price = 10

    if coins >= price then
        print("Покупка доступна")
    else
        print("Монет недостаточно")
    end
end

-- Пример: elseif
do
    local score = 75

    if score >= 90 then
        print("Золотая награда")
    elseif score >= 60 then
        print("Серебряная награда")
    else
        print("Продолжай тренировку")
    end
end

-- Пример: truthiness
do
    local coins = 0

    if coins then
        print("Число 0 считается истинным")
    end

    if coins > 0 then
        print("Есть монеты")
    else
        print("Монет нет")
    end
end

-- Пример: for_count
do
    for count = 1, 3 do
        print(count)
    end
end

-- Пример: accumulator
do
    local total = 0

    for round = 1, 3 do
        total = total + 2
        print(total)
    end

    print("Итог: " .. tostring(total))
end

-- Пример: for_step
do
    for number = 2, 6, 2 do
        print(number)
    end

    for count = 3, 1, -1 do
        print("Старт через " .. tostring(count))
    end
end

-- Пример: while_charge
do
    local energy = 0

    while energy < 6 do
        energy = energy + 2
        print(energy)
    end

    print("Зарядка завершена")
end

-- Пример: repeat
do
    local attempt = 0

    repeat
        attempt = attempt + 1
        print(attempt)
    until attempt >= 2
end

-- Пример: greeting
do
    local function greet(playerName)
        print("Привет, " .. playerName .. "!")
    end

    greet("Аня")
    greet("Борис")
end

-- Пример: return
do
    local function calculateCost(price, quantity)
        local cost = price * quantity
        return cost
    end

    local total = calculateCost(8, 3)
    print(total)
    print(total + 5)
    print(type(calculateCost))
end

-- Пример: scope_update
do
    local coins = 10

    if true then
        coins = coins + 5
    end

    print(coins)
end

-- Пример: scope_shadow
do
    local coins = 10

    if true then
        local coins = 99
        print(coins)
    end

    print(coins)
end

-- Пример: scope_function
do
    local function addReward(balance, reward)
        local newBalance = balance + reward
        return newBalance
    end

    local coins = 10
    coins = addReward(coins, 5)
    print(coins)
end
