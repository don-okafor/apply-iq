from typing import Any, Dict
import json
import re

class TypeConverter:

    def __init__(self):
        pass

    def get_dict_from_json(self, json_data:str) -> Dict[str, Any]:
        """Return the json data."""
         # Clean the string
        if json_data and json_data.startswith("```json"):
            # Remove ```json and get JSON body
            json_data = json_data.strip("`").split("\n", 1)[1]  
            json_data = json_data.rsplit("\n```", 1)[0]
            # Convert JSON text to Python dictionary
            return json.loads(json_data)
        else:
            return json_data
    
    def remove_spaces_and_special_characters(self, input_string):
        # Remove spaces
        string_without_spaces = input_string.replace(" ", "")

        # Remove special characters using regex (keeping only alphanumeric characters)
        # The regex '[^a-zA-Z0-9]' matches any character that is NOT an alphanumeric character.
        # re.sub() replaces all occurrences of the pattern with an empty string.
        cleaned_string = re.sub(r'[^a-zA-Z0-9]', '', string_without_spaces)

        return cleaned_string
    
    def write_dict_to_pdf(self, data: dict, filepath: str):
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.lib.pagesizes import LETTER
        
        doc = SimpleDocTemplate(filepath, pagesize=LETTER)
        styles = getSampleStyleSheet()
        story = []
        
        def render_dict(d, level=0):
            for key, value in d.items():
                if level == 0:
                    style = styles['Heading1']
                elif level == 1:
                    style = styles['Heading2']
                else:
                    style = styles['Normal']

                story.append(Paragraph(str(key), style))
                story.append(Spacer(1, 0.1 * inch))

                if isinstance(value, dict):
                    render_dict(value, level + 1)
                else:
                    story.append(Paragraph(str(value), styles['Normal']))
                    story.append(Spacer(1, 0.2 * inch))

        render_dict(data)
        doc.build(story)
        
    def write_string_to_pdf_file(self, text_content, output_filename="output.pdf"):
        from fpdf import FPDF
        try:
            # Create a new PDF object
            # P = Portrait, mm = millimeters as unit, A4 = page format
            pdf = FPDF('P', 'mm', 'A4')
            
            # Add a page
            pdf.add_page()

            # Set font: Arial, Regular, size 12
            pdf.set_font('Arial', '', 12)

            # Write the text content.
            # The multi_cell method is used to print text with automatic word-wrap.
            # 0: width (0 means stretching to the right margin)
            # 10: height of each line
            # text_content: the string to print
            # 0: border (0 means no border)
            # 'J': align (J = Justify, L = Left, C = Center, R = Right)
            # 0: fill (0 means no background fill)
            pdf.multi_cell(0, 10, text_content, 0, 'L')

            # Save the PDF to the specified filename
            pdf.output(output_filename)
            print(f"Text successfully written to '{output_filename}'")

        except Exception as e:
            print(f"An error occurred: {e}")
