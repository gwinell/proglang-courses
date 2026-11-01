local root = Instance.new("Folder")
root.Name = "Lesson04Lifecycle"
root.Parent = workspace

local cube = Instance.new("Part")
cube.Name = "TemporaryCube"
cube.Size = Vector3.new(3, 3, 3)
cube.Position = Vector3.new(0, 4, -10)
cube.Anchored = true

local light = Instance.new("PointLight")
light.Parent = cube
cube.Parent = root

print("Потомков: " .. tostring(#root:GetDescendants()))
task.wait(1)

cube.Parent = nil
print("Детей после скрытия: " .. tostring(#root:GetChildren()))
task.wait(1)

cube.Parent = root
print("Детей после возврата: " .. tostring(#root:GetChildren()))
task.wait(1)

cube:Destroy()
cube = nil
light = nil
print("Потомков после Destroy: " .. tostring(#root:GetDescendants()))
