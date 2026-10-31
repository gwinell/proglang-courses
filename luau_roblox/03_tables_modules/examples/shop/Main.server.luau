local Catalog = require(script.Parent.Catalog)
local CartMath = require(script.Parent.CartMath)

local cart = {
    {itemId = "potion", quantity = 2},
    {itemId = "rope", quantity = 1},
}
local coins = 30

local total = CartMath.calculateTotal(cart, Catalog)

if total == nil then
    print("Ошибка: неизвестный товар")
else
    print("Стоимость: " .. tostring(total))
    if coins >= total then
        print("Покупка доступна")
        print("Останется: " .. tostring(coins - total))
    else
        print("Не хватает: " .. tostring(total - coins))
    end
end
