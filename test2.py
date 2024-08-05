import cv2
import pytesseract
from matplotlib import pyplot as plt

# Dictionary with coordinates (corrected)
areas_dict = {
    "Gross Receipts": [1021, 1898, 1727, 1988],  # Adjusted coordinates
    "Return and Allowances": [2096, 1904, 2825, 1992],
    "Cost of Goods Sold": [4030, 2001, 4804, 2096],
    "Net Gain (Loss) from Form 4797, line 17": [4026, 2204, 4804, 2303],
    "Other Income (Loss)": [4021, 2312, 4809, 2397],
    "Total Income (Loss)": [4026, 2402, 4809, 2496],
    "Compensation of Officers": [4026, 2505, 4809, 2600],
    "Salaries and Wages": [4026, 2604, 4804, 2699],
    "Repairs and Maintenance": [4030, 2703, 4804, 2793],
    "Bad Debts": [4026, 2802, 4804, 2896],
    "Rents": [4021, 2906, 4804, 2996],
    "Taxes and Licenses": [4026, 3007, 4804, 3101],
    "Taxes and Licenses Statements": [1152, 2999, 3837, 3093],
    "Interest": [4017, 3107, 4809, 3197],
    "Depreciation": [4021, 3200, 4813, 3299],
    "Depletion": [4026, 3293, 4804, 3401],
    "Advertising": [4026, 3404, 4804, 3494],
    "Pension, Profit-Sharing, etc.": [4026, 3504, 4804, 3599],
    "Employee Benefit Programs": [4026, 3600, 4804, 3699],
    "Other Deductions": [4026, 3701, 4809, 3796],
    "Other Deductions Statements": [1673, 3696, 3846, 3790],
    "Total Deductions": [4026, 3803, 4809, 3897],
    "Ordinary Business Income (Loss)": [4026, 3901, 4809, 3996],
    "Excess Net Passive Income or LIFO Recapture": [3068, 4005, 3846, 4099],
    "Tax from Schedule D": [3068, 4102, 3837, 4196],
    "Add lines 22a and 22b": [4026, 4001, 4800, 4293],
    "2017 Estimated Tax Payments": [3063, 4286, 3841, 4400],
    "Tax Deposited With Form 7004": [3068, 4403, 3837, 4504],
    "Credit For Federal Tax Paid on Fuels": [3068, 4506, 3841, 4600],
    "Add lines 23a Through 23c": [4026, 4297, 4809, 4698],
    "Estimated Tax Penalty": [4026, 4706, 4809, 4796],
    "Amount Owed": [4026, 4797, 4809, 4896],
    "Overpayment": [4021, 4905, 4809, 5004],
    "Gross Profit": [4026, 2100, 4809, 2195],
    "Company Name": [1138, 886, 3779, 1093],
    "Year": [3913, 310, 4800, 688]
}

# Load the image
image_path = r"C:\Users\rybot\OneDrive\Desktop\Taxes for Code\111\Image Versions\Image 111 S Corp Tax Return IS no Statements.jpg"
image = cv2.imread(image_path)
image_boxes = cv2.imread(image_path)

# Get the dimensions of the image
img_height, img_width, _ = image.shape
print(f"Image dimensions: width={img_width}, height={img_height}")

# Function to preprocess and extract text from a given region
def extract_text_from_region(image, coords):
    x1, y1, x2, y2 = coords

    # Ensure the coordinates are within the image bounds
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(img_width, x2), min(img_height, y2)

    # Check if coordinates are valid
    if x1 >= x2 or y1 >= y2:
        raise ValueError(f"Invalid coordinates: ({x1}, {y1}, {x2}, {y2})")

    # Print debug information
    print(f"Cropping region: ({x1}, {y1}, {x2}, {y2})")

    # Crop the region from the image
    cropped_image = image[y1:y2, x1:x2]

    # Check if the cropped image is empty
    if cropped_image.size == 0:
        raise ValueError(f"Cropped image is empty for coordinates: ({x1}, {y1}, {x2}, {y2})")

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Apply manual thresholding
    _, thresh_image = cv2.threshold(gray_image, 140, 230, cv2.THRESH_BINARY_INV)

    # Rescale the image to increase DPI
    scale_percent = 200  # Percent of original size
    width = int(thresh_image.shape[1] * scale_percent / 100)
    height = int(thresh_image.shape[0] * scale_percent / 100)
    dim = (width, height)
    rescaled_image = cv2.resize(thresh_image, dim, interpolation=cv2.INTER_LINEAR)

    # Use pytesseract to extract text from the processed image
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(rescaled_image, config=custom_config)

    return text

# Loop through the dictionary and extract text for each region
extracted_texts = {}

for key, coords in areas_dict.items():
    x1, y1, x2, y2 = coords
    cv2.rectangle(image_boxes, (x1, y1), (x2, y2), (0, 0, 255), 2)
    try:
        text = extract_text_from_region(image, coords)
        extracted_texts[key] = text
        print(key, " : ", text)
    except Exception as e:
        print(f"Error processing {key}: {e}")

output_image_path = r'C:\Users\MSG_Rbott\OneDrive - Mark S. Gottlieb, CPA, PC\Desktop\Important\_MSG Code\Code\Matter 1\Image 111 S Corp Tax Return IS no Statements.jpg'
output_image_path2 = r'C:\Users\MSG_Rbott\OneDrive - Mark S. Gottlieb, CPA, PC\Desktop\Important\_MSG Code\Code\Matter 1\Image 111 S Corp Tax Return IS no Statements scaled.jpg'
cv2.imwrite(output_image_path, image_boxes)
#cv2.imwrite(output_image_path2, rescaled_image)

# Optionally, display the image with red boxes
plt.imshow(cv2.cvtColor(image_boxes, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
