from bs4 import BeautifulSoup
import os
from sys import argv



EXACT_CRITERIA_ID = "make-everything-ok-button"
PATH_EXAMPLES_DIR = "html-examples"



if len(argv) > 1:
    _, origin_file, dif_file = argv
else:
    origin_file = "sample-0-origin.html"
    dif_files = ["sample-1-evil-gemini.html", "sample-2-container-and-clone.html", "sample-3-the-escape.html", "sample-4-the-mash.html"]
    origin_file = os.path.join(PATH_EXAMPLES_DIR, origin_file)
    dif_file = os.path.join(PATH_EXAMPLES_DIR, dif_files[0])
print ("Your origin file is:", origin_file)
print ("Your dif file is:", dif_file)



def main():
    try:
        soup_origin = BeautifulSoup(open(origin_file), "lxml")
        soup_diff = BeautifulSoup(open(dif_file), "lxml")

        origin_btn = soup_origin.find(id=EXACT_CRITERIA_ID)
        print(f"\nOriginal button in '{origin_file}': \n\n {origin_btn.prettify()}\n")
        if origin_btn is None:
            raise ValueError(f'The exact criteria "{EXACT_CRITERIA_ID}" is not found in original filed')

        origin_btn_attrs = origin_btn.attrs
        origin_btn_text = origin_btn.text.strip()
        origin_btn_name = origin_btn.name

        # print(origin_btn_attrs)
        # print(origin_btn_text)
        # print(origin_btn_name)

        elements = soup_diff.find_all(origin_btn_name)
        buttons = []  # possible elements to compare

        for element in elements:
            score = 0

            # check for button text similarity:
            if element.text.strip() == origin_btn_text:
                score += 10

            # check for button attributes similarity:
            for attr_key, attr_value in origin_btn_attrs.items():
                if element.has_attr(attr_key):  # if item has the same attribute
                    # print(f"{attr_key}  ////  {attr_value}  ////   {element.attrs[attr_key]}  ////  {element}")

                    if attr_key == 'class':
                        same_classes = list(set(attr_value) & set(element.attrs[attr_key]))
                        if len(same_classes):
                            score += len(same_classes)*5
                    elif element.attrs[attr_key] == attr_value:
                        score += 5

            if score:
                buttons.append({'element': element, 'score': score})

        # print(len(buttons))
        # print(buttons)
        if len(buttons):
            sorted_buttons = sorted(buttons, key=lambda k: k['score'], reverse=True)
            # print(sorted_buttons)
            print(f"Matching element in '{dif_file}' found: \n\n {sorted_buttons[0]['element']}")
            pass
        else:
            print("No matching element found!")

    except FileNotFoundError as error:
        print("Exception:", error)
    except ValueError as error:
        print("Exception:", error)
    except Exception as error:
        print("Exception:", error)



if __name__ == '__main__':
    main()
