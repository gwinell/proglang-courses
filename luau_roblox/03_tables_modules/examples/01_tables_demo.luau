-- Урок 3. Независимые примеры таблиц.
-- do ... end отделяет локальные переменные каждого примера.

print("--- empty_table ---")
do
    local inventory = {}
    print(type(inventory))
end

print("--- array_read ---")
do
    local dialogue = {"Привет!", "Как дела?", "До встречи!"}

    print(dialogue[1])
    print(dialogue[3])
    print(#dialogue)
end

print("--- array_change ---")
do
    local items = {"Карта", "Факел", "Верёвка"}
    local slot = 2

    items[slot] = "Компас"
    print(items[2])
    print(#items)
end

print("--- array_insert_remove ---")
do
    local items = {"Карта", "Факел"}

    table.insert(items, "Верёвка")
    table.insert(items, 2, "Компас")
    local removed = table.remove(items, 3)

    print("Убрали: " .. removed)
    print(items[1])
    print(items[2])
    print(items[3])
    print(#items)
end

print("--- numeric_iteration ---")
do
    local items = {"Карта", "Факел", "Верёвка"}

    for index = 1, #items do
        print(tostring(index) .. ": " .. items[index])
    end
end

print("--- generalized_iteration ---")
do
    local items = {"Карта", "Факел", "Верёвка"}

    for index, item in items do
        print(tostring(index) .. ": " .. item)
    end
end

print("--- array_sum ---")
do
    local rewards = {4, 7, 3}
    local total = 0

    for index, reward in rewards do
        total = total + reward
        print("После " .. tostring(index) .. ": " .. tostring(total))
    end

    print("Итог: " .. tostring(total))
end

print("--- dictionary_read ---")
do
    local stock = {
        potion = 2,
        rope = 0,
    }

    print(stock.potion)
    print(stock["rope"])

    local itemId = "potion"
    print(stock[itemId])
    print(stock["shield"])
end

print("--- dictionary_change ---")
do
    local stock = {potion = 2, rope = 0}

    stock.potion = stock.potion + 1
    stock.torch = 5
    stock.rope = nil

    print(stock.potion)
    print(stock.torch)
    print(stock.rope)
end

print("--- dictionary_presence ---")
do
    local settings = {soundEnabled = false}

    if settings.soundEnabled ~= nil then
        print("Настройка существует")
    end

    if settings.soundEnabled then
        print("Звук включён")
    else
        print("Звук выключен")
    end
end

print("--- dictionary_iteration ---")
do
    local stock = {potion = 2, rope = 3}

    for itemId, amount in stock do
        print(itemId .. ": " .. tostring(amount))
    end
end

print("--- dictionary_count ---")
do
    local stock = {potion = 2, rope = 0, torch = 5}
    local kinds = 0
    local total = 0

    for itemId, amount in stock do
        kinds = kinds + 1
        total = total + amount
    end

    print("Видов: " .. tostring(kinds))
    print("Всего: " .. tostring(total))
end

print("--- ordered_dictionary ---")
do
    local stock = {potion = 2, rope = 0, torch = 5}
    local order = {"rope", "potion", "torch"}

    for index, itemId in order do
        print(itemId .. ": " .. tostring(stock[itemId]))
    end
end

print("--- records ---")
do
    local players = {
        {name = "Аня", coins = 10},
        {name = "Борис", coins = 7},
    }

    print(players[1].name)

    local total = 0
    for index, player in players do
        total = total + player.coins
    end

    print(total)
end

print("--- table_alias ---")
do
    local backpack = {"Карта", "Факел"}
    local sameBackpack = backpack

    sameBackpack[1] = "Компас"

    print(backpack[1])
    print(backpack == sameBackpack)
end

print("--- table_clone ---")
do
    local backpack = {"Карта", "Факел"}
    local copy = table.clone(backpack)

    copy[1] = "Компас"

    print(backpack[1])
    print(copy[1])
    print(backpack == copy)
end

print("--- shallow_clone ---")
do
    local original = {coins = 10, items = {"Карта"}}
    local copy = table.clone(original)

    copy.coins = 99
    copy.items[1] = "Компас"

    print(original.coins)
    print(original.items[1])
    print(original.items == copy.items)
end
