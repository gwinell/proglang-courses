local World = {}

local function createPart(parent, name, size, position, color)
    local part = Instance.new("Part")
    part.Name = name
    part.Size = size
    part.Position = position
    part.Anchored = true
    part.CanCollide = true
    part.CanTouch = true
    part.Color = color
    part.Parent = parent
    return part
end

local function createSpawn(parent, name, position, color)
    local spawn = Instance.new("SpawnLocation")
    spawn.Name = name
    spawn.Size = Vector3.new(8, 1, 8)
    spawn.Position = position
    spawn.Anchored = true
    spawn.CanCollide = true
    spawn.CanTouch = true
    spawn.Neutral = true
    spawn.Enabled = true
    spawn.AllowTeamChangeOnTouch = false
    spawn.Duration = 0
    spawn.Color = color
    spawn.Parent = parent
    return spawn
end

local function create()
    local root = Instance.new("Folder")
    root.Name = "Lesson05Mechanics"

    local start = createSpawn(root, "Start", Vector3.new(0, 0.5, 12), Color3.fromRGB(37, 99, 235))
    local checkpoint1 = createSpawn(root, "Checkpoint1", Vector3.new(24, 0.5, 0), Color3.fromRGB(15, 138, 104))
    local checkpoint2 = createSpawn(root, "Checkpoint2", Vector3.new(48, 0.5, 0), Color3.fromRGB(117, 80, 204))
    local hazard = createPart(root, "Hazard", Vector3.new(6, 1, 8), Vector3.new(12, 0.5, 0), Color3.fromRGB(220, 60, 60))

    local coins = {}
    for index, position in {Vector3.new(6, 1.5, -6), Vector3.new(30, 1.5, -6)} do
        local coin = createPart(root, "Coin" .. tostring(index), Vector3.new(2, 2, 2), position, Color3.fromRGB(246, 190, 35))
        coin.Shape = Enum.PartType.Ball
        coin.Material = Enum.Material.Neon
        coin.CanCollide = false
        table.insert(coins, coin)
    end

    createPart(root, "MedkitBase", Vector3.new(4, 0.5, 4), Vector3.new(36, 0.25, 6), Color3.fromRGB(210, 235, 222))
    root.Parent = workspace

    return {
        root = root,
        start = start,
        hazard = hazard,
        checkpoints = {{spawn = checkpoint1, stage = 1}, {spawn = checkpoint2, stage = 2}},
        coins = coins,
        medkitPosition = Vector3.new(36, 1.5, 6),
    }
end

World.create = create
return World
