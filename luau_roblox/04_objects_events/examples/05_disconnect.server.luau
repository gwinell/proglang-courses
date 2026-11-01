local part = Instance.new("Part")
part.Name = "Lesson04Signal"
part.Anchored = true
part.Position = Vector3.new(0, 3, -10)
part.Color = Color3.fromRGB(37, 99, 235)
part.Parent = workspace

local calls = 0
local function onColorChanged()
    calls = calls + 1
    print("Цвет изменился")
end

local connection = part:GetPropertyChangedSignal("Color"):Connect(onColorChanged)

part.Color = Color3.fromRGB(15, 138, 104)
task.wait(0.1)

connection:Disconnect()
print(connection.Connected)

part.Color = Color3.fromRGB(220, 70, 70)
task.wait(0.1)
print(calls)
