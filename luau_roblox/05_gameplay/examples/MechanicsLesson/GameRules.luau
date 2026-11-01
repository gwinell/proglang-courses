local GameRules = {}

local function newSession()
    return {coins = 0, stage = 0, nextDamageAt = 0}
end

local function tryDamage(state, now, cooldown)
    if now < state.nextDamageAt then
        return false
    end
    state.nextDamageAt = now + cooldown
    return true
end

local function addCoins(state, amount)
    state.coins = state.coins + amount
    return state.coins
end

local function advanceCheckpoint(state, stage)
    if stage <= state.stage then
        return false
    end
    state.stage = stage
    return true
end

local function calculateHealedHealth(health, maxHealth, amount)
    return math.min(health + amount, maxHealth)
end

GameRules.newSession = newSession
GameRules.tryDamage = tryDamage
GameRules.addCoins = addCoins
GameRules.advanceCheckpoint = advanceCheckpoint
GameRules.calculateHealedHealth = calculateHealedHealth
return GameRules
