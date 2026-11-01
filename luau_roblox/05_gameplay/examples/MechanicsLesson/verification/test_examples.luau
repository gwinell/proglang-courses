-- Limited API model: explicit events, no real physics, UI, networking or respawn.
local Model = require("./RobloxModel")
local Sources = require("./Sources")
local Rules = require("../GameRules")
local count = 0
local function check(value, label)
    assert(value, label)
    count = count + 1
end

local function addPlayer(M, name)
    local player = M.Instance.new("Player")
    player.Name = name
    player.Parent = M.players
    local character = M.Instance.new("Model")
    character.Name = name .. "Character"
    character.Parent = M.workspace
    player.Character = character
    local humanoid = M.Instance.new("Humanoid")
    humanoid.Parent = character
    local foot = M.Instance.new("Part"); foot.Name = "Foot"; foot.Parent = character
    local otherFoot = M.Instance.new("Part"); otherFoot.Name = "OtherFoot"; otherFoot.Parent = character
    local accessory = M.Instance.new("Accessory"); accessory.Parent = character
    local handle = M.Instance.new("Part"); handle.Name = "Handle"; handle.Parent = accessory
    return {player = player, humanoid = humanoid, foot = foot, otherFoot = otherFoot, handle = handle, character = character}
end

local function fixture()
    local M = Model.new()
    local a = addPlayer(M, "A")
    local b = addPlayer(M, "B")
    for _, name in {"GameRules", "World"} do
        local module = M.Instance.new("ModuleScript")
        module.Name = name
        module.Source = Sources[name .. ".luau"]
        module.Parent = M.modules
    end
    M.run(Sources["Main.server.luau"])
    return M, a, b, M.workspace.Lesson05Mechanics
end

local function touch(M, part, ...)
    for _, hit in {...} do M.emit(part.Touched, hit) end
    M.advance(0)
end

do
    local a, b = Rules.newSession(), Rules.newSession()
    check(a ~= b and a.coins == 0 and a.stage == 0, "new independent records")
    check(Rules.tryDamage(a, 0, 1.5), "initial damage at zero")
    check(not Rules.tryDamage(a, 1.49, 1.5) and a.nextDamageAt == 1.5, "before boundary, no extension")
    check(Rules.tryDamage(a, 1.5, 1.5) and a.nextDamageAt == 3, "exact boundary")
    check(Rules.tryDamage(b, 0.1, 1.5), "independent player deadline")
    check(Rules.addCoins(a, 5) == 5 and Rules.addCoins(a, 5) == 10 and b.coins == 0, "coin arithmetic independent")
    check(Rules.advanceCheckpoint(a, 2) and a.stage == 2, "skipping stage allowed")
    check(not Rules.advanceCheckpoint(a, 2) and not Rules.advanceCheckpoint(a, 1) and a.stage == 2, "no repeat or rollback")
    check(Rules.calculateHealedHealth(50, 100, 30) == 80, "ordinary heal")
    check(Rules.calculateHealedHealth(95, 100, 30) == 100 and Rules.calculateHealedHealth(100, 100, 30) == 100, "heal clamp")
end

do
    local M, a, b, w = fixture()
    check(#M.output == 1 and M.output[1] == "Механики готовы: Coins, Stage, Hazard, Medkit", "ready output")
    check(a.player.leaderstats.Coins.Value == 0 and b.player.leaderstats.Stage.Value == 0, "initial stats")
    check(a.player.RespawnLocation == w.Start and b.player.RespawnLocation == w.Start, "initial respawn assignment")
    check(w.Checkpoint1.Enabled and w.Checkpoint1.Neutral and w.Checkpoint1.Duration == 0, "eligible training spawn")
    touch(M, w.Hazard, a.foot, a.otherFoot, a.handle, b.foot)
    check(a.humanoid.Health == 75 and b.humanoid.Health == 75, "bodypart repeats rejected; B independent")
    M.advance(1.49); touch(M, w.Hazard, a.foot)
    check(a.humanoid.Health == 75, "early repeated damage rejected")
    M.advance(0.01); touch(M, w.Hazard, a.handle)
    check(a.humanoid.Health == 50, "accessory ancestors and exact boundary")
    local shield = M.Instance.new("ForceField"); shield.Parent = b.character
    touch(M, w.Hazard, b.foot)
    check(b.humanoid.Health == 75, "TakeDamage respects modeled ForceField")
    shield:Destroy(); touch(M, w.Hazard, b.foot)
    check(b.humanoid.Health == 75, "absorbed attempt still consumes deadline")
    local npc = M.Instance.new("Model"); npc.Parent = M.workspace
    local hp = M.Instance.new("Humanoid"); hp.Parent = npc
    local limb = M.Instance.new("Part"); limb.Parent = npc
    touch(M, w.Hazard, limb)
    check(hp.Health == 100, "NPC ignored")
    a.humanoid.Health = 0; M.advance(2); touch(M, w.Hazard, a.foot)
    check(a.humanoid.Health == 0, "dead character ignored")
end

do
    local M, a, b, w = fixture()
    local coin = w.Coin1
    touch(M, coin, a.foot, a.otherFoot, b.foot)
    check(a.player.leaderstats.Coins.Value == 5 and b.player.leaderstats.Coins.Value == 0, "single winner from queued contacts")
    check(coin.Transparency == 1 and coin.CanTouch == true and coin.Touched._connections[1].Connected, "hidden but connection retained")
    touch(M, w.Coin2, b.handle)
    check(b.player.leaderstats.Coins.Value == 5, "other coin independent")
    M.advance(3.99); touch(M, coin, b.foot)
    check(b.player.leaderstats.Coins.Value == 5 and coin.Transparency == 1, "coin unavailable before delay")
    M.advance(0.01)
    check(w.Coin1 == coin and coin.Transparency == 0, "same Part restored at scheduled test time")
    touch(M, coin, b.foot, a.foot)
    check(b.player.leaderstats.Coins.Value == 10 and a.player.leaderstats.Coins.Value == 5, "next single winner after restore")
end

do
    local M, a, b, w = fixture()
    touch(M, w.Checkpoint2, a.foot)
    touch(M, w.Checkpoint1, b.foot, a.foot, a.otherFoot)
    check(a.player.RespawnLocation == w.Checkpoint2 and a.player.leaderstats.Stage.Value == 2, "skip allowed, no rollback")
    check(b.player.RespawnLocation == w.Checkpoint1 and b.player.leaderstats.Stage.Value == 1, "personal checkpoint")
    local oldCharacter = a.character
    a.humanoid.Health = 0
    local replacement = M.Instance.new("Model"); replacement.Parent = M.workspace
    local hp = M.Instance.new("Humanoid"); hp.Parent = replacement
    local foot = M.Instance.new("Part"); foot.Parent = replacement
    a.player.Character = replacement
    touch(M, w.Coin1, foot)
    check(a.player.leaderstats.Stage.Value == 2 and a.player.leaderstats.Coins.Value == 5, "new character keeps Player session")
    local oldHP = oldCharacter:FindFirstChildOfClass("Humanoid"); oldHP.Health = 100
    touch(M, w.Coin2, a.foot)
    check(a.player.leaderstats.Coins.Value == 5, "old model no longer recognized as current character")
end

do
    local M, a, b, w = fixture()
    local medkit = w.Medkit
    touch(M, medkit, a.foot)
    check(w.Medkit == medkit and #M.jobs == 0, "full health does not consume or schedule")
    a.humanoid.Health = 95; b.humanoid.Health = 50
    touch(M, medkit, a.foot, a.otherFoot, b.foot)
    check(a.humanoid.Health == 100 and b.humanoid.Health == 50 and medkit._destroyed and w.Medkit == nil, "one heal, clamp, item destroyed")
    check(#M.jobs == 1, "one pending medkit spawn")
    M.advance(5.99); check(w.Medkit == nil, "no early medkit")
    M.advance(0.01)
    check(w.Medkit ~= nil and w.Medkit ~= medkit, "new identity after delay")
    local quantity = 0
    for _, child in w:GetChildren() do if child.Name == "Medkit" then quantity = quantity + 1 end end
    check(quantity == 1, "one new medkit")
    touch(M, w.Medkit, b.handle)
    check(b.humanoid.Health == 80, "new item connected and heals ordinary amount")
    w:Destroy(); M.advance(6)
    check(M.workspace.Lesson05Mechanics == nil and #M.jobs == 0, "no spawn after root removed")
end

do
    local M, a, b, w = fixture()
    local before = #M.workspace:GetChildren()
    M.run(Sources["Main.server.luau"])
    check(#M.warnings == 1 and #M.workspace:GetChildren() == before and #w.Coin1.Touched._connections == 1, "duplicate guard")
    M.emit(M.players.PlayerAdded, a.player); M.advance(0)
    check(#a.player:GetChildren() == 1 and a.player.leaderstats.Coins.Value == 0, "idempotent setup")
    local c = addPlayer(M, "C")
    M.emit(M.players.PlayerAdded, c.player); M.advance(0)
    check(c.player.RespawnLocation == w.Start and c.player.leaderstats.Coins.Value == 0, "late join")
    M.emit(M.players.PlayerRemoving, a.player); M.advance(0); a.player.Parent = nil
    touch(M, w.Coin1, a.foot)
    check(a.player.leaderstats.Coins.Value == 0 and w.Coin1.Transparency ~= 1, "departed player ignored")
    local again = addPlayer(M, "A")
    M.emit(M.players.PlayerAdded, again.player); M.advance(0)
    check(again.player.leaderstats.Coins.Value == 0 and again.player.leaderstats.Stage.Value == 0, "rejoin gets fresh record")
    local d = addPlayer(M, "D")
    local stats = M.Instance.new("Folder"); stats.Name = "leaderstats"; stats.Parent = d.player
    M.emit(M.players.PlayerAdded, d.player); M.advance(0)
    check(d.player.leaderstats == stats and #d.player:GetChildren() == 1 and #M.warnings == 2, "existing stats preserved")
end

print("Checks passed: " .. tostring(count))
