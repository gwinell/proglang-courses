local root = Instance.new("Folder")
root.Name = "Lesson04Tree"

local inbox = Instance.new("Folder")
inbox.Name = "Inbox"
inbox.Parent = root

local archive = Instance.new("Folder")
archive.Name = "Archive"
archive.Parent = root

local token = Instance.new("Part")
token.Name = "Token"
token.Size = Vector3.new(2, 2, 2)
token.Position = Vector3.new(0, 4, -10)
token.Anchored = true
token.Parent = inbox

local light = Instance.new("PointLight")
light.Name = "Glow"
light.Brightness = 2
light.Range = 10
light.Parent = token

root.Parent = workspace

print(token.Parent.Name)
print(#root:GetChildren())
print(#root:GetDescendants())
print(root:FindFirstChild("Token") == nil)
print(root:FindFirstChild("Token", true).Name)

token.Parent = archive
print(token.Parent.Name)
print(token.Position.Y)
print(#inbox:GetChildren())

local partCount = 0
for index, object in root:GetDescendants() do
    if object:IsA("BasePart") then
        object.Color = Color3.fromRGB(15, 138, 104)
        partCount = partCount + 1
    end
end
print(partCount)
