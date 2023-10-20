from tkinter import *
from tkinter import filedialog, messagebox
import requests
from creds import API_Key


# Class to handle the application
class PdfProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ILovePDF API PDF Processor")
        self.root.geometry("560x480")
        self.root.config(bg="#5193b3")

        self.frame = Frame(self.root, bg="#5193b3")
        self.frame.pack(fill=X)

        self.combine_button = Button(self.frame, text="Combine PDFs", command=self.combine_pdfs,
                                        font=("Calibri", 12, "bold"), fg="white", bg="#4CBB17", bd=2)
        self.combine_button.pack(pady=10)

        self.separate_button = Button(self.frame, text="Separate PDFs", command=self.separate_pdfs,
                                         font=("Calibri", 12, "bold"), fg="white", bg="#4CBB17", bd=2)
        self.separate_button.pack(pady=10)

        self.remove_password_button = Button(self.frame, text="Remove PDF Password", command=self.remove_pdf_password,
                                                font=("Calibri", 12, "bold"), fg="white",bg="#4CBB17", bd=2)
        self.remove_password_button.pack(pady=10)

        self.extract_text_button = Button(self.frame, text="Extract Text from PDF", command=self.extract_text_from_pdf,
                                             font=("Calibri", 12, "bold"), fg="white", bg="#4CBB17", bd=2)
        self.extract_text_button.pack(pady=10)

        self.image_to_pdf_button = Button(self.frame, text="Convert Images to PDF", command=self.image_to_pdf,
                                             font=("Calibri", 12, "bold"), fg="white", bg="#4CBB17", bd=2)
        self.image_to_pdf_button.pack(padx=10,pady=10)

    # Method to combine PDFs
    def combine_pdfs(self):
        file_names = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if file_names:
            combine_pdfs(file_names)

    # Method to separate PDFs
    def separate_pdfs(self):
        file_name = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_name:
            separate_pdfs(file_name)

    # Method to remove PDF password
    def remove_pdf_password(self):
        file_name = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_name:
            remove_pdf_password(file_name)

    # Method to extract text from PDF
    def extract_text_from_pdf(self):
        file_name = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_name:
            extract_text_from_pdf(file_name)

    # Method to convert images to PDF
    def image_to_pdf(self):
        file_names = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.tiff")])
        if file_names:
            image_to_pdf(file_names)


'''
def save_response(response):
    if response.status_code == 200:
        with open("modified.pdf", "wb") as output_file:
            output_file.write(response.content)
        '''
# Method to combine PDFs
def combine_pdfs(file_names):
    files = {"file": (file_name, open(file_name, "rb")) for file_name in file_names}
    response = requests.post("https://api.ilovepdf.com/v1/task/combine", files=files, headers={"Authorization": API_Key})
    save_response(response)


# Method to separate PDFs
def separate_pdfs(file_name):
    files = {"file": (file_name, open(file_name, "rb"))}
    response = requests.post("https://api.ilovepdf.com/v1/task/split", files=files, headers={"Authorization": API_Key})
    save_response(response)


# Method to remove PDF password
def remove_pdf_password(file_name):
    files = {"file": (file_name, open(file_name, "rb"))}
    response = requests.post("https://api.ilovepdf.com/v1/task/unlock", files=files, headers={"Authorization": API_Key})
    save_response(response)


# Method to extract text from PDF
def extract_text_from_pdf(file_name):
    files = {"file": (file_name, open(file_name,"rb"))}
    response = requests.post("https://api.ilovepdf.com/v1/task/extract", files=files, headers={"Authorization": API_Key})
    save_response(response)


# Method convert images to convert images to PDF
def image_to_pdf(file_names):
    files = {"file": (file_name, open(file_name, "rb")) for file_name in file_names}
    response = requests.post("https://api.ilovepdf.com/v1/task/imagepdf", files=files, headers={"Authorization": API_Key})
    save_response(response)


# Method to save the API response as a file
def save_response(response):
    print(f"API Response Status Code: {response.status_code}")
    print(f"API Response Content: {response.text}")
    if response.status_code == 200:
        # If the API response is successful, save the resulting PDF to disk
        with open("results.pdf", 'wb') as f:
            f.write(response.content)
        messagebox.showinfo("Success", "Response Saved Successfully")

    else:
        # If the API response is unsuccessful, print the response error message
        response_data = response.json()
        error_message = response_data.get("message", "Unknown Error")
        print(f"API Response Error: {error_message}")
        messagebox.showerror("Failed",
                             f"Response failed with status code: {response.status_code}\nError: {error_message}")


def main():
    root = Tk()
    app = PdfProcessorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()