# SuperLua Transpiler

Transform your SuperLua code with classes into standard Lua compatible with ComputerCraft.

## Web Interface (Recommended)

The easiest way to use the SuperLua Transpiler is through the web interface:

1. **Open the web interface**: Open `transpiler_web.html` in any modern web browser
2. **Enter your code**: Type or paste your SuperLua code in the left panel
3. **Transpile**: Click "Transpile Code" or press `Ctrl+Enter`
4. **Get results**: The converted Lua code will appear in the right panel
5. **Try examples**: Click the example buttons to see sample SuperLua classes

### Features
- **Live transpilation**: Instant conversion in your browser
- **Dark theme**: GitHub-inspired interface
- **Example code**: Built-in Vector, Person, and Calculator class examples
- **Keyboard shortcuts**: `Ctrl+Enter` to transpile
- **Copy-paste friendly**: Easy to copy results for use in ComputerCraft

## What is SuperLua?

SuperLua adds object-oriented programming to Lua with a simple class syntax:

```superlua
class Vector
    function new(self, x, y)
        self.x = x or 0
        self.y = y or 0
    end
    
    function add(self, other)
        return Vector:new(self.x + other.x, self.y + other.y)
    end
end

-- Usage
local v1 = Vector:new(3, 4)
local v2 = Vector:new(1, 2) 
local v3 = v1:add(v2)
```

This gets converted to standard Lua using metatables:

```lua
Vector = {}
Vector.__index = Vector

function Vector:new(x, y)
  local self = setmetatable({__class = 'Vector'}, Vector)
  self.x = x or 0
  self.y = y or 0
  return self
end

function Vector:add(other)
  return Vector:new(self.x + other.x, self.y + other.y)
end
```

## How I Built SuperLua: Adding Object-Oriented Programming to Lua

This is my journey of creating a transpiler that brings class-based object-oriented programming to Lua. I wanted to make Lua feel more like modern programming languages while still running on ComputerCraft's vanilla Lua runtime.

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

## Python CLI Usage

If you prefer command line usage:

### Installation
```bash
pip install -r requirements.txt
```

### Usage
```bash
python transpiler.py input.slua output.lua
```

## File Structure

- `transpiler_web.html` - Web interface (recommended)
- `transpiler.py` - Python transpiler core
- `sample.slua` - Example SuperLua file
- `advanced_math.slua` - Advanced example with multiple classes
- `requirements.txt` - Python dependencies

Feel free to submit issues, feature requests, or pull requests to improve the SuperLua transpiler!
