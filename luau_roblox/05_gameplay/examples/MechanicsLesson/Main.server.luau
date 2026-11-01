local Players = game:GetService("Players")
local GameRules = require(script.Parent.GameRules)
local World = require(script.Parent.World)

local DAMAGE = 25
local DAMAGE_COOLDOWN = 1.5
local COIN_REWARD = 5
local COIN_RESPAWN = 4
local HEAL_AMOUNT = 30
local MEDKIT_RESPAWN = 6

if workspace:FindFirstChild("Lesson05Mechanics") ~= nil then
    warn("Lesson05Mechanics уже существует. Оставь одну копию Main.")
    return
end

local world = World.create()
local sessions = {}

local function publishStats(session)
    session.coinsStat.Value = session.state.coins
    session.stageStat.Value = session.state.stage
end

local function setupPlayer(player)
    if sessions[player] ~= nil then
        return
    end
    if player:FindFirstChild("leaderstats") ~= nil then
        warn("У игрока уже есть leaderstats. Отключи прежние учебные Script.")
        return
    end

    local stats = Instance.new("Folder")
    stats.Name = "leaderstats"
    local coinsStat = Instance.new("IntValue")
    coinsStat.Name = "Coins"
    coinsStat.Value = 0
    coinsStat.Parent = stats
    local stageStat = Instance.new("IntValue")
    stageStat.Name = "Stage"
    stageStat.Value = 0
    stageStat.Parent = stats

    sessions[player] = {state = GameRules.newSession(), coinsStat = coinsStat, stageStat = stageStat}
    player.RespawnLocation = world.start
    stats.Parent = player
end

local function removePlayer(player)
    sessions[player] = nil
end

Players.PlayerAdded:Connect(setupPlayer)
Players.PlayerRemoving:Connect(removePlayer)
for index, player in Players:GetPlayers() do
    setupPlayer(player)
end

local function findContact(hit)
    local object = hit
    while object ~= nil do
        if object:IsA("Model") then
            local player = Players:GetPlayerFromCharacter(object)
            if player ~= nil then
                local humanoid = object:FindFirstChildOfClass("Humanoid")
                if humanoid ~= nil and humanoid.Health > 0 then
                    return {player = player, humanoid = humanoid}
                end
                return nil
            end
        end
        object = object.Parent
    end
    return nil
end

local function onHazardTouched(hit)
    local contact = findContact(hit)
    if contact == nil then
        return
    end
    local session = sessions[contact.player]
    if session == nil then
        return
    end
    if GameRules.tryDamage(session.state, os.clock(), DAMAGE_COOLDOWN) then
        contact.humanoid:TakeDamage(DAMAGE)
    end
end
world.hazard.Touched:Connect(onHazardTouched)

local function connectCoin(coin)
    local available = true

    local function restoreCoin()
        if coin.Parent ~= nil then
            coin.Transparency = 0
            available = true
        end
    end

    local function onTouched(hit)
        if not available then
            return
        end
        local contact = findContact(hit)
        if contact == nil then
            return
        end
        local session = sessions[contact.player]
        if session == nil then
            return
        end

        available = false
        coin.Transparency = 1
        GameRules.addCoins(session.state, COIN_REWARD)
        publishStats(session)
        task.delay(COIN_RESPAWN, restoreCoin)
    end

    coin.Touched:Connect(onTouched)
end

for index, coin in world.coins do
    connectCoin(coin)
end

local function connectCheckpoint(entry)
    local function onTouched(hit)
        local contact = findContact(hit)
        if contact == nil then
            return
        end
        local session = sessions[contact.player]
        if session ~= nil and GameRules.advanceCheckpoint(session.state, entry.stage) then
            contact.player.RespawnLocation = entry.spawn
            publishStats(session)
        end
    end
    entry.spawn.Touched:Connect(onTouched)
end

for index, entry in world.checkpoints do
    connectCheckpoint(entry)
end

local currentMedkit = nil
local function spawnMedkit()
    if currentMedkit ~= nil or world.root.Parent == nil then
        return
    end

    local item = Instance.new("Part")
    item.Name = "Medkit"
    item.Size = Vector3.new(2, 2, 2)
    item.Position = world.medkitPosition
    item.Anchored = true
    item.CanCollide = false
    item.CanTouch = true
    item.Color = Color3.fromRGB(15, 180, 90)
    item.Material = Enum.Material.Neon
    local collected = false

    local function onTouched(hit)
        if collected then
            return
        end
        local contact = findContact(hit)
        if contact == nil or sessions[contact.player] == nil then
            return
        end
        local humanoid = contact.humanoid
        if humanoid.Health >= humanoid.MaxHealth then
            return
        end

        collected = true
        humanoid.Health = GameRules.calculateHealedHealth(humanoid.Health, humanoid.MaxHealth, HEAL_AMOUNT)
        item:Destroy()
        currentMedkit = nil
        task.delay(MEDKIT_RESPAWN, spawnMedkit)
    end

    item.Touched:Connect(onTouched)
    currentMedkit = item
    item.Parent = world.root
end

spawnMedkit()
print("Механики готовы: Coins, Stage, Hazard, Medkit")
