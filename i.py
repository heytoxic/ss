import json
import os

input_file = 'ig.json'
output_file = 'insta.json'

def clean_data():
    print("Processing start ho rahi hai... Thoda wait karein.")
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        f_out.write("[\n") # JSON Array start
        first_line = True
        
        for line in f_in:
            line = line.strip()
            if not line:
                continue
                
            try:
                # Line ko dictionary mein convert karna
                data = json.loads(line)
                
                # Naye format mein map karna
                clean_obj = {
                    "username": data.get("u"),
                    "id": data.get("id"),
                    "email": data.get("e"),
                    "phone": data.get("t"),
                    "name": data.get("n"),
                    "extra": {}
                }
                
                # Agar koi extra fields hain jo upar cover nahi hue
                known_keys = {'u', 'id', 'e', 't', 'n'}
                for key, value in data.items():
                    if key not in known_keys:
                        clean_obj["extra"][key] = value
                
                # JSON array formatting
                if not first_line:
                    f_out.write(",\n")
                
                json.dump(clean_obj, f_out, ensure_ascii=False)
                first_line = False
                
            except json.JSONDecodeError:
                continue # Agar koi line kharab hai to skip kar dega

        f_out.write("\n]") # JSON Array end

    print(f"Done! Saara data '{output_file}' mein save ho gaya hai.")

if __name__ == "__main__":
    if os.path.exists(input_file):
        clean_data()
    else:
        print(f"Error: '{input_file}' file nahi mili!")

