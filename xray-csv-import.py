from xml.etree import ElementTree
import csv


def parse_xml_to_csv():
    row_list = ["TCID", "Test Summary", "Precondition", "Test Priority", "Step", "Data", "Result"]
    tree = ElementTree.parse("xxxx.xml")
    root = tree.getroot()

    with open('output_test.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(row_list)
        # TCID, Test Summary, Test Priority, Step Data, Result
        index = 1
        for testcase in root.iter('testcase'):
            first_step = True
            testcase_name = testcase.attrib['name']
            test_precondition = ""
            print("Name: " + testcase_name)
            for precondition in testcase.iter('preconditions'):
                if precondition.text is not None:
                    test_precondition += precondition.text.replace('"', '')
                print("Test Precondition: " + test_precondition)
            if len(list(testcase.iter('step'))) == 0:
                writer.writerow([index, testcase_name, test_precondition, "High", "", "", ""])
            for step in testcase.iter('step'):
                final_action = step.find('actions').text.replace('"', '')
                expected_result = step.find('expectedresults').text.replace('"', '')
                print("Action:" + final_action)
                print("Expected result: " + expected_result)
                if first_step is True:
                    writer.writerow(
                        [index, testcase_name, test_precondition, "High", final_action, "", expected_result])
                    first_step = False
                else:
                    writer.writerow([index, "", "", "", final_action, "", expected_result])
            index += 1
            print("\n")


def prepare_execution_step(index, step, required_data, result):
    template = '"index": {}, "step": "{}", "data": "{}", "result": "{}"'.format(index, step,
                                                                                required_data, result)
    return '{' + template + '}'


if __name__ == "__main__":
    # print(prepare_execution_step(0, "Hello World", "nothing", "expected result"))
    parse_xml_to_csv()
