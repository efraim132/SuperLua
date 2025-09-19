Person = {}
Person.__index = Person

function Person:new(name, age)
  local self = setmetatable({__class = 'Person'}, Person)
      self.name = name
      self.age = age
  return self
end

function Person:say_hello(self)
      print("Hello, my name is " .. self.name .. " and I am " .. self.age .. " years old.")
end

function Person:get_name(self)
      return self.name
end



Dog = {}
Dog.__index = Dog

function Dog:new(name, breed)
  local self = setmetatable({__class = 'Dog'}, Dog)
      self.name = name
      self.breed = breed
  return self
end

function Dog:bark(self)
      print(self.name .. " says Woof!")
end



local person = Person:new("Alice", 30)
person:say_hello()

local dog = Dog:new("Buddy", "Golden Retriever")
dog:bark()
