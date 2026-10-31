local CartMath = {}

local function calculateTotal(cart, catalog)
    local total = 0

    for index, line in cart do
        local item = catalog[line.itemId]
        if item == nil then
            return nil
        end
        total = total + item.price * line.quantity
    end

    return total
end

CartMath.calculateTotal = calculateTotal
return CartMath
