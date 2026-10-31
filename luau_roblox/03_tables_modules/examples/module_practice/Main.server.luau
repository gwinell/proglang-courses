local Greeting = require(script.Parent.Greeting)
local sameGreeting = require(script.Parent.Greeting)

print(Greeting.makeMessage("Аня"))
print(Greeting == sameGreeting)
