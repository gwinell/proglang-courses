local pad = Instance.new("Part")
pad.Name = "Lesson04TouchPad"
pad.Size = Vector3.new(8, 1, 8)
pad.Position = Vector3.new(0, 1, -12)
pad.Anchored = true
pad.CanCollide = true
pad.CanTouch = true
pad.Color = Color3.fromRGB(37, 99, 235)
pad.Parent = workspace

local busy = false

local function onTouched(otherPart)
    if busy then
        return
    end

    local character = otherPart.Parent
    if character == nil then
        return
    end
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if humanoid == nil then
        return
    end

    busy = true
    pad.Color = Color3.fromRGB(15, 138, 104)
    print("Контакт персонажа")
    task.wait(2)
    pad.Color = Color3.fromRGB(37, 99, 235)
    busy = false
end

pad.Touched:Connect(onTouched)
print("Площадка готова")
