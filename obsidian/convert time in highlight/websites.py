from datetime import datetime
import os

directory = "Websites"

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)

    if os.path.isfile(file_path):
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()
        # Find the second occurrence of "---"
        first_index = content.find("---")
        second_index = content.find("---", first_index + 3)

        # change
        index = content.find("Updated on ")
        if (index == -1):
            continue
        index_end = content.find("]", index + 4)
        time_string = content[index+len("Updated on "):index_end]

        time_string = time_string[:len("2022-09-02")]
        print(time_string)

        if second_index != -1:
            # Insert "date:" before the second occurrence of "---"
            modified_content = content[:second_index] + \
                "date saved: "+time_string+"\n" + content[second_index:]

            # Write the modified content back to the file
            with open(file_path, 'w') as file:
                file.write(modified_content)

        print(f"Added 'date saved:' to {filename}.")

# # Original string
# original_string = "September 2, 2022 2:29 PM"

# # Convert to datetime object
# datetime_obj = datetime.strptime(original_string, "%B %d, %Y %I:%M %p")

# # Convert to desired format
# formatted_date = datetime_obj.strftime("%Y-%m-%d")

# print(formatted_date)  # Output: 2022-09-02
