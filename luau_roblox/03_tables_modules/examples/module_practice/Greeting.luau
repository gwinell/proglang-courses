local Greeting = {}

local function makeMessage(playerName)
    return "Привет, " .. playerName .. "!"
end

Greeting.makeMessage = makeMessage

print("Greeting загружен")
return Greeting
