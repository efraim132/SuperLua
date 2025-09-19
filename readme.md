# SuperLua 🎯

**Object-Oriented Programming for Lua and ComputerCraft**

SuperLua is a transpiler that brings clean, modern class syntax to Lua. Write object-oriented code that runs natively in ComputerCraft's vanilla Lua runtime.

## ✨ Features

- 🏗️ **Clean Class Syntax** - Write familiar OOP code
- 🔄 **Native Lua Output** - No runtime dependencies
- 🖥️ **Modern TUI Interface** - Beautiful terminal interface
- 💻 **CLI Support** - Traditional command-line usage
- 🎮 **ComputerCraft Ready** - Perfect for CC:Tweaked projects
- 📝 **Template System** - Quick start with built-in templates

## 🚀 Quick Start

### Option 1: TUI (Recommended)

```bash
python superlua_tui.py
```

### Option 2: Launcher (Choose Interface)

```bash
python launcher.py
```

### Option 3: Traditional CLI

```bash
python transpiler.py
```

## 📖 SuperLua Syntax

Write clean classes in `.slua` files:

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

Gets transpiled to efficient Lua:

```lua
Calculator = {}
Calculator.__index = Calculator

function Calculator:new(name)
  local self = setmetatable({__class = 'Calculator'}, Calculator)
  self.name = name
  self.result = 0
  return self
end

function Calculator:add(a, b)
  self.result = a + b
  return self.result
end

function Calculator:getResult()
  return self.result
end
```

## 🖥️ TUI Interface

The modern terminal interface provides:

- **📁 File Browser** - Navigate and open files visually
- **📝 Code Editor** - Syntax-highlighted editing
- **🔄 Live Transpilation** - Instant feedback
- **📊 Project Statistics** - Overview of your files
- **🏗️ Templates** - Start with pre-built classes
- **⌨️ Keyboard Shortcuts** - Efficient workflow

### TUI Shortcuts

- `Ctrl+N` - New file
- `F5` - Transpile current file
- `F1` - Help
- `Q` - Quit
- `Esc` - Close current screen

## 💡 Example Templates

### Basic Class

```superlua
class MyClass
  function new(self, name)
    self.name = name
  end

  function sayHello(self)
    print("Hello from " .. self.name)
  end
end
```

### Vector Math

```superlua
class Vector2D
  function new(self, x, y)
    self.x = x or 0
    self.y = y or 0
  end

  function add(self, other)
    return Vector2D:new(self.x + other.x, self.y + other.y)
  end

  function magnitude(self)
    return math.sqrt(self.x * self.x + self.y * self.y)
  end
end
```

## 🎮 ComputerCraft Integration

Perfect for ComputerCraft projects:

```superlua
class Turtle
  function new(self, name)
    self.name = name
    self.fuel = turtle.getFuelLevel()
  end

  function smartMove(self, direction)
    if self.fuel < 10 then
      self:refuel()
    end

    if direction == "forward" then
      turtle.forward()
    elseif direction == "up" then
      turtle.up()
    end
  end

  function refuel(self)
    turtle.refuel()
    self.fuel = turtle.getFuelLevel()
  end
end
```

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/SuperLua.git
   cd SuperLua
   ```

2. **Install dependencies**

   ```bash
   pip install rich textual click
   ```

3. **Run the TUI**
   ```bash
   python superlua_tui.py
   ```

## 📚 How It Works

SuperLua uses a line-by-line parser that:

1. **Detects Classes** - Finds `class Name` blocks
2. **Processes Methods** - Handles constructor and regular methods
3. **Manages Scope** - Tracks nested `end` statements
4. **Generates Lua** - Creates clean, efficient output

### Key Insights

- **Metatable Magic** - Uses Lua's metatable system for inheritance
- **Colon Syntax** - Leverages `:` for automatic `self` passing
- **No Runtime** - Pure transpilation, no dependencies
- **ComputerCraft Compatible** - Works in vanilla Lua 5.2/5.3

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Inheritance support
- [ ] Static methods
- [ ] Better error messages
- [ ] IDE integration
- [ ] More templates

## 📄 License

MIT License - See LICENSE file for details

## 🎯 Why SuperLua?

**The Problem**: Lua's OOP requires verbose metatable boilerplate
**The Solution**: Clean class syntax that transpiles to efficient Lua
**The Result**: Modern OOP patterns for ComputerCraft and beyond!

---

_Made with ❤️ for the ComputerCraft community_
