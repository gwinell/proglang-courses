-- Test-only model. It does not simulate physics, UI, networking or engine scheduling.
local Model = {}

function Model.new()
    local M = {now = 0, jobs = {}, output = {}, warnings = {}}
    local methods = {}
    local create

    local function resumeThread(thread, ...)
        local ok, delay = coroutine.resume(thread, ...)
        if not ok then
            error(delay)
        end
        if coroutine.status(thread) ~= "dead" then
            table.insert(M.jobs, {at = M.now + (delay or 0), thread = thread})
        end
    end

    local function signal()
        local s = {_connections = {}}
        function s:Connect(handler)
            assert(type(handler) == "function", "Connect requires a function")
            local connection = {Connected = true, handler = handler}
            function connection:Disconnect()
                self.Connected = false
            end
            table.insert(self._connections, connection)
            return connection
        end
        return s
    end

    function M.emit(s, ...)
        local arguments = {...}
        for _, connection in s._connections do
            if connection.Connected then
                local thread = coroutine.create(function()
                    connection.handler(table.unpack(arguments))
                end)
                table.insert(M.jobs, {at = M.now, thread = thread})
            end
        end
    end

    function M.advance(seconds)
        local target = M.now + seconds
        local guard = 0
        while true do
            local nextIndex = nil
            local nextAt = math.huge
            for index, job in M.jobs do
                if job.at < nextAt then
                    nextIndex, nextAt = index, job.at
                end
            end
            if nextIndex == nil or nextAt > target + 0.000001 then
                break
            end
            guard = guard + 1
            assert(guard <= 1000, "Unexpected unbounded scheduling")
            local job = table.remove(M.jobs, nextIndex)
            M.now = job.at
            resumeThread(job.thread)
        end
        M.now = target
    end

    function methods:GetChildren()
        return table.clone(self._children)
    end

    function methods:GetDescendants()
        local result = {}
        local function visit(object)
            for _, child in object._children do
                table.insert(result, child)
                visit(child)
            end
        end
        visit(self)
        return result
    end

    function methods:FindFirstChild(name, recursive)
        for _, child in (if recursive then self:GetDescendants() else self:GetChildren()) do
            if child.Name == name then
                return child
            end
        end
        return nil
    end

    function methods:FindFirstChildOfClass(className)
        for _, child in self._children do
            if child.ClassName == className then
                return child
            end
        end
        return nil
    end

    function methods:WaitForChild(name, timeout)
        local child = self:FindFirstChild(name)
        if child == nil and timeout then
            coroutine.yield(timeout)
            child = self:FindFirstChild(name)
        end
        return child
    end

    function methods:IsA(className)
        return className == "Instance" or className == self.ClassName
            or (className == "BasePart" and (self.ClassName == "Part" or self.ClassName == "SpawnLocation"))
    end

    function methods:GetPropertyChangedSignal(name)
        if self._propertySignals[name] == nil then
            self._propertySignals[name] = signal()
        end
        return self._propertySignals[name]
    end

    function methods:Destroy()
        for _, child in self:GetChildren() do
            child:Destroy()
        end
        for _, event in self._events do
            for _, connection in event._connections do
                connection:Disconnect()
            end
        end
        for _, event in self._propertySignals do
            for _, connection in event._connections do
                connection:Disconnect()
            end
        end
        self.Parent = nil
        rawset(self, "_destroyed", true)
    end

    function methods:GetPlayers()
        return self:GetChildren()
    end

    function methods:GetPlayerFromCharacter(character)
        for _, player in self:GetPlayers() do
            if player.Character == character then return player end
        end
        return nil
    end

    function methods:TakeDamage(amount)
        if self.Parent:FindFirstChildOfClass("ForceField") == nil then
            self.Health = math.max(0, self.Health - amount)
        end
    end

    create = function(className)
        local object = {
            _props = {Name = className, ClassName = className, Enabled = true},
            _children = {}, _propertySignals = {}, _events = {},
        }
        if className == "Part" or className == "SpawnLocation" then
            object._events.Touched = signal()
        elseif className == "Players" then
            object._events.PlayerAdded = signal()
            object._events.PlayerRemoving = signal()
        elseif className == "Humanoid" then
            object._props.Health = 100
            object._props.MaxHealth = 100
        elseif className == "IntValue" then
            object._props.Value = 0
        elseif className == "ProximityPrompt" then
            object._events.Triggered = signal()
        end
        return setmetatable(object, {
            __index = function(self, key)
                if methods[key] then return methods[key] end
                if self._events[key] then return self._events[key] end
                if self._props[key] ~= nil then return self._props[key] end
                for _, child in self._children do
                    if child.Name == key then return child end
                end
                return nil
            end,
            __newindex = function(self, key, value)
                assert(not self._destroyed, "Cannot modify destroyed object")
                assert(key ~= "ClassName", "ClassName is read-only")
                local previous = self._props[key]
                if key == "Parent" then
                    if previous then
                        local index = table.find(previous._children, self)
                        if index then table.remove(previous._children, index) end
                    end
                    if value then table.insert(value._children, self) end
                end
                if key == "CanTouch" and value == false and self._events.Touched then
                    for _, c in self._events.Touched._connections do c:Disconnect() end
                end
                self._props[key] = value
                if previous ~= value and self._propertySignals[key] then
                    M.emit(self._propertySignals[key])
                end
            end,
        })
    end

    M.players = create("Players")
    M.modules = create("Folder")
    M.modules.Name = "MechanicsLesson"
    M.script = create("Script")
    M.script.Parent = M.modules
    M.moduleCache = {}
    M.workspace = create("Workspace")
    M.workspace.Name = "Workspace"
    M.Instance = {new = create}
    M.Color3 = {fromRGB = function(r, g, b) return tostring(r) .. "," .. tostring(g) .. "," .. tostring(b) end}
    M.Vector3 = {new = function(x, y, z) return {X = x, Y = y, Z = z} end}
    M.Enum = {KeyCode = {E = "E"}, Material = {Neon = "Neon"}, PartType = {Ball = "Ball"}}

    function M.environment()
        return setmetatable({
            workspace = M.workspace, Instance = M.Instance, Color3 = M.Color3,
            Vector3 = M.Vector3, Enum = M.Enum,
            script = M.script,
            game = {GetService = function(_, name) assert(name == "Players"); return M.players end},
            os = {clock = function() return M.now end},
            require = function(module)
                if M.moduleCache[module] ~= nil then return M.moduleCache[module] end
                local compiled, message = loadstring(module.Source)
                assert(compiled, message)
                setfenv(compiled, M.environment())
                local value = compiled()
                M.moduleCache[module] = value
                return value
            end,
            task = {
                wait = function(seconds) return coroutine.yield(seconds or 0) end,
                delay = function(seconds, callback)
                    assert(type(callback) == "function")
                    table.insert(M.jobs, {at = M.now + seconds, thread = coroutine.create(callback)})
                end,
            },
            print = function(...)
                local values = {...}
                for i, value in values do values[i] = tostring(value) end
                table.insert(M.output, table.concat(values, "\t"))
            end,
            warn = function(value) table.insert(M.warnings, tostring(value)) end,
        }, {__index = getfenv(0)})
    end

    function M.run(source)
        local compiled, message = loadstring(source)
        assert(compiled, message)
        setfenv(compiled, M.environment())
        resumeThread(coroutine.create(compiled))
        M.advance(0)
    end

    return M
end

return Model
