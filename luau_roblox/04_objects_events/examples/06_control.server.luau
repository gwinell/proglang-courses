if workspace:FindFirstChild("Lesson04Control") ~= nil then
    warn("Lesson04Control уже существует. Оставь один учебный Script.")
    return
end

local root = Instance.new("Folder")
root.Name = "Lesson04Control"

local control = Instance.new("Part")
control.Name = "Control"
control.Size = Vector3.new(4, 2, 3)
control.Position = Vector3.new(0, 1, -10)
control.Anchored = true
control.Color = Color3.fromRGB(37, 99, 235)
control.Parent = root

local prompt = Instance.new("ProximityPrompt")
prompt.Name = "ProximityPrompt"
prompt.ObjectText = "Пульт"
prompt.ActionText = "Создать куб"
prompt.KeyboardKeyCode = Enum.KeyCode.E
prompt.HoldDuration = 0
prompt.MaxActivationDistance = 10
prompt.RequiresLineOfSight = false
prompt.Parent = control

local activeCube = nil
local busy = false

local function createCube()
    local cube = Instance.new("Part")
    cube.Name = "Cube"
    cube.Size = Vector3.new(3, 3, 3)
    cube.Position = Vector3.new(6, 3, -10)
    cube.Anchored = true
    cube.CanCollide = false
    cube.CanTouch = false
    cube.Color = Color3.fromRGB(15, 138, 104)
    cube.Material = Enum.Material.Neon

    local light = Instance.new("PointLight")
    light.Name = "Glow"
    light.Color = cube.Color
    light.Brightness = 2
    light.Range = 12
    light.Parent = cube

    cube.Parent = root
    return cube
end

local function onTriggered(player)
    if busy then
        return
    end
    busy = true
    prompt.Enabled = false

    if activeCube == nil then
        activeCube = createCube()
        prompt.ActionText = "Убрать куб"
        print("Куб создан")
    else
        activeCube:Destroy()
        activeCube = nil
        prompt.ActionText = "Создать куб"
        print("Куб удалён")
    end

    task.wait(1)
    prompt.Enabled = true
    busy = false
end

prompt.Triggered:Connect(onTriggered)
root.Parent = workspace
print("Пульт готов")
