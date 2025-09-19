import os
import re

def transpile_superlua(input_code):
    output_code = []
    
    # Split input into lines for easier processing
    lines = input_code.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if we're starting a class
        if line.startswith('class '):
            class_name = line.split()[1]
            output_code.append(f"{class_name} = {{}}")
            output_code.append(f"{class_name}.__index = {class_name}")
            output_code.append("")
            i += 1
            
            # Process class body
            while i < len(lines):
                line = lines[i].strip()
                
                # Check if we're at the end of the class
                if line == 'end':
                    break
                
                # Check if we're starting a function
                if line.startswith('function '):
                    # Parse function declaration
                    func_line = line
                    func_match = re.match(r'function\s+(\w+)\s*\((.*?)\)', func_line)
                    if func_match:
                        method_name = func_match.group(1)
                        method_args = func_match.group(2).strip()
                        
                        # Collect function body until matching 'end'
                        i += 1
                        method_body = []
                        end_count = 1  # We need to find the matching 'end'
                        
                        while i < len(lines) and end_count > 0:
                            current_line = lines[i]
                            stripped_line = current_line.strip()
                            
                            # Count nested structures
                            if stripped_line.startswith('if ') or stripped_line.startswith('for ') or stripped_line.startswith('while ') or stripped_line.startswith('function '):
                                end_count += 1
                            elif stripped_line == 'end':
                                end_count -= 1
                            
                            # Add line to body if we haven't found the matching end
                            if end_count > 0:
                                method_body.append(current_line)
                            
                            i += 1
                        
                        # Generate the method
                        if method_name == "new":
                            # Constructor
                            clean_args = method_args.replace('self', '').strip()
                            if clean_args.startswith(','):
                                clean_args = clean_args[1:].strip()
                            output_code.append(f"function {class_name}:{method_name}({clean_args})")
                            output_code.append(f"  local self = setmetatable({{__class = '{class_name}'}}, {class_name})")
                            for body_line in method_body:
                                output_code.append("  " + body_line)
                            output_code.append("  return self")
                            output_code.append("end")
                        else:
                            # Regular method - remove 'self' from parameters since colon syntax provides it
                            clean_args = method_args.replace('self', '').strip()
                            if clean_args.startswith(','):
                                clean_args = clean_args[1:].strip()
                            if clean_args.endswith(','):
                                clean_args = clean_args[:-1].strip()
                            output_code.append(f"function {class_name}:{method_name}({clean_args})")
                            for body_line in method_body:
                                output_code.append("  " + body_line)
                            output_code.append("end")
                        
                        output_code.append("")
                        i -= 1  # Adjust because we'll increment at the end of the loop
                else:
                    # Non-function line within class - skip or preserve comments
                    if line and not line.startswith('--'):
                        pass  # Skip non-comment, non-function lines in class
                    
                i += 1
            
            output_code.append("")
        else:
            # Non-class line - preserve it
            output_code.append(lines[i])
        
        i += 1
    
    return "\n".join(output_code)

def main():
    print("SuperLua Transpiler (SLUA to LUA)")

    input_file_path = None
    while not input_file_path:
        path_input = input("Enter the path to your .slua file: ")
        if not os.path.exists(path_input):
            print("Error: File does not exist.")
        elif not path_input.endswith(".slua"):
            print("Error: File is not a .slua file.")
        else:
            input_file_path = path_input

    if not input_file_path:
        print("No input file provided. Exiting.")
        return

    default_output_file_path = input_file_path.replace(".slua", ".lua")
    output_file_path = input(f"Enter the output .lua file path (default: {default_output_file_path}): ")
    if not output_file_path:
        output_file_path = default_output_file_path

    if not output_file_path:
        print("No output file path provided. Exiting.")
        return

    try:
        with open(input_file_path, 'r') as f:
            superlua_code = f.read()

        transpiled_code = transpile_superlua(superlua_code)

        with open(output_file_path, 'w') as f:
            f.write(transpiled_code)

        print(f"Successfully transpiled '{input_file_path}' to '{output_file_path}'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
