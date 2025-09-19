How I Built SuperLua: Adding Object-Oriented Programming to Lua

This is my journey of creating a transpiler that brings class-based object-oriented programming to Lua. I wanted to make Lua feel more like modern programming languages while still running on ComputerCraft's vanilla Lua runtime.

## What is SuperLua?

SuperLua is a simple language extension that adds class syntax to Lua. I created it because writing object-oriented code in pure Lua can be messy with all the metatable boilerplate. SuperLua lets me write clean, readable classes that transpile to efficient Lua code.

Here's what SuperLua looks like:

```superlua
class Calculator
  function new(self, name)
    self.name = name
    self.result = 0
  end

  function add(self, a, b)
    self.result = a + b
    return self.result
  end

  function getResult(self)
    return self.result
  end
end

local calc = Calculator:new("MathBot")
calc:add(5, 3)
print("Result: " .. calc:getResult())
```

## How the Transpiler Works

I built the transpiler using Python and a line-by-line parsing approach. Here's how it transforms SuperLua into standard Lua:

### Step 1: Class Declaration

When I write `class Calculator`, the transpiler generates:

```lua
Calculator = {}
Calculator.__index = Calculator
```

This creates the class table and sets up the metatable system that Lua uses for object-oriented programming.

### Step 2: Constructor Method

The `new` method gets special treatment. It becomes a constructor that:

- Creates a new object with `setmetatable()`
- Runs the initialization code
- Returns the new object

```lua
function Calculator:new(name)
  local self = setmetatable({__class = 'Calculator'}, Calculator)
  self.name = name
  self.result = 0
  return self
end
```

### Step 3: Regular Methods

Other methods are converted to standard Lua functions with the class prefix:

```lua
function Calculator:add(a, b)
  self.result = a + b
  return self.result
end
```

The key insight I discovered: Lua's colon syntax `:` automatically passes `self` as the first parameter, so I had to remove explicit `self` parameters from the method signatures to avoid conflicts.

## The Parsing Algorithm

I went through several iterations before settling on a line-by-line parser instead of regex. Here's why:

1. **Regex was too fragile** - Nested structures like if/for/while blocks inside methods broke the pattern matching
2. **End counting was crucial** - I needed to track nested `end` statements to properly close method bodies
3. **Line-by-line gave better control** - I could handle edge cases and maintain proper indentation

The parser tracks:

- Class boundaries (`class Name` to `end`)
- Method boundaries (`function name()` to matching `end`)
- Nested structures that increment the `end` counter

## Key Challenges I Solved

### Problem 1: Table Literal Syntax

Initial bug: `{'__class' = 'Calculator'}` - Invalid Lua syntax
Solution: Use `{__class = 'Calculator'}` without quotes around keys

### Problem 2: Method Call Syntax

Initial bug: Methods defined with explicit `self` parameter caused "attempt to index nil" errors
Solution: Remove `self` from parameter lists since colon syntax provides it automatically

### Problem 3: Nested Structure Parsing

Initial bug: Regex captured everything until the last `end`, breaking method boundaries
Solution: Line-by-line parsing with proper `end` counting for nested blocks

## Object-Oriented Features

SuperLua supports real OOP concepts:

- **Encapsulation**: Data and methods bundled in classes
- **Instance Variables**: Each object has its own state (`self.name`, `self.result`)
- **Method Chaining**: Objects can call methods on themselves and other objects
- **State Persistence**: Objects remember their data between method calls
- **Constructor Pattern**: Clean initialization with the `new` method

## Why This Matters for ComputerCraft

ComputerCraft uses Lua 5.2/5.3 without any extensions. My transpiler produces vanilla Lua that runs perfectly in this environment. This means I can:

- Write complex robot control systems with clean class hierarchies
- Build reusable code libraries with proper encapsulation
- Create maintainable large-scale ComputerCraft projects
- Use familiar OOP patterns from other languages

## Usage

1. Write your code in `.slua` files using class syntax
2. Run `python transpiler.py`
3. Copy the generated `.lua` files to ComputerCraft
4. Your object-oriented code runs natively!

The transpiler bridges the gap between modern programming practices and ComputerCraft's constraints, letting me write better code without sacrificing compatibility.
