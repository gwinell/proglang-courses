local part = Instance.new("Part")
part.Name = "Lesson04Properties"
part.Size = Vector3.new(6, 1, 6)
part.Position = Vector3.new(0, 3, -10)
part.Anchored = true
part.CanCollide = true
part.Color = Color3.fromRGB(37, 99, 235)
part.Transparency = 0.2
part.Parent = workspace

print(part.ClassName)
print(part.Name)
print(part.Size.Y)
print(part.Position.Y)
