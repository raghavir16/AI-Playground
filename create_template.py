from utils.template_manager import TemplateManager
import os

def main():
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create the template
    template_path = os.path.join('templates', 'littlefish_template.docx')
    TemplateManager.create_littlefish_template(template_path)
    print(f"Template created successfully at: {template_path}")

if __name__ == "__main__":
    main() 