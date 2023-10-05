import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog
import time

# Func for opening the dialog box for inserting the image
def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        label.config(text="Selected File: " + file_path)
        processing_image(file_path)

# Func to stop the program 
def kill_process(error: str):
    label.config(text=error)
    time.sleep(3)
    cv2.destroyAllWindows()
    root.destroy()

# Func to OCR the image
def processing_image(filepath):
    # Loading the table image
    image = cv2.imread(filepath)

    # Check if the image was loaded successfully
    if image is None or not str(filepath).endswith(('.png', '.jpeg', '.jpg')):
        error_msg = f"Error: Unable to load the image from '{image}'"
        kill_process(error_msg)

    else:
        res = cv2.resize(image,None,fx=0.8, fy=0.8, interpolation = cv2.INTER_CUBIC)
        h,w,ch = res.shape
        cv2.rectangle(res, (0,0), (w,h), (0,0,0), 10)

        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray,220,255,cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        sort_cnts = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * res.shape[1])
        
        if len(sort_cnts) < 1:
            error_msg = "Error, OCR failed"
            kill_process(error_msg)

        ROIs = []
        coordinates = []

        for cnt in sort_cnts:
            x,y,w,h = cv2.boundingRect(cnt)
            if [x, y, w, h] not in coordinates:
                if 2000 > w > 70 and h < 100:
                    ROI = res[y:y+h, x:x+w]
                    ROIs.append(ROI)
                    cv2.rectangle(res, (x,y), (x+w,y+h), (0,255,0), 2)
            coordinates.append([x, y, w, w])
            
        # Optionally, you can save the preprocessed image
        cv2.imwrite('preprocessed_table.png', res)

        # Loop through each contour (cell) and extract text
        for ROI in ROIs:
            # Perform OCR on the cell
            text = pytesseract.image_to_string(ROI)  # 8 Treat the image as a single word.
            
            for char in text:
                if ord(char) not in range(65,91) and ord(char) not in range(97, 123) and ord(char) not in range(48, 58):
                    text = text.replace(char, "")
            
            text = text.strip()
            
            # Print the extracted text from the cell
            print(text)
            # print(filtered_list)
            
            # # Gets the table fields for creating the table and filters them
            # table_fields = filtered_list[0].split(' ')
            # while '' in table_fields:
            #     table_fields.remove('')
            
            # # Gets the table records
            # records = filtered_list[1:]
            
            # # Writing the sql file
            # with open("main_sql.sql", "w") as file:
            #     # Creating the table
            #     create_table = f"CREATE TABLE 'table_name' ({' type, '.join(table_fields)} type);\n\n"
            #     file.write(create_table)                

            #     # Writing Insert statements
            #     file.write("INSERT INTO 'table_name'\n\tVALUES (")
            #     for record in records:
            #         if record != records[-1]:
            #             file.write(f"{', '.join(record)}),\n\t\t(")
                        
            #         else:
            #             file.write(f"{', '.join(record)});")

            #     file.close()

    # Release resources
    cv2.destroyAllWindows()
    root.destroy()

# Create a Tkinter window
root = tk.Tk()
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