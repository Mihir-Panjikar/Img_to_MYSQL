import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        label.config(text="Selected File: " + file_path)
        processing_image(file_path)

def processing_image(filepath):
    # Loading the table image
    image = cv2.imread(filepath)

    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Unable to load the image from '{image}'")
    else:
        # Preprocess the image (you can adjust these preprocessing steps as needed)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Find contours in the image to identify table cells
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop through each contour (cell) and extract text
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cell = image[y:y+h, x:x+w]

            # Perform OCR on the cell
            text = pytesseract.image_to_string(cell)  # --psm 6 for treating the image as a single uniform block of text
            
            for char in text:
                text = text.replace("|", "")
            
            newline_separated = text.split('\n')
            
            filtered_list = []
            for item in newline_separated:
                if not item.strip() == '':
                    filtered_list.append(item)

            # Print the extracted text from the cell
            print()
            print(text.strip())
            
            print()
            # print(filtered_list)
            
            # Gets the table fields for creating the table
            table_fields = filtered_list[0].split(' ')
            
            # Gets the table records
            records = filtered_list[1:]
            
            while '' in table_fields:
                table_fields.remove('')
            
            # print(table_fields)
            
            # W
            with open("main_sql.sql", "w") as file:
                # Creating the table
                file.write("CREATE TABLE 'table_name' (")
                for item in table_fields:
                    if item != table_fields[-1]:
                        file.write(item + " type" + ",")
                    
                    else:
                        file.write(item + " type")
                file.write(");")
                

                # Writing Insert statements
                file.write("\n\nINSERT INTO 'table_name'\n\tVALUES (")
                for record in records:
                    individual_entities = record.split(' ')
                    while '' in individual_entities:
                        individual_entities.remove('')
                        
                    if record != records[-1]:
                        for entity in individual_entities:
                            if entity != individual_entities[-1]:
                                file.write(entity + " ,")
                            else:
                                file.write(entity + "),\n\t\t(")
                    else:
                        for entity in individual_entities:
                            if entity != individual_entities[-1]:
                                file.write(entity + " ,")
                            else:
                                file.write(entity + ");")
                    
                file.close()

        # Optionally, you can save the preprocessed image
        # cv2.imwrite('preprocessed_table.png', thresh)

        # Release resources
    cv2.destroyAllWindows()
    
    root.destroy()

# Create a Tkinter window
root = tk.Tk()  # Replace "plastik" with the desired theme
root.title("IMG TO SQL")
root.geometry("600x400")

# Create a label to display the selected file
label = tk.Label(root, text="")
label.pack()

# Create a button to open the file dialog
open_button = tk.Button(root, text="Open File", command=open_file_dialog)
open_button.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()